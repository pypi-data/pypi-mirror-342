import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_cqt_spectrogram(audio_path, output_path, hop_length=512, n_bins=84):
    """
    Generate a CQT spectrogram from an audio file and save it as a PNG.

    Args:
        audio_path (str): Path to the input audio file (.wav or .mp3).
        output_path (str): Path to save the output PNG file.
        hop_length (int, optional): Number of samples between successive frames. Defaults to 512.
        n_bins (int, optional): Number of frequency bins. Defaults to 84.

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
        C = np.abs(librosa.cqt(y, sr=sr, hop_length=hop_length, n_bins=n_bins))
        C_db = librosa.amplitude_to_db(C, ref=np.max)

        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(12, 6))
        img = librosa.display.specshow(C_db, sr=sr, x_axis='time', y_axis='cqt_note', 
                                     hop_length=hop_length, ax=ax)
        fig.colorbar(img, ax=ax, format='%+2.0f dB')

        ax.set_title('CQT Spectrogram', fontsize=16)
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Note', fontsize=12)

        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return output_path
    except Exception as e:
        raise Exception(f"Failed to generate CQT spectrogram: {str(e)}")