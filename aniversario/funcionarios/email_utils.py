import yagmail
import logging
import os
from django.conf import settings
from django.template.loader import render_to_string

def enviar(destinatario, nome_destinatario, foto = None):
    try:
        #Verifica se a foto foi fornecida e se o caminho da foto é valido/existe
        if foto and not os.path.exists(foto):
            raise ValueError("O caminho da foto não existe.")

        # Configura o SMTP com yagmail usando as credenciais do settings.py
        yag = yagmail.SMTP(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Renderiza o template de email com os dados do funcionário
        mensagem = render_to_string('funcionarios/email_template.html', {'nome': nome_destinatario})
    
        #Configura o assunto e mensagem do email, além da assinatura
        assunto = f"Feliz Aniversário!, {nome_destinatario}!"
    
        if foto:
            yag.send(to=destinatario, subject=assunto, contents=mensagem, attachments=foto)
        else:
            yag.send(to=destinatario, subject=assunto, contents=mensagem)

        print(f"Email enviado com sucesso para {destinatario}")
        logging.info(f"Email enviado com sucesso para {destinatario}")
        return True
    
    except Exception as e:
        print(f"Erro ao enviar e-mail:{e}")
        logging.error(f"Erro ao enviar o e-mail:{e}")
        return False