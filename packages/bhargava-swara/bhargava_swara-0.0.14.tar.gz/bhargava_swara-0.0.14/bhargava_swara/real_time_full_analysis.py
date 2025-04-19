import google.generativeai as genai

def configure_api_key(api_key):
    """Configures the Gemini API key."""
    genai.configure(api_key=api_key)

def analyze_music_full_gemini(audio_data, file_name, api_key=None):
    """Performs a full analysis of Indian classical music."""
    if api_key:
        configure_api_key(api_key)
    
    try:
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")

        prompt_text = """
        Analyze the audio provided.

        Instructions:
        1. **Initial Identification:** Begin by attempting to classify the audio as Indian classical music (Hindustani or Carnatic tradition).
        2. **If Identified as Indian Classical:**
            * Identify and extract the following musical elements to the best of your ability:
                * MUSIC TRADITION (Hindustani or Carnatic)
                * RAGA (Identify the Raga name, focusing on common and fundamental Ragas. If the Raga is a variation or less common, clearly state that it's a variation and name the closest recognized Raga.)
                * THALA (Identify the Thala name, focusing on core and well-known Thalas. If the Thala is a variation, mention the closest recognized Thala.)
                * TEMPO (Describe the Tempo using appropriate terms like Vilambit, Madhya, Drut, or slow, medium, fast).
                * ORNAMENTS (Determine if ornaments are present (YES/NO). If YES, list prominent ornament names like Gamaka, Meend, etc.)
            * **Deviation Analysis and Corrections:**
                * If any element (Raga, Thala) deviates from a standard or recognized form, provide specific suggestions to correct the deviation and bring it closer to a standard performance.
            * **Output Format:**
                -------------------
                EXTRACTED DETAILS

                MUSIC TRADITION :- [Tradition, or "Not Indian Classical Music" if applicable]
                instruments:- [List instruments heard]
                mood:- [Describe the overall mood]
                RAGA :- [Raga Name, or "Unidentifiable" if unable to determine]
                THALA :- [Thala Name, or "Unidentifiable" if unable to determine]
                TEMPO :- [Tempo description]
                ORNAMENTS :- [YES/NO]
                [If YES, list ornament names: ...]
                Correction:- [Specific correction suggestions, or "None" if no deviations]
                Other information:- [if any]
                -------------
        3. **If NOT Identified as Indian Classical Music:**
            * Describe the sonic characteristics of the audio as accurately as possible.
            * Set MUSIC TRADITION to "Not Indian Classical Music"
            * Set RAGA and THALA to "Unidentifiable".
            * Populate the "Other information" field with your description.
        4. Try to avoid default answers, be honest.
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
            "top_p": 0.1,
            "top_k": 1,
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
        raise Exception(f"Error during full analysis: {str(e)}")

def extract_details(analysis_result):
    """Extracts detailed analysis from the Gemini response."""
    try:
        start_index = analysis_result.find("EXTRACTED DETAILS")
        end_index = analysis_result.find("-------------", start_index)
        if start_index != -1 and end_index != -1:
            details_part = analysis_result[start_index:end_index].strip()
            return details_part
        return "No Details Detected"
    except Exception:
        return "Error extracting details"

def analyze_music_full(audio_file_path, api_key=None):
    """Analyzes an audio file and returns a full music analysis."""
    try:
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()
        analysis_result = analyze_music_full_gemini(audio_data, audio_file_path, api_key)
        return extract_details(analysis_result)
    except Exception as e:
        raise Exception(f"Failed to perform full analysis: {str(e)}")