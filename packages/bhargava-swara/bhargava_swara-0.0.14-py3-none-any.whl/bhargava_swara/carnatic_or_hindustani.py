from .raga_recognition import analyze_music_gemini

def extract_tradition(analysis_result):
    """Extracts the music tradition from the Gemini response."""
    try:
        start_index = analysis_result.find("MUSIC TRADITION :-")
        end_index = analysis_result.find("-------------", start_index)
        if start_index != -1 and end_index != -1:
            tradition_part = analysis_result[start_index + 18:end_index].strip()
            return tradition_part
        return "Unknown Tradition"
    except Exception:
        return "Error extracting Tradition"

def analyze_tradition(audio_file_path, api_key=None):
    """Analyzes an audio file and returns the detected music tradition (Hindustani/Carnatic)."""
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        analysis_result = analyze_music_gemini(audio_data, audio_file_path, api_key, "Music Tradition (Hindustani or Carnatic)")
        return extract_tradition(analysis_result)
    except Exception as e:
        raise Exception(f"Failed to analyze tradition: {str(e)}")