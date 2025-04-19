import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_mel_spectrogram(audio_path, output_path, n_mels=128, fmax=8000):
    """
    Generate a mel-frequency spectrogram from an audio file and save it as a PNG.

    Args:
        audio_path (str): Path to the input audio file (.wav or .mp3).
        output_path (str): Path to save the output PNG file.
        n_mels (int, optional): Number of mel bands. Defaults to 128.
        fmax (int, optional): Maximum frequency. Defaults to 8000 Hz.

    Raises:
        FileNotFoundError: If the audio file does not exist.
        Exception: If spectrogram generation fails.
    """
    # Validate audio file
    if not os.path.isfile(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        # Load the audio file while preserving its original sampling rate
        y, sr = librosa.load(audio_path, sr=None)

        # Compute the mel spectrogram and convert to decibel units
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=n_mels, fmax=fmax)
        S_db = librosa.power_to_db(S, ref=np.max)

        # Use a built-in Matplotlib style
        plt.style.use('ggplot')  # Changed from 'seaborn-darkgrid'
        fig, ax = plt.subplots(figsize=(12, 6))
        img = librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='mel', fmax=fmax, ax=ax)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')

        # Set plot title and labels
        ax.set_title('Mel-frequency Spectrogram', fontsize=16)
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Frequency (Hz)', fontsize=12)

        # Save the plot as a PNG file with high resolution (300 dpi)
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return output_path
    except Exception as e:
        raise Exception(f"Failed to generate mel spectrogram: {str(e)}")