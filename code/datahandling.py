import pandas as pd
import numpy as np
import os
from typing import List, Literal

import numpy as np
import pandas as pd
import re



def parse_signal_csv(
    filename,
    fs=250,
    samples_per_packet=63,
    gap_threshold_factor=2,
    signal_key='SignalRaw',
    normal_packet_interval_ms=252,
):
    """
    Parse streamed signal packets into a continuous signal.

    Parameters
    ----------
    filename : str
        Input CSV containing 'Timestamp' and 'SignalRaw' columns.

    output_filename : str or None
        If provided, save the parsed signal to this CSV.

    fs : float
        Signal sampling frequency in Hz.

    samples_per_packet : int
        Expected number of signal samples per packet.

    gap_threshold_factor : float
        A packet timestamp interval greater than
        normal_packet_interval * this factor is treated as a
        missing-data gap.

    Returns
    -------
    parsed : pandas.DataFrame
        DataFrame containing only:
            Timestamp
            Signal

        Timestamp is in milliseconds and is spaced at exactly 1/fs.

    missing_percent : float
        Percentage of signal samples that were missing and subsequently
        interpolated.
    """

    # read csv file
    df = pd.read_csv(filename)

    def parse_samples(value):
        if pd.isna(value):
            return np.array([], dtype=float)

        # Extract numbers robustly from strings such as:
        # "[520, 521, 523, ...]"
        numbers = re.findall(
            r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?",
            str(value)
        )

        return np.asarray(numbers, dtype=float)

    packet_timestamps = df["Timestamp"].astype(float).to_numpy()

    # samples are stored as strings in the CSV, so we parse them into arrays
    packet_samples = [
        parse_samples(x)
        for x in df[signal_key]
    ]

    
    # timestamp_diffs = np.diff(packet_timestamps)
    # Ignore zero/negative intervals
    # valid_diffs = timestamp_diffs[timestamp_diffs > 0]
    # Large gaps are excluded using the 75th percentile.
    # upper_limit = np.percentile(valid_diffs, 75)

    # normal_diffs = valid_diffs[
    #     valid_diffs <= upper_limit
    # ]

    # 252ms for ECG and 1000ms for BR
    normal_packet_interval = normal_packet_interval_ms

    gap_threshold = (
        normal_packet_interval * gap_threshold_factor
    )

    # sample timestamp generation
    sample_period_ms = 1000.0 / fs
    # use the first packet timestamp as the start.
    start_timestamp = packet_timestamps[0]
    # Total number of expected samples based on packet positions.
    total_samples = 0
    packet_start_indices = []
    current_index = 0

    for i, (timestamp, samples) in enumerate(
        zip(packet_timestamps, packet_samples)
    ):

        if i > 0:
            # dt can both be too early or too late from the expected 
            dt = (packet_timestamps[i] - packet_timestamps[i - 1])

            # Estimate how many packet periods have elapsed using threshold
            if dt > gap_threshold:
                missing_packet_count = max(
                    0,
                    int(round(
                        dt / normal_packet_interval
                    )) - 1
                )

                current_index += (
                    missing_packet_count *
                    samples_per_packet
                )

        packet_start_indices.append(current_index)
        current_index += len(samples)

    total_samples = current_index

    # create signal
    signal = np.full(
        total_samples,
        np.nan,
        dtype=float
    )

    for start_idx, samples in zip(
        packet_start_indices,
        packet_samples
    ):

        end_idx = min(
            start_idx + len(samples),
            total_samples
        )

        signal[start_idx:end_idx] = samples[
            :end_idx - start_idx
        ]



    missing_percent = (
        np.isnan(signal).sum() /
        len(signal)
    ) * 100.0

    # interpolation
    signal_series = pd.Series(signal)

    signal_interpolated = (
        signal_series
        .interpolate(
            method="linear",
            limit_direction="both"
        )
        .to_numpy()
    )

    # generate uniform timestamps for the interpolated signal
    timestamps = (
        start_timestamp +
        np.arange(total_samples) * sample_period_ms
    )

    parsed = pd.DataFrame({
        "Timestamp": timestamps,
        signal_key: signal_interpolated
    })

    return parsed, missing_percent

class LoadStudyData:
    def __init__(self,
                 base_folder: str = './data',
                 experiment: Literal['1_MW', '2_Stress', '3_MW_Stress'] = '1_MW',
                 ):

        self._base_folder = base_folder
        self._experiment = experiment
        self._ecgraw_filename = 'ECGRaw.csv'
        self._brraw_filename = 'BreathingRaw.csv'
        self._rpeak_filename = 'rpeak_signal.csv'
        self._eeg_filename = 'EEGRaw.csv'
        self._eog_filename = 'EOGRaw.csv'
        self._headmovement_filename = 'HeadMovement_AccRaw.csv'
        self.fs_ECG = 250
        self.fs_BR = 18
        self.data_path = os.path.join(self._base_folder, 
                                      self._experiment, 
                                      )
        

    def load_subject_info(self, subject_id: str, phase: Literal[1,2,3,4]):
        self._subject_id = subject_id
        self._condition = phase
        self.file_path = os.path.join(self.data_path, 
                                              self._subject_id, 
                                              'phase_' + str(self._condition))
        

    def _load_data(self, feature_filename: str = None):
        
        df_data = pd.read_csv(os.path.join(self.file_path, feature_filename))

        return df_data
    
    def get_raw_ecg(self):
        df, missing_percent = parse_signal_csv(os.path.join(self.file_path, self._ecgraw_filename), 
                              fs=self.fs_ECG,
                              signal_key = 'EcgRaw'
                              )

        ecgSig = df['EcgRaw'].to_numpy()
        return ecgSig, self.fs_ECG, missing_percent
    
    def get_raw_br(self):
        df, missing_percent = parse_signal_csv(os.path.join(self.file_path, self._brraw_filename), 
                                      fs=self.fs_BR,
                                      signal_key = 'BreathingRaw',
                                      normal_packet_interval_ms=1000,
                                      samples_per_packet=18
                                      )
        
        brSig = df['BreathingRaw'].to_numpy()
        
        return brSig, self.fs_BR, missing_percent
    
    def get_raw_eeg(self, convert_to_uv: bool = True):
        df_eeg  = self._load_data(self._eeg_filename)
        fs_eeg = df_eeg.SamplingRate.iloc[0]
        df_eeg.drop(columns = ['SamplingRate', 'TimeStamp', 'Converted_Timestamp'], axis = 1, inplace = True)
        channel_names = [ch_.split('_')[1] for ch_ in df_eeg.columns]
        replace_ch_dict = {'FP1': 'Fp1', 'FP2': 'Fp2', 'FPZ': 'Fpz', 'OZ': 'Oz'}
        channel_names = [replace_ch_dict.get(x, x) for x in channel_names]
        df_eeg.columns = channel_names
        # converting to microvolts from raw ADC values for Kaptics headset
        if convert_to_uv:
            df_eeg = df_eeg*0.02235
        return df_eeg, fs_eeg

    def get_raw_eog(self, convert_to_uv: bool = True):
            df_eog  = self._load_data(self._eog_filename)
            fs_eog = df_eog.SamplingRate.iloc[0]
            df_eog.drop(columns = ['SamplingRate', 'TimeStamp'], axis = 1, inplace = True)
            # converting to microvolts from raw ADC values for Kaptics headset
            if convert_to_uv:
                df_eog = df_eog*0.02235
            return df_eog, fs_eog

    def get_raw_headmovement(self):
        df_headmovement  = self._load_data(self._headmovement_filename)
        fs_headmovement = df_headmovement.SamplingRate.iloc[0]
        df_headmovement.drop(columns = ['SamplingRate', 'TimeStamp', 'Converted_Timestamp'], axis = 1, inplace = True)
        return df_headmovement, fs_headmovement
    
    def get_rpeak(self):
        df_rpeak = self._load_data(feature_filename = self._rpeak_filename)
        return df_rpeak, self.fs_ECG



class LoadExtractedFeatures:
    def __init__(self,
                 base_folder: str = './data',
                 experiment: Literal['1_MW', '2_Stress', '3_MW_Stress'] = '1_MW',
                 ):

        self._base_folder = base_folder
        self._experiment = experiment
        self._hrv_filename = 'features_hrv__w30_o15.csv'
        self._br_filename = 'features_br_w30_o15.csv'
        self._eeg_filename = 'features_eeg_w8_o4.csv'
        self.data_path = os.path.join(self._base_folder, 
                                      self._experiment, 
                                      )
        

    def load_subject_info(self, subject_id: str, phase: Literal[1,2,3,4]):
        self._subject_id = subject_id
        self._condition = phase
        self.file_path = os.path.join(self.data_path, 
                                    self._subject_id, 
                                    'phase_' + str(self._condition))

    def _load_data(self, feature_filename: str = None):
        
        df_data = pd.read_csv(os.path.join(self.file_path, feature_filename))

        return df_data
    
    def get_features(self, feature_type: Literal['eeg', 'hrv', 'br'] = 'eeg'):
        if feature_type == 'eeg':
            filename = self._eeg_filename
        elif feature_type == 'hrv':
            filename = self._hrv_filename
        elif feature_type == 'br':
            filename = self._br_filename
        df = self._load_data(feature_filename = filename)
        
        return df
    


        