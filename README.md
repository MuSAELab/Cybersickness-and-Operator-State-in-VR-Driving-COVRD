# Cybersickness and Operator State in VR Driving (COVRD)

The repository contains scripts and documentation for analyzing the **Cybersickness and Operator State in VR Driving (COVRD)** dataset. This multimodal dataset includes EEG, EOG, ECG, respiration, and head movement signals collected from 60 participants during simulated driving tasks in Virtual Reality. In addition to physiological recordings, the dataset contains self-reported measures of mental states, including mental workload, stress, and cybersickness levels.

---

## Table of Contents

- [Dataset Information](#dataset-information)
- [Downloading the Dataset](#downloading-the-dataset)
- [Citation](#citation)
- [License](#license)
- [Data Collection Overview](#data-collection-overview)
- [Dataset Structure](#dataset-structure)
- [File Descriptions](#file-descriptions)
- [Dataset Parsing](#dataset-parsing)
- [Pre-Extracted Features](#pre-extracted-features)
- [Methodological Information](#methodological-information)
- [Data Quality and Missing Data](#data-quality-and-missing-data)
- [Contributors](#contributors)

---

## Dataset Information

**Title:** Cybersickness and Operator State in VR Driving (COVRD) Dataset

**Related publication:** *A Multimodal Dataset for the Study of Cybersickness Under Stress and Mental Workload During Immersive VR Driving* (submitted to Frontiers in Neuroergonomics; link will be added upon publication)

---

## Downloading the Dataset

This repository contains only a sample of the dataset for use with the provided Python notebook. The full dataset is available on the Federated Research Data Repository:

🔗 [https://www.frdr-dfdr.ca/repo/dataset/](https://www.frdr-dfdr.ca/repo/dataset/)

---

## Citation

If you use this dataset, please cite:

> Tiwari, A., Moinnereau, M., Benesch, D., Bolt, N., Krätzig, G., Paré, S., Falk, T. (2026). *Cybersickness and Operator State in VR Driving (COVRD)*. Federated Research Data Repository. https://doi.org/10.20383/103.01679

---

## License

These data are available under a **CC BY 4.0** license: <https://creativecommons.org/licenses/by/4.0/>

---

## Data Collection Overview

Data was collected from 60 participants using a VR driving simulator instrumented with physiological sensors, including a VR-integrated EEG, EOG, and head-movement system, and a chest belt for ECG and respiration. Survey questionnaires were administered directly within the VR environment.

Each participant completed four driving phases:

- **Phase 1** — Straight-line driving at low speed with no surrounding traffic.
- **Phase 2** — Introduces turns, light traffic, and pedestrian activity to encourage visual exploration and head movement.
- **Phase 3** — Further increases complexity with more turns and denser traffic.
- **Phase 4** — Corresponds to one of three experimental conditions (see below).

Phases 1–3 are common across all participants and conditions. Each experimental condition in phase 4 was performed by 20 unique participants (i.e., participant `S01` in `1_MW` is a different individual from `S01` in `2_Stress`).

**Experimental conditions:**

| Condition | Folder | Description |
|---|---|---|
| Mental Workload | `1_MW` | Participants drive while performing a visual monitoring task, counting specific pedestrian configurations appearing in the environment. |
| Stress | `2_Stress` | Additional stressors are introduced: aggressive traffic behavior, increased auditory stimulation (honking, shouting), unexpected events requiring sudden braking, and an emergency-transport scenario framing. |
| Mental Workload + Stress | `3_MW_Stress` | Combines elements of both the Mental Workload and Stress conditions simultaneously. |

**Surveys administered:**

- **Demographic survey** (start of experiment): sex, binned age (for anonymity), spoken language, education level, VR experience/frequency, medical conditions, GAD-7 (Generalized Anxiety Disorder) total score, and pre-experiment comments/concerns.
- **DASS-21 and NASA-TLX**: administered at the start of the simulation (Q1), end of phase 3 (Q4), and end of phase 4 (Q5).
- **SSQ (Simulator Sickness Questionnaire)**: administered at the start of the simulation (Q1) and at the end of each phase (Q2–Q5).

---

## Dataset Structure

```
├── CSDatasetRaw_V1
│   ├── 1_MW
│   │   ├── S01
│   │   │   ├── phase_1
│   │   │   │   ├── BreathingRaw.csv
│   │   │   │   ├── ECGRaw.csv
│   │   │   │   ├── EEGRaw.csv
│   │   │   │   ├── EOGRaw.csv
│   │   │   │   ├── HeadMovement_AccRaw.csv
│   │   │   │   ├── features_br_w30_o15.csv
│   │   │   │   ├── features_eeg_w8_o4.csv
│   │   │   │   ├── features_hrv_w30_o15.csv
│   │   │   │   └── rpeak_signal.csv
│   │   │   ├── phase_2
│   │   │   ├── phase_3
│   │   │   └── phase_4
│   │   ├── S02
│   │   ├── ...
│   │   └── S20
│   ├── 2_Stress
│   ├── 3_MW_Stress
│   └── Codebooks_and_mappings
```

- Directories `2_Stress` and `3_MW_Stress` follow the same structure as `1_MW`.
- Within each `phase_X` folder, file names are consistent across subjects, with a few documented exceptions (see [Data Quality and Missing Data](#data-quality-and-missing-data)).
- Processed and demographic data files are provided at the top level of `CSDatasetRaw_V1`.

---

## File Descriptions

| Item | Description |
|---|---|
| **`1_MW/`** | All driving phases with physiological data from the Mental Workload condition. |
| **`2_Stress/`** | All driving phases with physiological data from the Stress condition. |
| **`3_MW_Stress/`** | All driving phases with physiological data from the combined Mental Workload + Stress condition. |
| **`S01`–`S20`** | Unique subject folders per condition (subjects are not shared across conditions). |
| **`phase_1`–`phase_4`** | Physiological data for a given driving phase (see [Methodological Information](#methodological-information)). |
| **`Codebooks_and_mappings/`** | Codebooks (`{filename}_codebook.csv`) documenting column names, labels, valid ranges, and missing-value conventions for each data file, plus `raw_to_processed_mapping.csv`, which documents the encoding used for categorical variables in `processed_demo_info.csv`. |
| **`BreathingRaw.csv`** | Raw breathing data per phase, collected via Bioharness 3 at 18 Hz. |
| **`ECGRaw.csv`** | Raw ECG data per phase, collected via Bioharness 3 at 250 Hz. |
| **`EEGRaw.csv`** | Raw EEG data collected with the Kaptics instrumented VR headset (channels: Fp1, Fpz, Fp2, F1, F2, C1, C2, P3, P4, O1, Oz, O2; dry electrodes, 250 Hz). |
| **`HeadMovement_AccRaw.csv`** | Raw head movement data (3-axis accelerometer, 250 Hz) from the Kaptics headset/acquisition board. |
| **`EOGRaw.csv`** | Raw EOG data from 4 electrodes on the HMD face cushion (frontal, horizontal, and vertical channels), 250 Hz. |
| **`features_eeg_w8_o4.csv`** | Benchmark power spectral density (PSD) EEG features from 8 s epochs with 4 s overlap. |
| **`features_hrv_w30_o15.csv`** | Benchmark time-domain HRV features from 30 s epochs with 15 s overlap. Includes `rr_coverage` (0–100), an ECG quality metric per epoch. |
| **`features_br_w30_o15.csv`** | Benchmark time- and frequency-domain breathing-rate features from 30 s epochs with 15 s overlap. |
| **`rpeak_signal.csv`** | Detected R-peak mask from processed ECG signals (1 = R-peak, 0 = otherwise), sampled at 250 Hz. |
| **`raw_demographic_info.csv`** | Raw survey demographic data collected at the start of the experiment. |
| **`raw_{questionnaire_name}_questionnaire.csv`** | Raw subject responses per questionnaire: SSQ (`ssq`), DASS (`dass`), NASA-TLX (`nasa_tlx`). |
| **`processed_ratings.csv`** | Processed/aggregated questionnaire ratings per phase and condition — mean NASA-TLX and DASS scores per dimension, and total SSQ score. Reorganized by phase (`phase_1`–`phase_4`); Q1 excluded. |
| **`processed_demo_info.csv`** | Processed demographic information with categorical variables numerically encoded (see `Codebooks_and_mappings/raw_to_processed_mapping.csv`). |
| **`processed_merged_ratings_and_demo.csv`** | Merged `processed_demo_info.csv` and `processed_ratings.csv` for streamlined downstream analysis. |
| **`eeg_signal_quality.csv`** | Documents bad EEG channels for all subjects, phases, and conditions. |
| **`eeg_notch_filtering_info.csv`** | Documents powerline frequency (50 Hz or 60 Hz) per subject/phase/condition, based on data collection site (Europe or America). |

---

## Dataset Parsing

The dataset signals can be loaded using the `datahandling` module provided in `code/`. Example code for loading participant data (both raw signals and features) is available in the `loading_subject_data.ipynb` notebook. Data parsers require Python to run.

---

## Pre-Extracted Features

Preprocessing was performed on the signals prior to feature extraction:

| Modality | Preprocessing | Artifact Removal |
|---|---|---|
| EEG | 0.5–45 Hz Bandpass | Artifact Subspace Reconstruction (ASR) |
| ECG | 0.5–40 Hz Bandpass + R-peak detection | RR outlier removal (range- and rate-of-change-based) |
| Respiration | 0.05–1 Hz Bandpass | None |

Features were then extracted as follows:

| Modality | Feature Types | Window Size (s) | Overlap (s) | Filename |
|---|---|---|---|---|
| EEG | Power Spectral Density (PSD), by band (delta, theta, alpha, beta, low gamma) | 8 | 4 | `features_eeg_w8_o4.csv` |
| ECG | HRV (time-domain) | 30 | 15 | `features_hrv_w30_o15.csv` |
| Respiration | Breathing rate (time-domain and spectral) | 30 | 15 | `features_br_w30_o15.csv` |

---

## Methodological Information

**EEG:** Quality assessment of EEG channels was first performed. Bad channels were defined as those exhibiting an 
absolute amplitude < 0.5 uV for more than 98% of a given driving phase, indicating near-flat or non-informative signal behavior. Preprocessed using the EEGLAB toolbox in MATLAB. A 0.5–45 Hz bandpass filter was applied first, followed by artifact removal (eye blinks, muscle/eye movement) using ASR with default EEGLAB parameters. Cleaned signals were re-referenced to the average and decomposed into delta (0.5–4 Hz), theta (4–8 Hz), alpha (8–12 Hz), beta (12–30 Hz), and low gamma (30–45 Hz) bands. Signals were epoched into 8 s windows with 50% overlap, and normalized power spectral features were extracted per epoch.

**ECG:** RR intervals were detected per driving phase using the NeuroKit2 Python package. Signals were epoched into 30 s windows with 50% overlap. RR outlier filtering was then applied:
- **Range-based filter:** only RR intervals between 400–1500 ms are retained.
- **Rate-of-change filter:** successive RR interval changes > 25% are removed.

An RR quality metric was computed as the proportion of accepted RR intervals relative to total epoch duration (lower values indicate more rejected data due to noise/artifacts). Epochs with an RR quality metric below 60% were excluded from feature extraction, resulting in an empty row in the corresponding feature file.

**Respiration (BR):** Bandpass filtering was applied first, followed by epoching into 30 s windows with 50% overlap.

**Quality assurance:** Data quality was assessed for EEG and ECG during feature extraction. Files or epochs failing predefined quality criteria were excluded, resulting in either missing feature files (entire file failed) or missing/empty feature rows (individual epochs failed).

**Software/tools:** Data parsers are available in this GitHub repository and require Python. EEG preprocessing used MATLAB/EEGLAB; ECG processing used the Python NeuroKit2 package.

---

## Data Quality and Missing Data

- **EEG:** Features were not generated for files with one or more missing channels (see `eeg_signal_quality.csv`) or for files that failed ASR-based artifact removal due to channels with excessive noise or highly correlated channels.
- **HRV/BR:** Feature files are missing when no epochs within a file passed the quality criteria; individual rows are missing/empty when specific epochs were rejected.


**Known instances:**

| File(s) | Issue |
|---|---|
| `features_eeg_w8_o4.csv` | 211 instances missing across 29 folders. |
| `2_Stress/S04/phase_4/features_br_w30_o15.csv` | Row for the 4th epoch is empty. |
| `3_MW_Stress/S13/phase_1/features_hrv_w30_o15.csv` | Rows for the 5th and 6th epochs are empty. |

---

For EEG data, the files with bad channels include:

| Experimental Condition | Subject | Driving Phase(s) | Bad Channels   |
| ---------------------- | ------- | ---------------- | -------------- |
| MW                     | S04     | 1–4              | F2             |
| MW                     | S07     | 1–4              | C2             |
| MW                     | S09     | 1–2              | P3, O1, Oz, O2 |
| MW                     | S09     | 3                | Oz, O2         |
| MW                     | S09     | 4                | O1, Oz, O2     |
| Stress                 | S07     | 1–3              | F2, C2         |
| Stress                 | S07     | 4                | F2, C2, P4     |
| Stress                 | S08     | 1                | F2, C2         |
| Stress                 | S08     | 2                | F2, P3, Oz     |
| Stress                 | S08     | 3                | F2             |
| Stress                 | S09     | 1                | F2             |
| Stress                 | S09     | 2                | F1             |
| Stress                 | S09     | 3                | F1, C1, P4     |
| Stress                 | S09     | 4                | F1, P4         |
| Stress                 | S17     | 3                | C2             |

*Table: EEG channels that did not pass the bad channel quality criteria.*


## Contributors

**Principal Investigator**
- Tiago Falk — Institut National de la Recherche Scientifique, INRS-EMT — Tiago.Falk@inrs.ca

**Co-Investigators**
- Abhishek Tiwari — INRS-EMT — abhishek.tiwari@inrs.ca
- Marc-Antoine Moinnereau - INRS-EMT
- Danielle Benesch — Thales, CortAIx Labs 
- Nicole Bolt — University of Saskatchewan
- Gregory Krätzig — University of Regina 
- Simon Paré — Public Safety Canada 

