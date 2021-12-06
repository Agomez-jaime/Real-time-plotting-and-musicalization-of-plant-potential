

import time

import brainflow
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardIds, BoardShim, BrainFlowInputParams
from brainflow.data_filter import AggOperations, DataFilter, FilterTypes


def scale_magnitude_array(x, ymin, ymax):
    x = np.array(x)
    return (x - ymin) / (ymax - ymin)


def board_2_df(data):
    # data = scale_magnitude_array(data, -396, 433)
    df = pd.DataFrame(data[:, [1, 22]], columns=["ECG", "TIME"])
    return df


class CytonBoard(object):
    def __init__(self, serial_port):
        self.params = BrainFlowInputParams()
        self.params.serial_port = serial_port
        self.board = BoardShim(BoardIds.CYTON_BOARD.value, self.params)


    def start_stream(self):
        self.board.prepare_session()
        self.board.start_stream()

    def stop_stream(self):
        self.board.stop_stream()
        self.board.release_session()

    def poll(self, sample_num):
        datos = []
        try:
            while self.board.get_board_data_count() < sample_num:
                time.sleep(0.02)
        except Exception as e:
            raise (e)
        self.count = self.board.get_board_data_count()
        board_data = self.board.get_board_data()
        for i in range(0, self.count - 1):
            recoger = np.zeros(2)
            recoger[0] = board_data[1][i]
            recoger[1] = board_data[2][i]
            datos.append(recoger)
        return datos

    def sampling_frequency(self):
        sampling_freq = self.board.get_sampling_rate(BoardIds.CYTON_BOARD.value)
        return sampling_freq

    def canales(self):
        return BoardShim.get_eeg_channels(BoardIds.CYTON_BOARD.value)

    def data(self):
        return self.board_data


