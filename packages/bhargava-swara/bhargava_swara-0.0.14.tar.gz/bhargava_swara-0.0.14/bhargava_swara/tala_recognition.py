from .raga_recognition import analyze_music_gemini

def extract_tala(analysis_result):
    """Extracts the Tala name from the Gemini response."""
    try:
        start_index = analysis_result.find("TALA :-")
        end_index = analysis_result.find("-------------", start_index)
        if start_index != -1 and end_index != -1:
            tala_part = analysis_result[start_index + 8:end_index].strip()
            return tala_part
        return "Unknown Tala"
    except Exception:
        return "Error extracting Tala"

def analyze_tala(audio_file_path, api_key=None):
    """Analyzes an audio file and returns the detected tala."""
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        analysis_result = analyze_music_gemini(audio_data, audio_file_path, api_key, "Tala")
        return extract_tala(analysis_result)
    except Exception as e:
        raise Exception(f"Failed to analyze tala: {str(e)}")