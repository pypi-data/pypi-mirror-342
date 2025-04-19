from .raga_recognition import analyze_music_gemini

def extract_ornaments(analysis_result):
    """Extracts ornamentation details from the Gemini response."""
    try:
        start_index = analysis_result.find("ORNAMENTS :-")
        end_index = analysis_result.find("-------------", start_index)
        if start_index != -1 and end_index != -1:
            ornaments_part = analysis_result[start_index + 13:end_index].strip()
            return ornaments_part
        return "Unknown Ornamentation"
    except Exception:
        return "Error extracting Ornamentation"

def analyze_ornaments(audio_file_path, api_key=None):
    """Analyzes an audio file and returns detected ornamentation details."""
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        prompt = "Ornaments (Are ornaments present? YES/NO. If YES, try to name a few prominent ones if possible)"
        analysis_result = analyze_music_gemini(audio_data, audio_file_path, api_key, prompt)
        return extract_ornaments(analysis_result)
    except Exception as e:
        raise Exception(f"Failed to analyze ornaments: {str(e)}")