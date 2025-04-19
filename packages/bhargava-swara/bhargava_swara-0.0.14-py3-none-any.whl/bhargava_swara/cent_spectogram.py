import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_cent_spectrogram(audio_path, output_path, n_filters=128, fmax=8000):
    """
    Generate a cent filterbank spectrogram from an audio file and save it as a PNG.

    Args:
        audio_path (str): Path to the input audio file (.wav or .mp3).
        output_path (str): Path to save the output PNG file.
        n_filters (int, optional): Number of filters in the filterbank. Defaults to 128.
        fmax (int, optional): Maximum frequency. Defaults to 8000 Hz.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        Exception: If spectrogram generation fails.
    """
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        y, sr = librosa.load(audio_path, sr=None)
        # Using triangular filterbank with cent scale
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_filters, fmax=fmax)
        S_db = librosa.power_to_db(S, ref=np.max)

        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(12, 6))
        img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', 
                                     fmax=fmax, ax=ax)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')

        ax.set_title('Cent Filterbank Spectrogram', fontsize=16)
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Frequency (Hz)', fontsize=12)

        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return output_path
    except Exception as e:
        raise Exception(f"Failed to generate cent spectrogram: {str(e)}")