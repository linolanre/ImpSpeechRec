import streamlit as st
import speech_recognition as sr
import pyaudio

# Define global variables
text = ""
paused = False

def transcribe_speech(api, language):
    global text, paused  # Use the global variables
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        while True:
            if not paused:
                try:
                    audio = r.listen(source)
                    st.write("Transcribing...")
                    if api == "Google":
                        text = r.recognize_google(audio, language=language)
                    elif api == "Microsoft":
                        text = r.recognize_azure(audio, language=language)
                    elif api == "IBM":
                        text = r.recognize_ibm(audio, language=language)
                    elif api == "Wit":
                        text = r.recognize_wit(audio, language=language)
                    else:
                        raise ValueError("Invalid speech recognition API selected.")
                    
                    st.write("Transcription:", text)
                except sr.UnknownValueError:
                    st.write("Error: Unable to transcribe speech.")
                except sr.RequestError as e:
                    st.write("Error: Could not connect to the speech recognition service.")
                    st.write(e)
            else:
                st.write("Transcription paused.")
                break

def save_transcription():
    global text  # Use the global variable
    filename = st.text_input("Enter the filename to save the transcription to")
    if st.button("Save Transcription") and text:
        with open(filename, "w") as file:
            file.write(text)
        st.write("Transcription saved to", filename)

# Streamlit app
st.title("Speech Transcription App By LinoLanre")
st.sidebar.image('unnamed.png')

api = st.selectbox("Select speech recognition API", ("Google", "Microsoft", "IBM", "Wit"))
language = st.text_input("Enter the language you are speaking in")
# PyAudio initialization
p = pyaudio.PyAudio()

if st.sidebar.button("Start Transcription"):
    paused = False
    transcribe_speech(api, language)

if st.sidebar.button("Pause Transcription"):
    paused = True

if st.sidebar.button("Resume Transcription"):
    paused = False

save_transcription()