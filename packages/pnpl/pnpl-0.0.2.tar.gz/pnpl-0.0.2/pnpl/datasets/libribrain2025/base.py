import os
import numpy as np
import pandas as pd
import h5py
import torch
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor
from pnpl.datasets.libribrain2025.constants import RUN_KEYS, PHONATION_BY_PHONEME
from pnpl.datasets.utils import check_include_and_exclude_ids, include_exclude_ids
from torch.utils.data import Dataset
from huggingface_hub import hf_hub_download
from pnpl.datasets.libribrain2025.constants import VALIDATION_RUN_KEYS, TEST_RUN_KEYS


class LibriBrainBase(Dataset):
    # Adjust max_workers as needed.
    _executor = ThreadPoolExecutor(max_workers=4)
    _download_futures = {}
    _lock = threading.Lock()

    def __init__(
            self,
            data_path: str,
            partition: str | None = None,
            preprocessing_str: str | None = "bads+headpos+sss+notch+bp+ds",
            tmin: float = 0.0,
            tmax: float = 0.5,
            include_run_keys: list[str] = [],
            exclude_run_keys: list[str] = [],
            exclude_tasks: list[str] = [],
            standardize: bool = True,
            clipping_boundary: float | None = 10,
            channel_means: np.ndarray | None = None,
            channel_stds: np.ndarray | None = None,
            include_info: bool = False,
            preload_files: bool = False,
    ):
        """
        IMPORTANT: Channels x Time

        data_path: path to the base directory containing task folders.
                   Each task folder should contain a derivatives folder with subdirectories:
                   - serialised (for h5 files)
                   - events (for tsv files)
        preprocessing_str: preprocessing string used to preprocess the data.
        tmin: start time of the sample in seconds in reference to the onset of the phoneme.
        standardize: whether to standardize the data.
        clipping_boundary: factor to clip the data by. None for not clipping.
        channel_means: means of the channels in the dataset.
        channel_stds: stds of the channels in the dataset.
        preload_files: whether to preload all required files in parallel (True) or download
                      as needed (False).
        """
        os.makedirs(data_path, exist_ok=True)
        self.data_path = data_path
        self.partition = partition
        self.preprocessing_str = preprocessing_str
        self.tmin = tmin
        self.tmax = tmax
        self.include_run_keys = include_run_keys
        self.exclude_run_keys = exclude_run_keys
        self.standardize = standardize
        self.clipping_boundary = clipping_boundary
        self.channel_means = channel_means
        self.channel_stds = channel_stds
        self.include_info = include_info
        self.preload_files = preload_files

        if partition is not None:
            if include_run_keys or exclude_run_keys or exclude_tasks:
                raise ValueError(
                    "partition is a shortcut to indicate what data to include. include_run_keys, exclude_run_keys, exclude_tasks must be empty when partition is not None")
            if partition == "train":
                exclude_run_keys = VALIDATION_RUN_KEYS + TEST_RUN_KEYS
            elif partition == "validation":
                include_run_keys = VALIDATION_RUN_KEYS
            elif partition == "test":
                include_run_keys = TEST_RUN_KEYS
            else:
                raise ValueError(
                    f"Invalid partition: {partition}. Must be one of: train, validation, test")
        # Convert channel_means and channel_stds to np.ndarray if they are provided as lists.
        if isinstance(channel_means, list):
            self.channel_means = np.array(channel_means)
        if isinstance(channel_stds, list):
            self.channel_stds = np.array(channel_stds)

        include_run_keys = [tuple(run_key) for run_key in include_run_keys]
        exclude_run_keys = [tuple(run_key) for run_key in exclude_run_keys]
        check_include_and_exclude_ids(
            include_run_keys, exclude_run_keys, RUN_KEYS)

        intended_run_keys = include_exclude_ids(
            include_run_keys, exclude_run_keys, RUN_KEYS)
        self.intended_run_keys = [
            run_key for run_key in intended_run_keys if run_key[2] not in exclude_tasks]

        if len(self.intended_run_keys) == 0:
            raise ValueError(
                f"Your configuration does not allow any run keys to be included. Please check configuration: include_run_keys={include_run_keys}, exclude_run_keys={exclude_run_keys}, exclude_tasks={exclude_tasks}"
            )

        # Preload files if requested BEFORE calling _get_sfreq which would trigger sequential downloads
        if self.preload_files:
            self.prefetch_files()

        # Now we can safely get sfreq as files are already downloading/downloaded
        self.sfreq = self._get_sfreq(
            self.intended_run_keys[0][0],
            self.intended_run_keys[0][1],
            self.intended_run_keys[0][2],
            self.intended_run_keys[0][3]
        )
        self.points_per_sample = int((tmax - tmin) * self.sfreq)
        self.open_h5_datasets = {}

    def __len__(self):
        return len(self.samples)

    def prefetch_files(self):
        """Preload all required files in parallel."""
        futures = []
        needed_files = set()

        # Collect all file paths that we'll need
        for subject, session, task, run in self.intended_run_keys:
            # H5 files
            h5_path = self._get_h5_path(subject, session, task, run)
            if not os.path.exists(h5_path):
                needed_files.add(h5_path)

            # Event files
            events_path = self._get_events_path(subject, session, task, run)
            if not os.path.exists(events_path):
                needed_files.add(events_path)

        # Schedule downloads for all files that don't exist locally
        for fpath in needed_files:
            futures.append(self._schedule_download(fpath))

        # Wait for all downloads to complete
        if futures:
            print(f"Downloading {len(futures)} files...")
            for future in futures:
                try:
                    future.result()
                except Exception as e:
                    print(f"Error downloading a file: {e}")
            print("Done!")

    def _schedule_download(self, fpath):
        """Schedule a file download with retry logic."""
        rel_path = os.path.relpath(fpath, self.data_path)
        # Windows fix: convert Windows path separator to URL path separator
        rel_path = rel_path.replace(os.path.sep, '/')
        os.makedirs(os.path.dirname(fpath), exist_ok=True)

        with LibriBrainBase._lock:
            if fpath not in LibriBrainBase._download_futures:
                LibriBrainBase._download_futures[fpath] = LibriBrainBase._executor.submit(
                    self._download_with_retry,
                    fpath=fpath,
                    rel_path=rel_path
                )
            return LibriBrainBase._download_futures[fpath]

    def _download_with_retry(self, fpath, rel_path, max_retries=5):
        """Download a file (with retry logic for handling timeouts).

        If the environment variable HF_TOKEN is set, use it to authenticate the download
        and switch to the "pnpl/LibriBrain" repo instead of "pnpl/LibriBrain-alpha".
        """
        retries = 0
        while retries < max_retries:
            try:
                hf_token = os.environ.get("HF_TOKEN")
                if hf_token:
                    repo_id = "pnpl/LibriBrain"
                else:
                    repo_id = "pnpl/LibriBrain-alpha"
                return hf_hub_download(
                    repo_id=repo_id,
                    repo_type="dataset",
                    filename=rel_path,
                    local_dir=self.data_path,
                    token=hf_token
                )
            except Exception as e:
                retries += 1
                # Exponential backoff with jitter
                wait_time = 2 ** retries + random.uniform(0, 1)
                if retries < max_retries:
                    print(
                        f"Download error for {os.path.basename(fpath)}, retrying in {wait_time:.1f}s ({retries}/{max_retries})")
                    time.sleep(wait_time)
                else:
                    print(
                        f"Failed to download {os.path.basename(fpath)} after {max_retries} attempts")
                    raise e

    def _ensure_file(self, fpath: str) -> str:
        """
        Ensures the file exists locally, downloading if needed.
        This is a blocking call that waits for download to complete.
        """
        if os.path.exists(fpath):
            return fpath

        future = self._schedule_download(fpath)
        # Wait for the download to complete
        return future.result()

    def _get_h5_path(self, subject: str, session: str, task: str, run: str) -> str:
        """
        Gets the path to the h5 file.
        """
        fname = f"sub-{subject}_ses-{session}_task-{task}_run-{run}"
        if self.preprocessing_str is not None:
            fname += f"_proc-{self.preprocessing_str}"
        fname += "_meg.h5"
        return os.path.join(self.data_path, task, "derivatives", "serialised", fname)

    def _get_events_path(self, subject: str, session: str, task: str, run: str) -> str:
        """
        Gets the path to the events file.
        """
        fname = f"sub-{subject}_ses-{session}_task-{task}_run-{run}_events.tsv"
        return os.path.join(self.data_path, task, "derivatives", "events", fname)

    def _ids_to_h5_path(self, subject: str, session: str, task: str, run: str) -> str:
        """
        Gets the path to the h5 file and ensures it exists.
        """
        path = self._get_h5_path(subject, session, task, run)
        return self._ensure_file(path)

    def _get_sfreq(self, subject, session, task, run):
        h5_path = self._ids_to_h5_path(subject, session, task, run)
        with h5py.File(h5_path, "r") as h5_file:
            sfreq = h5_file.attrs["sample_frequency"]
        return sfreq

    def _load_events(self, subject: str, session: str, task: str, run: str):
        fpath = self._get_events_path(subject, session, task, run)
        fpath = self._ensure_file(fpath)
        events_df = pd.read_csv(fpath, sep="\t")
        return events_df

    def _calculate_standardization_params(self):
        n_samples = []
        means = []
        stds = []
        for run_key in self.run_keys:
            subject, session, task, run = run_key
            hdf_dataset = h5py.File(self._ids_to_h5_path(
                subject, session, task, run), "r")["data"]
            data = hdf_dataset[:, :]

            if "channel_means" in hdf_dataset.attrs and "channel_stds" in hdf_dataset.attrs:
                channel_means = hdf_dataset.attrs["channel_means"]
                channel_stds = hdf_dataset.attrs["channel_stds"]
            else:
                channel_means = np.mean(data, axis=1)
                channel_stds = np.std(data, axis=1)
                hdf_dataset.file.close()
                with h5py.File(self._ids_to_h5_path(subject, session, task, run), "r+") as f:
                    f["data"].attrs["channel_means"] = channel_means
                    f["data"].attrs["channel_stds"] = channel_stds
                hdf_dataset = h5py.File(self._ids_to_h5_path(
                    subject, session, task, run), "r")["data"]
                print("calculated stats for: ", run_key)

            n_samples.append(data.shape[1])
            means.append(channel_means)
            stds.append(channel_stds)
        means = np.array(means)
        stds = np.array(stds)
        n_samples = np.array(n_samples)
        self.channel_stds, self.channel_means = self._accumulate_stds(
            means, stds, n_samples)
        self.broadcasted_stds = np.tile(
            self.channel_stds, (self.points_per_sample, 1)).T
        self.broadcasted_means = np.tile(
            self.channel_means, (self.points_per_sample, 1)).T

    @staticmethod
    def _accumulate_stds(ch_means, ch_stds, n_samples):
        """
        ch_means: np.ndarray (n_groups, n_channels)
        ch_stds: np.ndarray (n_groups, n_channels)
        n_samples: np.ndarray (n_groups)
        """
        vars = np.array(ch_stds) ** 2
        means_total = np.average(ch_means, axis=0, weights=n_samples)
        sum_of_squares_within = np.sum(
            vars * np.tile(n_samples, (vars.shape[1], 1)).T, axis=0)
        sum_of_squares_between = np.sum(
            (ch_means - np.tile(means_total, (ch_means.shape[0], 1))) ** 2 *
            np.tile(n_samples, (ch_means.shape[1], 1)).T,
            axis=0
        )
        sum_of_squares_total = sum_of_squares_within + sum_of_squares_between
        return np.sqrt(sum_of_squares_total / np.sum(n_samples)), means_total

    def _clip_sample(self, sample, boundary):
        sample = np.clip(sample, -boundary, boundary)
        return sample

    def __getitem__(self, idx):
        # returns channels x time
        if idx >= len(self.samples):
            raise IndexError(
                f"Index {idx} is out of bounds for dataset of size {len(self.samples)}"
            )
        sample = self.samples[idx]
        subject, session, task, run, onset, label = sample
        if self.include_info:
            info = {
                "dataset": "libribrain2025",
                "subject": subject,
                "session": session,
                "task": task,
                "run": run,
                "onset": torch.tensor(onset, dtype=torch.float32),
            }

        if (subject, session, task, run) not in self.open_h5_datasets:
            h5_path = self._ids_to_h5_path(subject, session, task, run)
            h5_dataset = h5py.File(h5_path, "r")["data"]
            self.open_h5_datasets[(subject, session, task, run)] = h5_dataset
        else:
            h5_dataset = self.open_h5_datasets[(subject, session, task, run)]

        start = max(0, int((onset + self.tmin) * self.sfreq))
        end = start + self.points_per_sample
        data = h5_dataset[:, start:end]

        if self.standardize:
            data = (data - self.broadcasted_means) / self.broadcasted_stds

        if self.clipping_boundary is not None:
            data = self._clip_sample(data, self.clipping_boundary)

        if self.include_info:
            return [torch.tensor(data, dtype=torch.float32), label, info]
        return [torch.tensor(data, dtype=torch.float32), label, {}]
