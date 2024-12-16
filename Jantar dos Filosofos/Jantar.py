import threading
import random
import time

N = 5  # Número de filósofos
EXECUTIONS = 1000  # Número de execuções para verificar impasse
IMPASSE_TENTATIVAS_MAX = 50  # Número máximo de tentativas antes de considerar impasse
impasse_ocorreu = False

# Mutex para sincronizar o acesso aos garfos
garfos = [threading.Lock() for _ in range(N)]
mutex = threading.Lock()

# Variáveis para armazenar os tempos
total_tempo_espera = 0
total_tempo_comendo = 0
total_execucoes = 0
tentativas_sem_sucesso = [0] * N  # Contador de tentativas sem sucesso para cada filósofo

def filosofo(id, execucoes):
    global impasse_ocorreu, total_tempo_espera, total_tempo_comendo, total_execucoes, tentativas_sem_sucesso

    for _ in range(execucoes):
        # O filósofo está pensando
        pensar()

        # Tentar pegar os garfos
        if id < (id + 1) % N:  # Ordem de prioridade para evitar impasses
            primeiro, segundo = id, (id + 1) % N
        else:
            primeiro, segundo = (id + 1) % N, id

        start_espera = time.time()  # Marca o tempo de início da espera

        with mutex:  # Proteção para verificar e pegar garfos
            if garfos[primeiro].locked() or garfos[segundo].locked():
                tentativas_sem_sucesso[id] += 1
                if tentativas_sem_sucesso[id] > IMPASSE_TENTATIVAS_MAX:
                    print(f"Impasse detectado! Filósofo {id} não conseguiu pegar os garfos após várias tentativas.")
                    impasse_ocorreu = True
                    return  # Encerra a execução do filósofo após detectar impasse
                continue  # Não pegar garfos se não estão disponíveis

            garfos[primeiro].acquire()
            garfos[segundo].acquire()

        # Calcula o tempo de espera e acumula
        total_tempo_espera += time.time() - start_espera
        tentativas_sem_sucesso[id] = 0  # Reseta a contagem de tentativas sem sucesso quando consegue pegar os garfos

        # Comer
        start_comendo = time.time()
        comer(id)
        total_tempo_comendo += time.time() - start_comendo

        # Liberar os garfos
        garfos[primeiro].release()
        garfos[segundo].release()

    total_execucoes += execucoes


def pensar():
    time.sleep(random.uniform(0.1, 0.3))  # Simula tempo pensando


def comer(id):
    print(f"Filósofo {id} está comendo.")
    time.sleep(random.uniform(0.1, 0.3))  # Simula tempo comendo


def verificar_impasse():
    global impasse_ocorreu, total_tempo_espera, total_tempo_comendo, total_execucoes

    for _ in range(EXECUTIONS):
        threads = []
        for i in range(N):
            t = threading.Thread(target=filosofo, args=(i, 10))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    # Cálculo dos tempos médios
    tempo_medio_espera = total_tempo_espera / total_execucoes
    tempo_medio_comendo = total_tempo_comendo / total_execucoes

    print(f"Teste finalizado!")
    print(f"Tempo médio de espera: {tempo_medio_espera:.4f} segundos")
    print(f"Tempo médio de comendo: {tempo_medio_comendo:.4f} segundos")

    if not impasse_ocorreu:
        print("Nenhum impasse ocorreu durante a simulação.")
    else:
        print("Impasse ocorreu durante a simulação!")


if __name__ == "__main__":
    verificar_impasse()
