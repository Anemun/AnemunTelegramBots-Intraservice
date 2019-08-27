import speech_recognition as sr

def recognize(data):

    r = sr.Recognizer()
    with sr.AudioFile(data) as source:
        audio = r.record(source)

    try:
        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

    result = ""
    return result