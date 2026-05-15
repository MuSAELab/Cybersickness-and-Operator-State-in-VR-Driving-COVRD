import pandas as pd
import numpy as np
import os
from typing import List, Literal

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
        self._eeg_filename = 'EEG_Data.csv'
        self.fs_ECG = 250
        self.fs_BR = 18
        self.data_path = os.path.join(self._base_folder, 
                                      self._experiment, 
                                      )
        

    def load_subject_info(self, subject_id: str, condition: Literal[1,2,3,4]):
        self._subject_id = subject_id
        self._condition = condition

    def _load_data(self, feature_filename: str = None):
        self.file_path = os.path.join(self.data_path, 
                                      self._subject_id, 
                                      'condition_' + str(self._condition))

        df_data = pd.read_csv(os.path.join(self.file_path, feature_filename))

        return df_data
    
    def get_raw_ecg(self):
        df = self._load_data(feature_filename = self._ecgraw_filename)
        df['ECGVal'] = df.EcgRaw.apply(lambda x: np.array(x.split('[')[2:][-1].split(']')[0].split(','), dtype = int))
        ecgSig = np.empty(0)
        for _, row in df.iterrows():
            ecgSig = np.hstack((ecgSig,row['ECGVal']))
        
        return ecgSig, self.fs_ECG
    
    def get_raw_br(self):
        df = self._load_data(feature_filename = self._brraw_filename)
        df['BRVal'] = df.BreathingRaw.apply(lambda x: np.array(x.split('[')[2:][-1].split(']')[0].split(','), dtype = int))
        brSig = np.empty(0)
        for _, row in df.iterrows():
            brSig = np.hstack((brSig,row['BRVal']))
        
        return brSig, self.fs_BR
    
    def get_raw_eeg(self):
        df_eeg  = pd.read_csv(os.path.join(self.file_path, self._eeg_filename))
        fs_eeg = df_eeg.SamplingRate.iloc[0]
        df_eeg.drop(columns = ['SamplingRate', 'TimeStamp', 'Converted_Timestamp'], axis = 1, inplace = True)
        channel_names = [ch_.split('_')[1] for ch_ in df_eeg.columns]
        replace_ch_dict = {'FP1': 'Fp1', 'FP2': 'Fp2', 'FPZ': 'Fpz', 'OZ': 'Oz'}
        channel_names = [replace_ch_dict.get(x, x) for x in channel_names]
        df_eeg.columns = channel_names

        return df_eeg, fs_eeg
    
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
        self._hrv_filename = 'hrv_features_w30_o15.csv'
        self._br_filename = 'br_features_w30_o15.csv'
        self._eeg_filename = 'eeg_features_w8_o4.csv'
        self.data_path = os.path.join(self._base_folder, 
                                      self._experiment, 
                                      )
        

    def load_subject_info(self, subject_id: str, condition: Literal[1,2,3,4]):
        self._subject_id = subject_id
        self._condition = condition

    def _load_data(self, feature_filename: str = None):
        self.file_path = os.path.join(self.data_path, 
                                      self._subject_id, 
                                      'condition_' + str(self._condition))

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
    


        