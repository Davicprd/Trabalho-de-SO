import numpy as np
import matplotlib.pyplot as plt

def round_robin(processes, burst_times, quantum, context_switch_time):
    n = len(processes)
    waiting_times = [0] * n
    turnaround_times = [0] * n
    remaining_times = burst_times[:]
    sequence = []

    time = 0
    completed_processes = 0

    while completed_processes < n:
        for i in range(n):
            if remaining_times[i] > 0:
                sequence.append(processes[i])

                # Execute the process for the quantum or until completion
                if remaining_times[i] > quantum:
                    time += quantum
                    remaining_times[i] -= quantum
                else:
                    time += remaining_times[i]
                    turnaround_times[i] = time
                    waiting_times[i] = time - burst_times[i]
                    remaining_times[i] = 0
                    completed_processes += 1

                # Add context switch time unless all processes are complete
                if completed_processes < n:
                    time += context_switch_time

    avg_waiting_time = np.mean(waiting_times)
    std_waiting_time = np.std(waiting_times)
    avg_turnaround_time = np.mean(turnaround_times)
    std_turnaround_time = np.std(turnaround_times)
    throughput = n / time

    metrics = {
        "avg_waiting_time": avg_waiting_time,
        "std_waiting_time": std_waiting_time,
        "avg_turnaround_time": avg_turnaround_time,
        "std_turnaround_time": std_turnaround_time,
        "throughput": throughput,
    }

    return metrics, sequence

# Simulação
def simulate():
    processes = ["P1", "P2", "P3", "P4"]
    burst_times = [8, 4, 9, 5, 11, 13, 15, 2]  # Tempo de execução de cada processo
    context_switch_time = 1  # Tempo de troca de contexto
    quantums = [2, 4, 6, 8, 10, 12, 14]  # Diferentes valores de quantum

    avg_waiting_times = []
    avg_turnaround_times = []
    throughputs = []

    for quantum in quantums:
        print(f"\nQuantum: {quantum}")
        metrics, sequence = round_robin(processes, burst_times, quantum, context_switch_time)
        print("Sequência de execução:", " -> ".join(sequence))
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

if __name__ == "__main__":
    simulate()
