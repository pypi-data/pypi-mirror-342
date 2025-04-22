# built-in
import os

# third-party
import mne

# local
from .visualization import plot_channels


class BipolarExplorer:

    def __init__(self, filepath):
        self.filepath = filepath
        data = read_mne_file(filepath)
        self.data = data.copy().pick(['ecg', 'eeg'])

    def list_channels(self):
        ''' Lists all channels that are not EEG (or at least labeled using the conventional 10-20 system).

        Parameters
        ---------- 

        Returns
        -------
        available_channels : list
            List of strings corresponding to the channels available.
        '''
        eeg_channels = [
            "eeg",
            "fp1", "fp2",
            "f7", "f3", "fz", "f4", "f8",
            "t3", "c3", "cz", "c4", "t4",
            "t5", "p3", "pz", "p4", "t6",
            "o1", "o2",
        ]
        available_channels = [ch for ch in self.data.info.ch_names if not any(
            substring in ch.lower() for substring in eeg_channels)]
        return available_channels

    def explore(self, bipolar_chn_name='Bipolar ECG', extra_ui_info=['id']):
        ''' Function description 

        Parameters
        ---------- 
        bipolar_chn_name : str
            Name to give the bipolar channel that will be created.
        extra_ui_info : list
            List of strings, corresponding to extra info that the user should input for each file.

        Returns
        -------
        ui_channels : str
            Names of the chosen channels, in the format "ch1,chn2". 
        *ui_replies : str
            Variable number of outputs, with the same length as extra_ui_info.
        '''

        try:
            ui_channels = self._get_channels_ui(bipolar_chn_name)
            ui_replies = []
            for ui_info in extra_ui_info:
                ui_replies = self._get_extra_ui_info(ui_info, self.filepath)

        except UnicodeDecodeError:
            return None, *([None]*len(extra_ui_info))

        return ui_channels, *ui_replies

    def _get_channels_ui(self, bipolar_chn_name):
        ''' From all available channels that are not EEG (or at least labeled using the conventional 10-20 system), visualize in real time to choose a bipolar configuration. A terminal input will allow for the choice of channels. Input is case- and spacing-sensitive and should be in the format ch1,chn2. Trailing spaces do not matter (i.e. ch1,    chn2).  

        Parameters
        ---------- 
        data : mne.io.Raw
            Instance of mne.io.Raw. Should contain at least 2 channels (unipolar).
        bipolar_chn_name : str
            Name to give the bipolar channel that will be created.

        Returns
        -------
        ui_channels : str
            String in the format 
        '''

        available_channels = self.list_channels()
        ui_channels = input(
            f'Choose 2 channels from {available_channels}\nch1,ch2: ')

        user_has_chosen = False
        while not user_has_chosen:
            ecg_data = get_bipolar_montage(
                self.data, channels=[ch.strip() for ch in ui_channels.split(',')], new_ch_name=bipolar_chn_name, resample_freq=None)
            plot_channels(ecg_data, channels=[
                bipolar_chn_name], datetime_as_index=True)

            ui = input(
                f'Are {ui_channels} the correct channels?\n(Y/N/NA/*): ')

            user_has_chosen = ui == 'Y'

            if ui == 'NA'.strip() or ui == '*':
                return ui.strip()
            elif not user_has_chosen:
                ui_channels = input(
                    f'Choose 2 channels from {available_channels}\nch1,ch2: ')

        return ui_channels

    def _get_extra_ui_info(self, ui_info, filename):
        ''' Function description 

        Parameters
        ---------- 
        param1 : int
            Description

        Returns
        -------
        result : bool
            Description
        '''
        ui_id = input(f'Set patient {ui_info} for file {filename}\n: ')
        if len(ui_id) == 0:
            ui_id = None
        return ui_id


# def read_data(filepath, bipolar_chn_name='Bipolar ECG'):
#     ''' Read a .EDF of .EEG file, extract all available channels, and deploy UI to visualize the chosen bipolar montages in real time. The result is a string in the format ch1, ch2 with the chosen anode and cathode (bipolar montage) or NA / * which can be used when no satisfactory channel combination was found. Optionally, a personalized ID for the file/subject can also be chosen.

#     Parameters
#     ----------
#     filepath : str
#         Path to the .EDF or .EEG file. containing the data
#     bipolar_chn_name : str
#         Name to give the bipolar channel that will be created.

#     Returns
#     -------
#     ui_channels : str
#         Names of the chosen channels, in the format "ch1,chn2".
#     ui_id : str
#         Chosen ID for the file/subject.
#     '''

#     try:
#         data = read_mne_file(filepath)
#         data = data.copy().pick(['ecg', 'eeg'])

#         ui_channels = _get_channels_ui(data, bipolar_chn_name)
#         ui_id = _get_id_ui(filepath)

#     except UnicodeDecodeError:
#         return None

#     return ui_channels, ui_id


def read_mne_file(filepath):
    ''' Load data instance of mne.io.Raw from a .edf or .EEG file using the MNE package.

    Parameters
    ----------
    filepath : str
        Path to the file to be loaded.

    Returns
    -------
    result : mne.io.Raw
        Instance of mne.io.Raw.

    Raises
    ------
    ValueError :
        Raised when the file extension is not supported.
    '''

    _, file_extension = os.path.splitext(filepath)

    if file_extension.lower() == '.edf':
        data = mne.io.read_raw_edf(filepath, encoding='latin1')
    elif file_extension.lower() == '.eeg':
        data = mne.io.read_raw_nihon(filepath)
    else:
        raise ValueError('File extension not supported.')

    return data


def get_bipolar_montage(data, channels, new_ch_name, resample_freq=None):
    ''' From 2 channels, create a new channel with the bipolar montage.  

    Parameters
    ---------- 
    data : mne.io.Raw
        Instance of mne.io.Raw. Should contain at least 2 channels (unipolar).
    channels : list
        List containing the names of the two channels [anode, cathode]. The bipolar reference takes the difference between two channels (the anode minus the cathode).
    resample_freq : int64
        New sampling frequency. 

    Returns
    -------
    result : mne.io.Raw
        Instance of mne.io.Raw with a single channel called "Bipolar ECG". 
    '''
    data = data.copy().pick(channels)
    data = data.load_data()

    bipolar = mne.set_bipolar_reference(
        data, anode=channels[0], cathode=channels[1], ch_name=new_ch_name, drop_refs=True)

    if resample_freq != None:
        bipolar = bipolar.copy().resample(sfreq=resample_freq)

    return bipolar
