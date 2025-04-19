import google.generativeai as genai

def configure_api_key(api_key):
    """Configures the Gemini API key."""
    genai.configure(api_key=api_key)

def analyze_music_gemini(audio_data, file_name, api_key=None, element="Raga"):
    """Analyzes music and returns analysis result for a specified element."""
    if api_key:
        configure_api_key(api_key)
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")

        prompt_text = f"""
        Analyze the musical characteristics of the audio.
        Assume this audio is Indian classical music.
        Identify and extract the following musical element:
        - {element}

        Output the extracted details in the following format:

        -------------------
        EXTRACTED DETAILS

        {element.upper()} :- [{element} Name]
        -------------
        """

        mime_type = "audio/mpeg" if file_name.lower().endswith(".mp3") else "audio/wav"
        contents = [{
            "parts": [
                {"text": prompt_text},
                {"inline_data": {"data": audio_data, "mime_type": mime_type}}
            ]
        }]

        generate_content_config = {
            "temperature": 0.0,
            "top_p": 0.9,
            "top_k": 32,
            "max_output_tokens": 2048,
        }
        safety_settings = [{"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}]

        response = model.generate_content(
            contents=contents,
            generation_config=generate_content_config,
            safety_settings=safety_settings
        )
        return response.text

    except Exception as e:
        raise Exception(f"Error during analysis: {str(e)}")

def extract_raga(analysis_result):
    """Extracts the Raga name from the Gemini response."""
    try:
        start_index = analysis_result.find("RAGA :-")
        end_index = analysis_result.find("-------------", start_index)
        if start_index != -1 and end_index != -1:
            raga_part = analysis_result[start_index + 8:end_index].strip()
            return raga_part
        return "Unknown Raga"
    except Exception:
        return "Error extracting Raga"

def analyze_raga(audio_file_path, api_key=None):
    """Analyzes an audio file and returns the detected raga."""
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        analysis_result = analyze_music_gemini(audio_data, audio_file_path, api_key, "Raga")
        return extract_raga(analysis_result)
    except Exception as e:
        raise Exception(f"Failed to analyze raga: {str(e)}")