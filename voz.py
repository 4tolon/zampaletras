import speech_recognition as sr

r = sr.Recognizer()

with sr.Microphone() as source:
    print("Expresa algo")
    #audio = r.listen(source)
    audioa = r.record(source, duration=2)
    print("Grabación terminada. Procesando...")
    texto = r.recognize_google(audioa,language = 'es_ES')
    texto = str.lower(texto)
print(texto)

f = open ('texto_dictado.txt','w')
f.write(texto)
f.close()