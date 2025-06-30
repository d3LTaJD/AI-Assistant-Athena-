import os
import pygame

def speak(text):
    voice = 'en-US-AvaNeural'
    speed = "+30%"
    #   name                   country languag                 
    
    # en-US-AvaNeural          1 usa english                       
    # en-US-AnaNeural          usa kid english                   
    # en-GB-LibbyNeural        1 british english    
    # en-GB-MaisieNeural       3 british kids english             
    # en-IE-EmilyNeural        ireland english                     
    # en-IN-NeerjaNeural       indian english                     
    # gu-IN-DhwaniNeural       gujarati                            
    # hi-IN-SwaraNeural        hindi
    # kn-IN-SapnaNeural        karnataka
    # ml-IN-SobhanaNeural      malyalam
    # mr-IN-AarohiNeural       marathi
    # ta-IN-PallaviNeural      tamil
    # te-IN-ShrutiNeural       telegu
    # ur-IN-GulNeural          urdu
    # bn-IN-TanishaaNeural     bengali
    chunks = text.split()
    chunk_size = 100
    chunks = [chunks[i:i + chunk_size]for i in range(0,len(chunks),chunk_size)]   
    for chunk in chunks:
        text= ' '.join(chunk)
        data = f'python -m edge_tts --voice "{voice}" --text "{text}" --rate={speed} --write-media "hello.mp3"'
        os.system(data)
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("hello.mp3")
        try:
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(e)
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()   
    return True




# edge-tts --text "Hello, world!" --write-media hello.mp3 --write-subtitles hello.vtt
