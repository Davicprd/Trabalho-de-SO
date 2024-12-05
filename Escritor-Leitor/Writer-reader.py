import threading
import time
import random

# Recursos compartilhados
resource = 0  # Recurso compartilhado (simplesmente um número)
read_count = 0  # Contador de leitores ativos

# Semáforos para sincronização
mutex = threading.Semaphore(1)  # Protege o contador de leitores
write = threading.Semaphore(1)  # Exclusividade para escritores

# Função para leitores
def reader(id):
    global read_count
    while True:
        # Região crítica para atualizar read_count
        mutex.acquire()
        read_count += 1
        if read_count == 1:
            write.acquire()  # Bloqueia escritores se for o primeiro leitor
        mutex.release()

        # Seção crítica de leitura
        print(f"Leitor {id} está lendo o valor: {resource}")
        time.sleep(random.uniform(0.5, 2))  # Simula tempo de leitura

        # Região crítica para decrementar read_count
        mutex.acquire()
        read_count -= 1
        if read_count == 0:
            write.release()  # Libera escritores se for o último leitor
        mutex.release()

        time.sleep(random.uniform(1, 3))  # Simula intervalo entre leituras

# Função para escritores
def writer(id):
    global resource
    while True:
        write.acquire()  # Exclusividade para escritores
        # Seção crítica de escrita
        resource += 1
        print(f"Escritor {id} escreveu o valor: {resource}")
        time.sleep(random.uniform(1, 3))  # Simula tempo de escrita
        write.release()

        time.sleep(random.uniform(2, 5))  # Simula intervalo entre escritas

# Criação de threads para leitores e escritores
num_readers = 10
num_writers = 2

threads = []

# Criando threads de leitores
for i in range(num_readers):
    t = threading.Thread(target=reader, args=(i+1,))
    threads.append(t)

# Criando threads de escritores
for i in range(num_writers):
    t = threading.Thread(target=writer, args=(i+1,))
    threads.append(t)

# Iniciando todas as threads
for t in threads:
    t.start()
