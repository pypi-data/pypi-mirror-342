from pnpl.datasets import LibriBrainPhoneme
from torch.utils.data import DataLoader
import torch
import os
from pnpl.datasets import GroupedDataset
from torch.utils.data import Subset


def event_in_phoneme_split(onset, tmin, sfreq, cutoff):
    start = max(0, int((onset + tmin) * sfreq))
    return start >= cutoff


def obfuscate_phoneme():
    output_path = "/Users/mirgan/LibriBrain/competitionShuffled/"
    dataset = LibriBrainPhoneme(
        data_path="/Users/mirgan/LibriBrain/serialized",
        include_run_keys=[("0", "2025", "pnpl-competition-holdout", "1")],
        standardize=True,
        clipping_boundary=10,
        preprocessing_str=None,
        preload_files=False,
        include_info=True
    )
    dataset[0]  # hack to make it open the h5 file
    cutoff = dataset.open_h5_datasets[(
        "0", "2025", "pnpl-competition-holdout", "1")].shape[1] // 2
    assert cutoff == 211125
    indices_in_phoneme_split = [i for i in range(len(dataset)) if event_in_phoneme_split(
        dataset[i][2]["onset"], tmin=dataset.tmin, sfreq=dataset.sfreq, cutoff=cutoff)]
    print("Holdout contains ", len(indices_in_phoneme_split),
          " samples in phoneme split")
    phoneme_split_dataset = Subset(dataset, indices_in_phoneme_split)
    avg_dataset = GroupedDataset(
        original_dataset=phoneme_split_dataset, grouped_samples=100, average_grouped_samples=True)
    held_back_indices = []
    for group in avg_dataset.groups:
        held_back_indices.append(group[0])
    print("Holding back ", len(held_back_indices),
          " samples to facilitate averaging")

    print("Holdout contains ", len(phoneme_split_dataset), " samples")
    phoneme_split_dataset_public_indices = [i for i in range(
        len(phoneme_split_dataset)) if i not in held_back_indices]
    phoneme_split_dataset_public = Subset(
        phoneme_split_dataset, phoneme_split_dataset_public_indices)
    dataloader = DataLoader(
        phoneme_split_dataset_public, batch_size=1, shuffle=True, num_workers=0)
    data = []
    labels = []
    for batch in dataloader:
        sample = batch[0].squeeze(0)
        label = batch[1].squeeze(0)
        data.append(sample)
        labels.append(label)
    single_data = torch.stack(data)
    single_labels = torch.stack(labels)
    print("Single phoneme data shape: ", single_data.shape)
    print("Single phoneme labels shape: ", single_labels.shape)

    os.makedirs(output_path, exist_ok=True)
    torch.save(single_data, output_path + "single_phoneme_samples.pt")
    torch.save(single_labels, output_path + "single_phoneme_labels.pt")

    # average phoneme dataset
    avg_data = []
    avg_labels = []
    avg_loader = DataLoader(
        avg_dataset, batch_size=1, shuffle=True, num_workers=0)
    for batch in avg_loader:
        sample = batch[0].squeeze(0)
        label = batch[1].squeeze(0)
        avg_data.append(sample)
        avg_labels.append(label)
    avg_data = torch.stack(avg_data)
    avg_labels = torch.stack(avg_labels)
    print("Average phoneme data shape: ", avg_data.shape)
    print("Average phoneme labels shape: ", avg_labels.shape)
    torch.save(avg_data, output_path + "avg_phoneme_samples.pt")
    torch.save(avg_labels, output_path + "avg_phoneme_labels.pt")


def main():
    torch.manual_seed(42)
    obfuscate_phoneme()


main()
