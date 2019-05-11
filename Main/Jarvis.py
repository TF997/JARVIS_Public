# pip install python-vlc
# pip install beautifulsoup4 | https://pypi.org/project/beautifulsoup4/
# pip install google | https://www.geeksforgeeks.org/performing-google-search-using-python-code/
# pip install pafy

import os
import vlc
import wave  
import time
import pafy
import wikipedia
from googlesearch import search
import math  


Instance = vlc.Instance()
player = Instance.media_player_new()
p = vlc.MediaPlayer(r"C:\Users\USER\Desktop\Jarvis\output.mp3")

def playback(Response):
    p.stop()
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=(r"Path\To\GoogleCred.json")
    from google.cloud import texttospeech


    client = texttospeech.TextToSpeechClient()


    synthesis_input = texttospeech.types.SynthesisInput(text=Response)

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-GB',
        name='en-GB-Wavenet-C',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)


    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)

    response = client.synthesize_speech(synthesis_input, voice, audio_config)

    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    p.play()
    print("Playback")

def SpeechInput():
    import speech_recognition as sr

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            return(text)
        except:
            print("Sorry could not recognize what you said")

def MusicSearch(MQ):
    try:
      QS = MQ
      QS = QS.split('play ',1)
      print(str(QS[1]))
      query = str(QS[1])
      print("I found these results: ")
      for Result in search(str(query), tld="co.uk", num=1, start=0, stop=1, pause=2):
        print("<" + Result + ">")
        url = Result
    except:
      print("I don't understand")

    try:
        video = pafy.new(url)
        best = video.getbest()
        playurl = best.url
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        playback("Playing" + query)
        player.play()
        time.sleep(3)
    except:
        playback("Sorry I could not find that")

def wikisearch(Query):
    if 'who is' in text:
        Query = Query.split('who is ',1)
    elif 'who' in text:
        Query = Query.split('who ',1)
    elif "what's" in text:
        Query = Query.split("what's",1)
        print(Query)
    elif 'what is' in text:
        Query = Query.split('what is ',1)
    elif 'what' in text:
        Query = Query.split('what ',1)
    elif 'wonder' in text:
        Query = Query.split('wonder ',1)

    equation = Query[1]
    print(equation)
    equation = calculationConverter(equation)

    try:
        playback(str(eval(equation)))
        return(0)
    except:
        print ("not an equation")

    try:
        msg = str(wikipedia.summary(str(Query[1]), chars = 350))
        msg = msg.replace("(listen);"," ")
        print(msg)
        playback(msg)
        time.sleep(3)
    except:
        playback("Sorry I could not find that")


def calculationConverter(equation):
        equationResult = ""
        equation = equation.replace("x","*")
        equation = equation.replace("add","+")
        equation = equation.replace("subtract","-")
        equation = equation.replace("takeaway","-")
        equation = equation.replace("^","**")
        if "the square root of" in equation or "√" in equation:
            equation = equation.replace("the square root of", "math.sqrt(")
            equation = equation.replace("√", "math.sqrt(")
            print(equation)
            equation = equation.split(" ")
            i = 0
            for i in range(len(equation)):
                print(equation[i])
                if equation[i].find("math.sqrt(") > -1:
                    equation[i+1] = equation[i+1].lstrip()
                    equation[i+1] = equation[i+1] + ")"
            equation = equationResult.join(equation)
            print(equation)
        return(equation)


while True:
    if player.is_playing() == False:
        player.stop()
    if player.is_playing() == True:
        print("Media Playing")

    print("Input:")
    text = ""
    text = SpeechInput() 
    if not text:
        print("Input:")
        text = ""
        text = SpeechInput()
    elif  "Jarvis" in text:
        if 'play' in text:
            MusicSearch(text)
        elif 'pause' in text:
            player.pause()
        elif 'resume' in text:
            player.play()
        elif 'stop' in text:
            playback("stopping")
            player.stop()
            p.stop()
        if "testing" in text:
            Response = "Test Successful."
            playback(Response)
            time.sleep(1) 
        if "who is" in text or "what is" in text or "who" in text or "what" in text or "wonder" in text:
           wikisearch(text)


    