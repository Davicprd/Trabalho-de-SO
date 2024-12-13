import threading
import time
import matplotlib.pyplot as plt
import numpy as np

class Process:
    def __init__(self, pid, burst_time):
        self.pid = pid
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.waiting_time = 0
        self.turnaround_time = 0

def round_robin(processes, quantum, context_switch_time):
    lock = threading.Lock()
    time_elapsed = 0
    completed_processes = 0
    n = len(processes)
    sequence = []

    def execute_process(process):
        nonlocal time_elapsed, completed_processes

        while process.remaining_time > 0:
            with lock:
                sequence.append(process.pid)
                exec_time = min(process.remaining_time, quantum)
                time.sleep(exec_time * 0.01)  # Simula tempo de execução
                time_elapsed += exec_time
                process.remaining_time -= exec_time

                if process.remaining_time == 0:
                    process.turnaround_time = time_elapsed
                    process.waiting_time = process.turnaround_time - process.burst_time
                    completed_processes += 1

                time_elapsed += context_switch_time
                time.sleep(context_switch_time * 0.01)  # Simula tempo de troca de contexto

    threads = []

    while completed_processes < n:
        for process in processes:
            if process.remaining_time > 0:
                thread = threading.Thread(target=execute_process, args=(process,))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

    avg_waiting_time = np.mean([p.waiting_time for p in processes])
    std_waiting_time = np.std([p.waiting_time for p in processes])
    avg_turnaround_time = np.mean([p.turnaround_time for p in processes])
    std_turnaround_time = np.std([p.turnaround_time for p in processes])
    throughput = n / time_elapsed

    metrics = {
        "avg_waiting_time": avg_waiting_time,
        "std_waiting_time": std_waiting_time,
        "avg_turnaround_time": avg_turnaround_time,
        "std_turnaround_time": std_turnaround_time,
        "throughput": throughput,
    }

    return metrics, sequence

# Simulação
if __name__ == "__main__":
    processes_data = [
        ("P1", 8),
        ("P2", 4),
        ("P3", 9),
        ("P4", 5),
        ("P5", 11),
        ("P6", 13),
        ("P7", 15),
        ("P8", 2),
    ]

    context_switch_time = 1  # Tempo de troca de contexto
    quantums = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]  # Diferentes valores de quantum

    avg_waiting_times = []
    avg_turnaround_times = []
    throughputs = []

    for quantum in quantums:
        processes = [Process(pid=p[0], burst_time=p[1]) for p in processes_data]
        metrics, sequence = round_robin(processes, quantum, context_switch_time)

        print(f"\nQuantum: {quantum}")
        print("Sequência de execução:", " -> ".join(map(str, sequence)))
        print(f"Tempo médio de espera (+/- std): {metrics['avg_waiting_time']:.2f} (+/- {metrics['std_waiting_time']:.2f})")
        print(f"Tempo médio de retorno (+/- std): {metrics['avg_turnaround_time']:.2f} (+/- {metrics['std_turnaround_time']:.2f})")
        print(f"Vazão: {metrics['throughput']:.2f} processos/unidade de tempo")

        avg_waiting_times.append(metrics['avg_waiting_time'])
        avg_turnaround_times.append(metrics['avg_turnaround_time'])
        throughputs.append(metrics['throughput'])

    # Plotando os gráficos
    plt.figure(figsize=(15, 5))

    # Gráfico de Tempo Médio de Espera
    plt.subplot(1, 3, 1)
    plt.plot(quantums, avg_waiting_times, marker='o')
    plt.title('Tempo Médio de Espera')
    plt.xlabel('Quantum')
    plt.ylabel('Tempo Médio de Espera')

    # Gráfico de Tempo Médio de Retorno
    plt.subplot(1, 3, 2)
    plt.plot(quantums, avg_turnaround_times, marker='o', color='green')
    plt.title('Tempo Médio de Retorno')
    plt.xlabel('Quantum')
    plt.ylabel('Tempo Médio de Retorno')

    # Gráfico de Vazão
    plt.subplot(1, 3, 3)
    plt.plot(quantums, throughputs, marker='o', color='red')
    plt.title('Vazão')
    plt.xlabel('Quantum')
    plt.ylabel('Vazão (processos/unidade de tempo)')

    plt.tight_layout()
    plt.show()
