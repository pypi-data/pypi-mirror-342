from .raga_recognition import analyze_music_gemini

def extract_tempo(analysis_result):
    """Extracts the tempo from the Gemini response."""
    try:
        start_index = analysis_result.find("TEMPO :-")
        end_index = analysis_result.find("-------------", start_index)
        if start_index != -1 and end_index != -1:
            tempo_part = analysis_result[start_index + 9:end_index].strip()
            return tempo_part
        return "Unknown Tempo"
    except Exception:
        return "Error extracting Tempo"

def analyze_tempo(audio_file_path, api_key=None):
    """Analyzes an audio file and returns the detected tempo."""
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        analysis_result = analyze_music_gemini(audio_data, audio_file_path, api_key, "Tempo")
        return extract_tempo(analysis_result)
    except Exception as e:
        raise Exception(f"Failed to analyze tempo: {str(e)}")