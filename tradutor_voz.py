import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from openai import OpenAI
from gtts import gTTS
import pygame


def gravar_audio(nome_arquivo="input_audio.wav", duracao=5, fs=44100):
    print("Gravando...")
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1)
    sd.wait()
    write(nome_arquivo, fs, audio)
    print(f"Áudio salvo em {nome_arquivo}")
    return nome_arquivo


def transcrever_audio(nome_arquivo, idioma="pt"):
    model = whisper.load_model("small")
    result = model.transcribe(nome_arquivo, fp16=False, language=idioma)
    texto = result["text"]
    print("Transcrição:", texto)
    return texto


def traduzir_texto(texto, destino="en"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Você é um tradutor de português para {destino}."},
            {"role": "user", "content": texto}
        ]
    )
    traducao = response.choices[0].message.content
    print("Tradução:", traducao)
    return traducao


def falar_texto(texto, idioma="en", nome_arquivo="translation_audio.mp3"):
    tts = gTTS(text=texto, lang=idioma)
    tts.save(nome_arquivo)
    print("Reproduzindo tradução...")
    pygame.mixer.init()
    pygame.mixer.music.load(nome_arquivo)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def main():
    arquivo = gravar_audio(duracao=5)
    texto_pt = transcrever_audio(arquivo, idioma="pt")
    texto_en = traduzir_texto(texto_pt, destino="en")
    falar_texto(texto_en, idioma="en")


if __name__ == "__main__":
    main()
