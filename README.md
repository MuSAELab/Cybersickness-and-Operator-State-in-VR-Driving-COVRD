# Cybersickness and Operator State in VR Driving (COVRD)
---

The repository contains scripts and documentation for analyzing the **Cybersickness and Operator State in VR Driving (COVRD)** dataset. This multimodal dataset includes EEG, ECG, and respiration signals collected from 60 participants during simulated driving tasks in Virtual Reality. In addition to physiological recordings, the dataset contains self-reported measures of mental states, including mental workload, stress, and cybersickness levels.

## Downloading the Dataset
---

The repository only contains a sample of the dataset for use in the python notebook. The full dataset is available on the Federated Research Data Repository ([link](https://www.frdr-dfdr.ca/repo/dataset/)):

To cite the dataset:


## Dataset Parsing
---

The dataset signals can be loaded using the `datahandling` file provided in `code/`. Example code for loading participant data (both raw signals and features) is available in the `loading_subject_data.ipynb` notebook.

## Pre-Extracted Features
---

Pre-processing was first performed on the signals before feature extraction:
| Modality    | Preprocessing  | Artifact Removal |
|--------------|--------------------------|-----------|
| EEG          | 0.5–45 Hz Bandpass | Artifact Subspace Reconstruction (ASR) |
| ECG          | 0.5–40 Hz Bandpass + R-peak detection | RR Outlier Removal |
| Respiration  | 0.05-1 Hz Bandpass | None |

Features were extracted as shown in the table below:

| Modality   | Feature Types                              | Window Size (s) | Overlap (s) | Filename |
|------------|---------------------------------------------|-----------------|-------------|---------|
| EEG        | Power Spectral Density (PSD)                | 8               | 4           | `eeg_features_w8_o4.csv` |
| ECG        | HRV (Time-Domain)                           | 30              | 15           | `hrv_features_w30_o15.csv` |
| Respiration| Breathing Rate (Time-Domain and Spectral)   | 30              | 15           | `br_features_w30_o15.csv` |

## Survey and Other Information

The subjective ratings (NASA-TLX, DASS-21 and SSQ) and demographic information are avalible both in raw and processed formats. 

Additionally, information about the power line frequency (notch filter frequcy) for the dataset is provided for subject to subject basis as data collection was done both in Europe and America.


