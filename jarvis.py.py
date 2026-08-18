import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import sys
import ctypes

# ----------------- CONFIGURAÇÃO DA VOZ — MICROSOFT DANIEL 🎙️ -----------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

print("🎤 Vozes encontradas no sistema:")
voz_encontrada = None
for i, v in enumerate(voices):
    print(f"  [{i}] {v.name}")
    # Procura pela voz em Português do Brasil (Microsoft Daniel)
    if 'Daniel' in v.name or 'Portuguese' in v.name or 'Brasil' in v.name or 'Brazil' in v.name:
        voz_encontrada = v.id

if voz_encontrada:
    engine.setProperty('voice', voz_encontrada)
    print("✅ Voz selecionada: Microsoft Daniel — Português (Brasil)")
else:
    # Se não encontrar, usa a primeira disponível
    engine.setProperty('voice', voices[0].id)
    print("⚠️ Usando a primeira voz disponível")

engine.setProperty('rate', 190)   # Velocidade da fala
engine.setProperty('volume', 1.0) # Volume máximo


def falar(texto):
    """Fala usando a voz do Windows — Microsoft Daniel!"""
    print(f"🗣️  Jarvis: {texto}")
    engine.say(texto)
    engine.runAndWait()


def cumprimentar():
    hora = datetime.datetime.now().hour
    if 0 <= hora < 12:
        falar("Bom dia! Estou pronto para as suas ordens.")
    elif 12 <= hora < 18:
        falar("Boa tarde! Sistema online, aguardando comandos.")
    else:
        falar("Boa noite! Jarvis ativado. Como posso ajudar?")


def ouvir():
    r = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("\n🎤 Ouvindo... (fale agora)")
        r.adjust_for_ambient_noise(fonte, duration=0.5)
        audio = r.listen(fonte)
    try:
        print("🔄 Processando...")
        comando = r.recognize_google(audio, language='pt-BR')
        print(f"👤 Você disse: {comando}\n")
        return comando.lower()
    except sr.UnknownValueError:
        falar("Desculpe, não entendi. Pode repetir?")
        return "nenhum"
    except sr.RequestError:
        print("⚠️ Sem conexão para reconhecimento de voz")
        return "erro"


def executar_comando(comando):
    # ⏰ HORA
    if 'que horas são' in comando or 'hora atual' in comando:
        agora = datetime.datetime.now().strftime('%H:%M')
        falar(f"Agora são {agora}")

    # 🌐 SITES
    elif 'abrir youtube' in comando:
        falar("Abrindo YouTube")
        webbrowser.open("youtube.com")
    elif 'abrir google' in comando:
        falar("Abrindo Google")
        webbrowser.open("google.com")
    elif 'abrir steam' in comando:
        falar("Abrindo Steam")
        os.startfile("C:\\Program Files (x86)\\Steam\\Steam.exe")
    elif 'abrir spotify' in comando or 'música' in comando:
        falar("Abrindo Spotify")
        webbrowser.open("open.spotify.com")

    # 📖 PESQUISA
    elif 'pesquise' in comando or 'procure' in comando:
        falar("Pesquisando...")
        termo = comando.replace('pesquise', '').replace('procure', '').strip()
        try:
            resultado = wikipedia.summary(termo, sentences=2)
            falar("Encontrei o seguinte:")
            print(f"📖 {resultado}")
            falar(resultado)
        except:
            falar("Não encontrei informações sobre isso.")

    # 🔒 SISTEMA
    elif 'bloqueia o pc' in comando or 'trava a tela' in comando:
        falar("Bloqueando o computador")
        ctypes.windll.user32.LockWorkStation()
    elif 'desligar' in comando or 'encerrar' in comando or 'sair' in comando:
        falar("Desativando sistemas. Até logo!")
        sys.exit()

    else:
        falar("Comando recebido, mas não sei como executar.")


# ====================== INÍCIO ======================
if __name__ == "__main__":
    print("="*50)
    print("🤖 JARVIS — Usando voz Microsoft Daniel!")
    print("="*50)
    cumprimentar()

    while True:
        comando = ouvir()
        if comando != "nenhum" and comando != "erro":
            executar_comando(comando)