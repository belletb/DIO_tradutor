import os
import sys
import atexit
import tempfile
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
from gtts import gTTS
import pygame


DEFAULT_RECORDING_DURATION = 5
SOURCE_LANGUAGE = "pt"
TARGET_LANGUAGE = "en"
WHISPER_MODEL_SIZE = "small"
SAMPLE_RATE = 44100

WHISPER_MODEL = None
temp_files = []


def cleanup_files():
    for filepath in temp_files:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass


atexit.register(cleanup_files)


def get_whisper_model():
    """Load Whisper model once and cache it."""
    global WHISPER_MODEL
    if WHISPER_MODEL is None:
        try:
            print(f"Carregando modelo Whisper ({WHISPER_MODEL_SIZE})...")
            WHISPER_MODEL = whisper.load_model(WHISPER_MODEL_SIZE)
            print("Modelo carregado com sucesso!")
        except Exception as e:
            print(f"ERRO ao carregar modelo Whisper: {e}")
            sys.exit(1)
    return WHISPER_MODEL


def validate_audio_devices():
    """Validate audio device availability."""
    try:
        devices = sd.query_devices()
        if not devices:
            print("ERRO: Nenhum dispositivo de áudio encontrado!")
            return False
        return True
    except Exception as e:
        print(f"ERRO ao verificar dispositivos de áudio: {e}")
        return False


def gravar_audio(duracao=DEFAULT_RECORDING_DURATION, fs=SAMPLE_RATE):
    """Record audio from microphone."""
    try:
        temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        temp_filename = temp_file.name
        temp_file.close()
        temp_files.append(temp_filename)
        
        print(f"\n🎤 Gravando por {duracao} segundos... FALE AGORA!")
        audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        write(temp_filename, fs, audio)
        print(f"✓ Áudio gravado com sucesso")
        return temp_filename
        
    except Exception as e:
        print(f"ERRO ao gravar áudio: {e}")
        return None


def transcrever_e_traduzir_audio(nome_arquivo):
    """
    Transcribe and translate audio using Whisper's built-in translation.
    
    Whisper can directly translate from any language to English!
    This is FREE and doesn't require OpenAI API.
    """
    try:
        if not os.path.exists(nome_arquivo):
            print(f"ERRO: Arquivo {nome_arquivo} não encontrado")
            return None, None
        
        model = get_whisper_model()
        
        # Transcribe in original language
        print("📝 Transcrevendo áudio...")
        transcription = model.transcribe(nome_arquivo, fp16=False, language=SOURCE_LANGUAGE)
        texto_original = transcription["text"].strip()
        
        if not texto_original:
            print("⚠️  Nenhum texto detectado no áudio")
            return None, None
        
        print(f"✓ Transcrição (PT): '{texto_original}'")
        
        # Translate using Whisper (FREE!)
        print("🌐 Traduzindo com Whisper...")
        translation = model.transcribe(nome_arquivo, fp16=False, task="translate")
        texto_traduzido = translation["text"].strip()
        
        print(f"✓ Tradução (EN): '{texto_traduzido}'")
        return texto_original, texto_traduzido
        
    except Exception as e:
        print(f"ERRO ao processar áudio: {e}")
        return None, None


def falar_texto(texto, idioma=TARGET_LANGUAGE):
    """Convert text to speech and play it."""
    try:
        if not texto or not texto.strip():
            print("ERRO: Texto vazio para sintetizar")
            return False
        
        temp_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_filename = temp_file.name
        temp_file.close()
        temp_files.append(temp_filename)
        
        print("🔊 Gerando e reproduzindo áudio...")
        tts = gTTS(text=texto, lang=idioma, slow=False)
        tts.save(temp_filename)
        
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        
        print("✓ Áudio reproduzido com sucesso")
        return True
        
    except Exception as e:
        print(f"ERRO ao reproduzir áudio: {e}")
        return False


def processar_traducao(duracao=DEFAULT_RECORDING_DURATION):
    """Execute the complete translation pipeline."""
    arquivo = gravar_audio(duracao=duracao)
    if not arquivo:
        return False
    
    texto_pt, texto_en = transcrever_e_traduzir_audio(arquivo)
    if not texto_en:
        return False
    
    success = falar_texto(texto_en)
    return success


def main():
    """Main function with interactive loop."""
    print("=" * 60)
    print("🌍 TRADUTOR DE VOZ GRATUITO (PT → EN)")
    print("💡 Usando apenas Whisper - SEM necessidade de API OpenAI!")
    print("=" * 60)
    
    if not validate_audio_devices():
        sys.exit(1)
    
    get_whisper_model()
    
    print("\n📋 Instruções:")
    print(f"  • Pressione ENTER para iniciar gravação ({DEFAULT_RECORDING_DURATION}s)")
    print("  • Fale claramente em português durante a gravação")
    print("  • Pressione Ctrl+C para sair\n")
    
    traducoes_realizadas = 0
    
    try:
        while True:
            print("-" * 60)
            user_input = input("⏎  Pressione ENTER para começar (ou 'q' para sair)...")
            
            if user_input.lower() == 'q':
                break
            
            if processar_traducao():
                traducoes_realizadas += 1
                print(f"\n✅ Tradução #{traducoes_realizadas} concluída!")
            else:
                print("\n❌ Tradução falhou. Tente novamente.")
            
            print()
    
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando tradutor...")
        print(f"📊 Total de traduções: {traducoes_realizadas}")
        print("Até logo!")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
