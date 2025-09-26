#!/usr/bin/env python3
"""
Script greedy-random silencioso: solo imprime resultados finales.
"""
import os, subprocess, statistics, glob
from collections import defaultdict

SHOW_PROGRESS = False  # Mantener en False

def extract_parameters_from_filename(filename):
    """Extrae n, densidad e instancia del nombre del archivo"""
    # Ejemplo: erdos_n1000_p0c0.1_1.graph
    parts = filename.split('_')
    n = density = instance = None
    for part in parts:
        if part.startswith('n') and part[1:].isdigit():
            n = int(part[1:])
        elif part.startswith('p0c'):
            try:
                density = float(part[3:])
            except ValueError:
                pass
        elif part.replace('.graph','').isdigit():
            instance = int(part.replace('.graph',''))
    return n, density, instance

def extract_density_from_filename(filename):
    """Extrae la densidad del nombre del archivo"""
    # Buscar el patrón p0c<densidad> en el nombre del archivo
    for part in filename.split('_'):
        if part.startswith('p0c'):
            try:
                return float(part[3:])
            except ValueError:
                return None
    return None

def run_experiment(executable_path, graph_file, k):
    """Ejecuta el algoritmo greedy-random con los parámetros extraídos del archivo y retorna (solution_size, time)"""
    filename = os.path.basename(graph_file)
    n, density, instance = extract_parameters_from_filename(filename)
    if n is None or density is None or instance is None:
        return None, None
    try:
        result = subprocess.run([
            executable_path, '-n', str(n), '-d', str(density), '-i', str(instance), '-k', str(k)
        ], capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            return None, None
        parts = result.stdout.strip().split()
        if len(parts) == 2:
            return int(parts[0]), float(parts[1])
    except Exception:
        return None, None
    return None, None

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Detectar ejecutable
    for cand in ('./greedy-random','./greedy_random','./greedy-random.exe'):
        full = os.path.join(script_dir, cand.lstrip('./'))
        if os.path.exists(full) and os.access(full, os.X_OK):
            executable = cand
            break
    else:
        print("ERROR: ejecutable greedy-random no encontrado")
        return
    # Leer k con prompt
    try:
        k = int(input("Ingrese k: ").strip())
    except Exception:
        print("ERROR: k inválido")
        return
    dataset_dirs = ["new_1000_dataset","new_2000_dataset","new_3000_dataset"]
    for dataset_dir in dataset_dirs:
        dataset_path = os.path.join(script_dir, dataset_dir)
        if not os.path.isdir(dataset_path):
            continue
        pattern = os.path.join(dataset_path, "erdos_n*_p0c*.graph")
        graph_files = glob.glob(pattern)
        if not graph_files:
            continue
        density_groups = defaultdict(list)
        for g in graph_files:
            d = extract_density_from_filename(os.path.basename(g))
            if d in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
                density_groups[d].append(g)
        results = {}
        for d in sorted(density_groups.keys()):
            sols, times = [], []
            for g in density_groups[d]:
                s, t = run_experiment(executable, g, k)
                if s is not None:
                    sols.append(s); times.append(t)
            if sols:
                results[d] = (statistics.mean(sols), statistics.mean(times))
        if results:
            print(f"RESULTADOS {dataset_dir.upper()} K={k}")
            print("Densidad Tamaño_Promedio Tiempo_Promedio_s")
            for d in sorted(results.keys()):
                ms, mt = results[d]
                print(f"{d:.1f} {ms:.2f} {mt:.6f}")

if __name__ == '__main__':
    main()
