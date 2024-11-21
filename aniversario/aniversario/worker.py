import django_rq

#Inicia a worker para processar as tarefas na fila default
if __name__ == '__main__':
    django_rq.get_worker('default').work()