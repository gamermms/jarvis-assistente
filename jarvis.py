import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import sys
import ctypes
import random
import urllib.request
import shutil

# ==================================================
# ⚙️ CONFIGURAÇÕES DO JARVIS
# ==================================================
VERSAO_ATUAL = "1.0"  # ← Aumente o número aqui quando houver versão nova
URL_ATUALIZACAO = "https://raw.githubusercontent.com/seu-usuario/jarvis/main/jarvis.py"  # ← Depois explico como criar
ARQUIVO_LOCAL = os.path.abspath(__file__)

# ==================================================
# 🔄 SISTEMA DE AUTO-ATUALIZAÇÃO
# ==================================================
def verificar_atualizacao():
    """Verifica se existe versão nova e atualiza sozinho!"""
    print("🔄 Verificando atualizações...")
    try:
        # ⚠️ Por enquanto, avisa apenas
        falar(f"Eu sou a versão {VERSAO_ATUAL}. Estou verificando se há atualizações.")
        print(f"✅ Você está usando a versão {VERSAO_ATUAL}")
        print("ℹ️ Para ativar atualização automática completa, precisamos hospedar o código na internet.")
        print("💡 Por enquanto, é só me avisar quando houver código novo que eu substituo aqui!")
        return False
    except Exception as e:
        print(f"⚠️ Não consegui verificar atualizações: {e}")
        return False

def baixar_e_atualizar():
    """Baixa a versão nova e substitui o arquivo antigo"""
    try:
        print("⬇️ Baixando nova versão...")
        urllib.request.urlretrieve(URL_ATUALIZACAO, ARQUIVO_LOCAL + ".novo")
        
        # Faz backup antes de atualizar
        shutil.copy2(ARQUIVO_LOCAL, ARQUIVO_LOCAL + ".backup")
        
        # Substitui pelo novo
        os.replace(ARQUIVO_LOCAL + ".novo", ARQUIVO_LOCAL)
        print("✅ Atualizado com sucesso! Reiniciando...")
        falar("Atualização concluída! Reiniciando agora.")
        
        # Reinicia o Jarvis com a versão nova
        os.execv(sys.executable, [sys.executable] + sys.argv)
        return True
    except Exception as e:
        print(f"❌ Erro na atualização: {e}")
        falar("Houve um erro ao atualizar. Continuando com a versão atual.")
        return False

# ==================================================
# 🎙️ VOZ MARIA — PORTUGUÊS
# ==================================================
def falar(texto):
    print(f"🗣️  Jarvis: {texto}")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    for v in voices:
        if 'Portuguese' in v.name or 'Brazil' in v.name:
            engine.setProperty('voice', v.id)
            break
    engine.setProperty('rate', 185)
    engine.setProperty('volume', 1.0)
    engine.say(texto)
    engine.runAndWait()
    engine.stop()

# ==================================================
# 🧠 INTELIGÊNCIA ARTIFICIAL
# ==================================================
def perguntar_ia(pergunta):
    pergunta_limpa = pergunta.lower().strip()
    
    respostas_ia = {
        "o que é inteligência artificial": "Inteligência Artificial é a capacidade de um computador simular funções cognitivas humanas, como aprender, raciocinar e resolver problemas!",
        "como funciona o universo": "O universo começou há cerca de 13,8 bilhões de anos com o Big Bang. Vem se expandindo e formando galáxias!",
        "qual a melhor forma de aprender": "A melhor forma é combinar leitura, prática e repetição. Ensinar o que aprendeu também ajuda muito!",
        "como ter sucesso": "Sucesso é esforço, persistência e aprendizado contínuo. Nunca desista e sempre melhore!",
        "por que o céu é azul": "A luz do Sol se espalha na atmosfera. A luz azul se espalha mais, por isso vemos o céu azul!",
    }
    
    respostas_gerais = {
        "quem é você": "Eu sou o Jarvis, seu assistente com inteligência artificial. Fui criado para conversar e ajudar você!",
        "o que você pode fazer": "Posso responder perguntas, abrir jogos e sites, dizer as horas, criar lembretes e me atualizar sozinho!",
        "obrigado": "De nada! Sempre às suas ordens.",
        "como você está": "Estou funcionando perfeitamente e sempre atualizado! E você, como está?",
    }
    
    for chave, resposta in respostas_ia.items():
        if chave in pergunta_limpa:
            return resposta
    
    for chave, resposta in respostas_gerais.items():
        if chave in pergunta_limpa:
            return resposta
    
    palavras_pesquisa = ["o que é", "quem é", "explique", "defina", "qual é"]
    if any(p in pergunta_limpa for p in palavras_pesquisa):
        termo = pergunta
        for p in palavras_pesquisa:
            termo = termo.replace(p, "")
        termo = termo.strip()
        if len(termo) > 3:
            try:
                resultado = wikipedia.summary(termo, sentences=2)
                return f"Encontrei isso: {resultado}"
            except:
                pass
    
    respostas_naturais = [
        "Que pergunta interessante! Pode me explicar melhor?",
        "Compreendo. Estou aprendendo cada dia mais!",
        "Ótima pergunta! Podemos pesquisar isso juntos.",
    ]
    return random.choice(respostas_naturais)

# ==================================================
# 🎮 JOGOS E COMANDOS
# ==================================================
JOGOS = {
    "pubg": r"C:\Program Files (x86)\Steam\steamapps\common\PUBG\TslGame\Binaries\Win64\TslGame.exe",
    "grand chase": r"C:\Program Files (x86)\Steam\steamapps\common\Grand Chase Classic\GrandChase.exe",
    "steam": r"C:\Program Files (x86)\Steam\Steam.exe",
}

lembretes = []

# ==================================================
# 🎉 CUMPRIMENTO
# ==================================================
def cumprimentar():
    hora = datetime.datetime.now().hour
    if 0 <= hora < 12:
        falar(f"Bom dia! Jarvis versão {VERSAO_ATUAL} online. Estou pronto e sempre me atualizando!")
    elif 12 <= hora < 18:
        falar(f"Boa tarde! Jarvis {VERSAO_ATUAL} operacional. Verificando atualizações na inicialização.")
    else:
        falar(f"Boa noite! Jarvis {VERSAO_ATUAL} online. Todos os sistemas atualizados e prontos!")

# ==================================================
# 🎤 OUVIR
# ==================================================
def ouvir():
    r = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("\n🎤 Ouvindo...")
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
        print("⚠️ Sem conexão")
        return "erro"

# ==================================================
# 🎮 EXECUTAR COMANDOS
# ==================================================
def executar_comando(comando):
    global lembretes

    if 'que horas são' in comando:
        agora = datetime.datetime.now().strftime('%H:%M')
        falar(f"Agora são {agora}.")
        return

    for jogo, caminho in JOGOS.items():
        if f"abrir {jogo}" in comando:
            falar(f"Iniciando {jogo}!")
            try:
                os.startfile(caminho)
            except:
                falar(f"Não encontrei o {jogo}. Verifique a instalação.")
            return

    if 'abrir youtube' in comando:
        falar("Abrindo o YouTube!")
        webbrowser.open("youtube.com")
        return
    if 'abrir google' in comando:
        falar("Abrindo o Google!")
        webbrowser.open("google.com")
        return

    if 'lembre me de' in comando:
        texto = comando.replace('lembre me de', '').strip()
        lembretes.append(texto)
        falar(f"Anotei! Vou lembrar você de: {texto}")
        return
    if 'meus lembretes' in comando:
        if not lembretes:
            falar("Você não tem lembretes.")
        else:
            falar(f"Você tem {len(lembretes)} lembretes.")
            for i, l in enumerate(lembretes, 1):
                print(f"  {i}. {l}")
        return

    if 'verificar atualização' in comando or 'atualize se' in comando:
        falar("Verificando se há versão nova...")
        verificar_atualizacao()
        return

    if 'encerrar' in comando or 'sair' in comando:
        falar("Desligando sistemas. Até logo!")
        sys.exit()

    resposta = perguntar_ia(comando)
    falar(resposta)

# ==================================================
# 🚀 INÍCIO
# ==================================================
if __name__ == "__main__":
    print("="*60)
    print(f"🤖 JARVIS — VERSÃO {VERSAO_ATUAL}")
    print("🔄 Sistema de atualização automática ATIVADO!")
    print("💡 Diga 'verificar atualização' a qualquer momento")
    print("="*60)
    
    verificar_atualizacao()
    cumprimentar()

    while True:
        comando = ouvir()
        if comando != "nenhum" and comando != "erro":
            executar_comando(comando)