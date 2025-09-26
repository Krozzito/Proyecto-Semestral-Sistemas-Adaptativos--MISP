#!/usr/bin/env python3
import os
import subprocess
import statistics
import glob
from collections import defaultdict
import sys

def extract_density_from_filename(filename):
    """Extrae la densidad del nombre del archivo"""
    parts = filename.split('_')
    for part in parts:
        if part.startswith('p0c'):
            density_str = part[3:]
            try:
                density = float(density_str)
                return density
            except ValueError:
                continue
    return None

def run_experiment(executable_path, graph_file):
    """Ejecuta el algoritmo en un archivo de grafo y retorna (solution_size, time)"""
    try:
        result = subprocess.run(
            [executable_path, '-i', graph_file],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            parts = output.split()
            if len(parts) == 2:
                solution_size = int(parts[0])
                execution_time = float(parts[1])
                return solution_size, execution_time
        return None, None
    except Exception:
        return None, None

def main():
    executable_path = "./greedy_misp"
    
    # Procesar solo el dataset de 1000 nodos
    dataset_dir = "new_1000_dataset"
    base_dir = "/Users/pedromunozsolano/Desktop/OwO/Sistemas_Adaptativos/Proyecto-Semestral-Sistemas-Adaptativos--MISP"
    
    print("="*80)
    print("ANÁLISIS DEL ALGORITMO GREEDY PARA MAXIMUM INDEPENDENT SET PROBLEM")
    print("Dataset: Grafos Erdős-Rényi con n=1000 nodos")
    print("="*80)
    
    dataset_path = os.path.join(base_dir, dataset_dir)
    pattern = os.path.join(dataset_path, "erdos_n*_p0c*.graph")
    graph_files = glob.glob(pattern)
    
    # Agrupar archivos por densidad (solo 0.1 a 0.9)
    density_groups = defaultdict(list)
    
    for graph_file in graph_files:
        filename = os.path.basename(graph_file)
        density = extract_density_from_filename(filename)
        
        if density is not None and 0.1 <= density <= 0.9:
            # Solo procesar densidades "principales" (0.1, 0.2, ..., 0.9)
            if density in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
                density_groups[density].append(graph_file)
    
    # Procesar cada grupo de densidad
    print(f"\\n{'Densidad':<9} {'Archivos':<9} {'Tamaño Promedio':<15} {'Desv. Est.':<10} {'Rango':<12} {'Tiempo Prom.':<12} {'Desv. Tiempo':<12}")
    print("-" * 80)
    
    all_results = {}
    
    for density in sorted(density_groups.keys()):
        files = density_groups[density]
        
        solution_sizes = []
        execution_times = []
        
        print(f"Procesando densidad {density}... ", end="", flush=True)
        
        for graph_file in files:
            solution_size, exec_time = run_experiment(executable_path, graph_file)
            
            if solution_size is not None and exec_time is not None:
                solution_sizes.append(solution_size)
                execution_times.append(exec_time)
        
        if solution_sizes and execution_times:
            # Calcular estadísticas
            avg_solution = statistics.mean(solution_sizes)
            std_solution = statistics.stdev(solution_sizes) if len(solution_sizes) > 1 else 0
            avg_time = statistics.mean(execution_times)
            std_time = statistics.stdev(execution_times) if len(execution_times) > 1 else 0
            min_solution = min(solution_sizes)
            max_solution = max(solution_sizes)
            
            all_results[density] = {
                'count': len(solution_sizes),
                'avg_solution': avg_solution,
                'std_solution': std_solution,
                'min_solution': min_solution,
                'max_solution': max_solution,
                'avg_time': avg_time,
                'std_time': std_time
            }
            
            print(f"{density:<9.1f} {len(solution_sizes):<9} "
                  f"{avg_solution:<15.2f} {std_solution:<10.2f} "
                  f"{min_solution}-{max_solution:<10} {avg_time:<12.6f} {std_time:<12.6f}")
        else:
            print(f"{density:<9.1f} {'ERROR':<9}")
    
    print("\\n" + "="*80)
    print("RESUMEN DE RESULTADOS")
    print("="*80)
    print("\\nObservaciones:")
    print("1. A medida que aumenta la densidad del grafo, el tamaño del conjunto independiente máximo disminuye")
    print("2. El tiempo de ejecución tiende a disminuir con mayor densidad")
    print("3. La variabilidad en los resultados es consistente entre densidades")
    
    # Calcular algunos insights adicionales
    if all_results:
        densities = sorted(all_results.keys())
        print(f"\\nRango de densidades: {densities[0]} - {densities[-1]}")
        print(f"Tamaño promedio del conjunto independiente:")
        print(f"  - Densidad baja (0.1): {all_results[0.1]['avg_solution']:.1f} nodos")
        print(f"  - Densidad alta (0.9): {all_results[0.9]['avg_solution']:.1f} nodos")
        print(f"  - Reducción: {((all_results[0.1]['avg_solution'] - all_results[0.9]['avg_solution']) / all_results[0.1]['avg_solution'] * 100):.1f}%")
        
        print(f"\\nTiempo de ejecución promedio:")
        print(f"  - Densidad baja (0.1): {all_results[0.1]['avg_time']:.6f} segundos")
        print(f"  - Densidad alta (0.9): {all_results[0.9]['avg_time']:.6f} segundos")

if __name__ == "__main__":
    main()
