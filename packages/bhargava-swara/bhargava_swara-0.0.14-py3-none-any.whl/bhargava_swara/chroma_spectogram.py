import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import os

def generate_chroma_spectrogram(audio_path, output_path, n_chroma=12, hop_length=512):
    """
    Generate a chroma spectrogram from an audio file and save it as a PNG.

    Args:
        audio_path (str): Path to the input audio file (.wav or .mp3).
        output_path (str): Path to save the output PNG file.
        n_chroma (int, optional): Number of chroma bins. Defaults to 12.
        hop_length (int, optional): Number of samples between successive frames. Defaults to 512.

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
        chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=n_chroma, hop_length=hop_length)

        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(12, 6))
        img = librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma', 
                                     hop_length=hop_length, ax=ax)
        fig.colorbar(img, ax=ax)

        ax.set_title('Chroma Spectrogram', fontsize=16)
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Chroma', fontsize=12)

        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close(fig)

        return output_path
    except Exception as e:
        raise Exception(f"Failed to generate chroma spectrogram: {str(e)}")