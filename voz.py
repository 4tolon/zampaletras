import speech_recognition as sr

r = sr.Recognizer()
for i in range(30):
    try:
        with sr.Microphone() as source:
            print("Expresa algo")
#            audio = r.listen(source)
            audioa = r.record(source, duration=2)
            print("Grabación terminada. Procesando...")
            texto = r.recognize_google(audioa,language = 'es')
            texto = str.lower(texto)
        print(texto, i)
    except: 
        continue

f = open ('texto_dictado.txt','w')
f.write(texto)
f.close()
