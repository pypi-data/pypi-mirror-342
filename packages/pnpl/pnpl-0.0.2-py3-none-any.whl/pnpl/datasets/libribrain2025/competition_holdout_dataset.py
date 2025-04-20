import os
from torch.utils.data import Dataset
import torch
from pnpl.datasets.libribrain2025.constants import PHONEME_CLASSES, SPEECH_CLASSES, PHONEME_HOLDOUT_PREDICTIONS, SPEECH_HOLDOUT_PREDICTIONS
import csv
import torch
import warnings


class LibriBrainCompetitionHoldout(Dataset):
    def __init__(self, data_path: str, task: str = "speech"):
        # Path to the data
        self.data_path = data_path
        self.task = task
        if (task == "speech"):
            sample_path = os.path.join(
                self.data_path, "competitionShuffled", "speech_samples.pt")
        elif (task == "phoneme"):
            sample_path = os.path.join(
                self.data_path, "competitionShuffled", "phoneme_samples.pt")
        else:
            raise ValueError(
                f"Task {task} not supported. Please use 'speech' or 'phoneme'.")

        try:
            with open(sample_path, "rb") as f:
                self.samples = torch.load(f)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"File {sample_path} not found. Please provide the correct data_path and run the competition_holdout_dataset.py script to generate the file.")

    def generate_submission_in_csv(self, predictions, output_path: str):
        """
        Generates a submission file in CSV format for the LibriBrain competition.
        The file contains the run keys and the corresponding labels.
        Args:
            predictions (List[Tensor]): List of scalar tensors, each representing a speech probability.
            output_path (str): Path to save the CSV file.
        """
        if self.task == "speech":
            if len(predictions) != SPEECH_HOLDOUT_PREDICTIONS:
                raise (ValueError(
                    "Length of speech predictions does not match number of segments."))
            if predictions[0].shape[0] != SPEECH_CLASSES:
                raise (ValueError(
                    "Speech classes does not match expect size (1)."))

            with open(output_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["segment_idx", "speech_prob"])

                for idx, tensor in enumerate(predictions):
                    # Ensure we extract the scalar float from tensor
                    speech_prob = tensor.item() if isinstance(
                        tensor, torch.Tensor) else float(tensor)
                    writer.writerow([idx, speech_prob])
        elif self.task == "phoneme":
            if len(predictions) != PHONEME_HOLDOUT_PREDICTIONS:
                raise (ValueError(
                    "Length of Phonemes predictions does not match number of segments."))
            if predictions[0].shape[0] != PHONEME_CLASSES:
                raise (ValueError(
                    f"Phonemes classes does not match expect size ({PHONEME_CLASSES})."))
            with open(output_path, mode='w', newline='') as csvfile:
                writer = csv.writer(csvfile)

                # Create header: segment_idx, phoneme_1, ..., phoneme_39
                header = ["segment_idx"] + \
                    [f"phoneme_{i + 1}" for i in range(39)]
                writer.writerow(header)

                for idx, tensor in enumerate(predictions):
                    # Ensure tensor is a flat list of floats
                    if isinstance(tensor, torch.Tensor):
                        probs = tensor.squeeze().tolist()  # shape: (39,)
                    else:
                        # if tensor is already a list-like
                        probs = list(tensor)

                    writer.writerow([idx] + probs)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


if __name__ == "__main__":
    output_path = "/Users/mirgan/pnpl"

    """dataset = LibriBrainCompetitionHoldout(
        "/Users/mirgan/LibriBrain/serialized", task="speech")
    random_predictions = [torch.rand(1, 1) for _ in range(1043)]

    dataset.generate_submission_in_csv(
        predictions=random_predictions, output_path=os.path.join(output_path, "speech_predictions.csv"))
    """
    dataset = LibriBrainCompetitionHoldout(
        "/Users/mirgan/LibriBrain", task="phoneme")
    random_predictions = [torch.randn(39) for _ in range(6862)]
    dataset.generate_submission_in_csv(
        predictions=random_predictions, output_path=os.path.join(output_path, "phoneme_predictions.csv"))

    print(len(dataset))
    print(dataset[0].shape)
    print(dataset[1].shape)
