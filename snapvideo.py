import yt_dlp as yt_baixar
from moviepy.editor import *
import customtkinter as ct
from tkinter import messagebox
from transformers import pipeline
import whisper

# Função para baixar o vídeo do YouTube
def baixar_video(url, formato='mp4'):

    url_video = (url)
    ydl_opts = {
        'merge_output_format': formato, 

        'outtmpl': 'video.mp4'#NOME DO VIDEO DEFINIDO PARA O PARAMETRO DA EXTRAÇÃO(SE ALTERAR, TEM Q MUDAR O VIDEO_PATCH)

    } #Aqui serve definir as configurações de download do vídeo (é necessário uma virgula para cada config se nao buga tudo)
    
    with yt_baixar.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url_video])

    
    return 'video.mp4'

# Extrair o áudio do vídeo

def extrair_audio(video_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile("audio.wav")
    return "audio.wav"

# Função para transcrever o áudio

def transcrever_audio(audio_patch):
    # Carrega o modelo Whisper
    modelo = whisper.load_model("base")
    
    # Faz a transcrição do áudio
    resultado = modelo.transcribe(audio_patch)
    
    return resultado['text']

# Função para resumir o texto transcrito
def resumir_texto(texto):
    try:
        summarizer = pipeline("summarization")
        max_input_length = 1024  # Ajuste conforme o modelo e suas limitações
        if len(texto) > max_input_length:
            partes = [texto[i:i + max_input_length] for i in range(0, len(texto), max_input_length)]
            resumos = [summarizer(parte, max_length=150, min_length=50, do_sample=False)[0]['summary_text'] for parte in partes]
            resumo_final = " ".join(resumos)
        else:
            resumo_final = summarizer(texto, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        print("Texto resumido com sucesso.")
        return resumo_final
    except Exception as e:
        print(f"Erro ao resumir texto: {e}")
        return None

# Função principal

def resumir_video_do_youtube(url):
    video_path = baixar_video(url) #Armazena o vídeo na pasta local
    audio_path = extrair_audio(video_path) #Extrai o audio do vídeo e armazena o audio
    texto_transcrito = transcrever_audio(audio_path) #Transcreve o audio do audio armazenado 
    resumo = resumir_texto(texto_transcrito)
    
    return resumo

#Interface Gráfica
def clique():
   url = link.get()

   if not url.strip():
       messagebox.showinfo("A caixa de URL está vazia!")
    
   else:
       inicia = resumir_video_do_youtube(url)
       messagebox.showinfo("RESUMO DO VÍDEO: ", inicia)
   
#Titulo e tamanho da janela

janela = ct.CTk()
janela.title("Snap Video")
janela._set_appearance_mode("dark")
janela.geometry("800x500")
titulo = ct.CTkLabel(janela, text="Snap Video") 
titulo.pack(padx=10, pady=10)


link = ct.CTkEntry(janela, placeholder_text="URL do vídeo")
link.pack(padx=10, pady=10)

bt_resumir = ct.CTkButton(janela, text="Resumir", command=clique)
bt_resumir.pack(padx=10, pady=10)

janela.mainloop()
