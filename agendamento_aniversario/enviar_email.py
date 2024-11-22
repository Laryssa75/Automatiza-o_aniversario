import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def enviar_email():
    """Função que envia o e-mail."""
    load_dotenv()

    servidor_smtp = 'smtp.gmail.com'
    porta_smtp = 587

    remetente = os.getenv('EMAIL_REMETENTE')
    senha = os.getenv('EMAIL_SENHA')  # Aqui você usará a senha gerada do Google
    destinatario = os.getenv('EMAIL_DESTINATARIO')

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente
    mensagem['To'] = destinatario
    mensagem['Subject'] = 'Assunto do e-mail'

    corpo_email = 'Este é um e-mail de teste enviado automaticamente usando Python.'
    mensagem.attach(MIMEText(corpo_email, 'plain'))

    try:
        servidor = smtplib.SMTP(servidor_smtp, porta_smtp)
        servidor.starttls()
        servidor.login(remetente, senha)
        texto = mensagem.as_string()
        servidor.sendmail(remetente, destinatario, texto)
        servidor.quit()
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print(f'Ocorreu um erro ao enviar o e-mail: {e}')


def iniciar_tarefa():
    """Inicia o agendador do APScheduler."""
    scheduler = BackgroundScheduler()

    scheduler.add_job(enviar_email, 'cron', month=12, day=25, hour=0, minute=0) #definir a logica para conferir a data de aniversario
    
    scheduler.start()

    print("Agendador iniciado.")
