import speech_recognition as sr


def audio_to_text():
    """Record audio from the microphone and return the recognized text."""
    # Initialize recognizer and microphone
    # Use the default microphone as the audio source
    # Adjust the recognizer sensitivity to ambient noise
    # Listen for a single phrase and return the result as text

    # Initialize recognizer and microphone
    # Use the default microphone as the audio source
    # Adjust the recognizer sensitivity to ambient noise
    # Listen for a single phrase and return the result as text

    # Initialize recognizer and microphone
    # Use the default microphone as the audio source
    # Adjust the recognizer sensitivity to ambient noise
    # Listen for a single phrase and return the result as text

    mic = sr.Microphone()
    r = sr.Recognizer()

    with mic as source:
        print("Speak now to Gemini...")
        audio = r.listen(source, timeout=10)
    text = r.recognize_google(audio)

    print(f"Recognized text: {text}")
    return text
    