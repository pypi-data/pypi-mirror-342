# bhargava_swara/synthesis.py
import numpy as np
import sounddevice as sd
from scipy.io import wavfile

def generate_tanpura_drone(pitch=261.63, duration=10, output_path=None, sr=44100):
    """
    Generate a tanpura drone with Sa-Pa-Sa-Pa pattern.
    
    Parameters:
    - pitch (float): Fundamental frequency of Sa (e.g., 261.63 Hz for C4).
    - duration (float): Duration of the drone in seconds.
    - output_path (str, optional): Path to save WAV file. If None, plays in real-time.
    - sr (int): Sample rate (default: 44100 Hz).
    
    Returns:
    - None: Plays audio or saves to file.
    """
    # Time array
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    
    # Fundamental (Sa) and harmonics
    sa1 = np.sin(2 * np.pi * pitch * t) * 0.5  # Fundamental
    sa1_harm = np.sin(2 * np.pi * (pitch * 2) * t) * 0.2  # First harmonic
    sa2 = np.sin(2 * np.pi * (pitch * 1.005) * t) * 0.4  # Slightly detuned Sa for shimmer
    
    # Pa (fifth, 3/2 * pitch)
    pa = np.sin(2 * np.pi * (pitch * 1.5) * t) * 0.3
    pa_harm = np.sin(2 * np.pi * (pitch * 3) * t) * 0.15
    
    # Combine waves (mimic Sa-Pa-Sa-Pa plucking)
    wave = sa1 + sa1_harm + sa2 + pa + pa_harm
    
    # Normalize to avoid clipping
    wave = wave / np.max(np.abs(wave)) * 0.8
    
    if output_path:
        # Save to WAV
        wavfile.write(output_path, sr, wave.astype(np.float32))
        print(f"Tanpura drone saved to {output_path}")
    else:
        # Play in real-time
        sd.play(wave, sr)
        sd.wait()
        print("Tanpura drone played successfully!")