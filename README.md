# Cybersickness and Operator State in VR Driving (COVRD)
---

The repository contains scripts and documentation for analyzing the **Cybersickness and Operator State in VR Driving (COVRD)** dataset. This multimodal dataset includes EEG, ECG, and respiration signals collected from 60 participants during simulated driving tasks in Virtual Reality. In addition to physiological recordings, the dataset contains self-reported measures of mental states, including mental workload, stress, and cybersickness levels.

## Downloading the Dataset
---

The dataset is available on the Federated Research Data Repository ([link](https://www.frdr-dfdr.ca/repo/dataset/)):

To cite the dataset:


## Dataset Parsing
---

The dataset signals can be loaded using the `datahandling` class provided in `src/`. Example code for loading participant data is available in the `loading_subject_data.ipynb` notebook located in the `notebooks/` folder.

## Pre-Extracted Features
---

Pre-processed and extracted features are avalible each subject and modality with the following settings:

| Modality   | Feature Types                              | Window Size (s) | Overlap (s) |
|------------|---------------------------------------------|-----------------|-------------|
| EEG        | Power Spectral Density (PSD)                | 3               | 1           |
| ECG        | HRV (Time-Domain)                           | 30              | 0           |
| Respiration| Breathing Rate (Time-Domain and Spectral)   | 30              | 0           |

The pre-processing performed on the signals for extracting features is described below:
| Modality    | Preprocessing  | Artifact Removal |
|--------------|--------------------------|-----------|
| EEG          | 0.5–40 Hz Bandpass | Artifact Subspace Reconstruction (ASR) |
| ECG          | 0.5–40 Hz Bandpass | R-peak detection + Outlier Removal |
| Respiration  | Bandpass filtering | None |
