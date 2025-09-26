#!/usr/bin/env python3
import os
import subprocess
import statistics
import glob
from collections import defaultdict

SHOW_PROGRESS = False  # Mantener False para solo imprimir resultados finales

def extract_density_from_filename(filename):
    """Extrae la densidad del nombre del archivo"""
    # Buscar el patrón p0c<densidad> en el nombre del archivo
    parts = filename.split('_')
    for part in parts:
        if part.startswith('p0c'):
            density_str = part[3:]
            density = float(density_str)
            return density
    return None

def run_experiment(executable_path, graph_file):
    """Ejecuta el algoritmo en un archivo de grafo y retorna (solution_size, time)"""
    result = subprocess.run(
        [executable_path, '-i', graph_file],
        capture_output=True,
        text=True,
        timeout=300  # 5 minutos de timeout
    )
    if result.returncode == 0:
        output = result.stdout.strip()
        parts = output.split()
        if len(parts) == 2:
            solution_size = int(parts[0])
            execution_time = float(parts[1])
            return solution_size, execution_time
        else:
            return None, None

def main():
    # Usar directorio actual del script para rutas relativas
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ruta al ejecutable (relativa)
    executable_path = "./greedy_misp"
    
    # Verificar que el ejecutable existe
    exe_full_path = os.path.join(script_dir, executable_path.lstrip('./'))
    if not os.path.exists(exe_full_path) or not os.access(exe_full_path, os.X_OK):
        print(f"Error: No se encontró el ejecutable {executable_path}")
        print("Compila greedy.cpp con: g++ -o greedy_misp greedy.cpp")
        return
    
    # Directorios de datasets (rutas relativas)
    dataset_dirs = ["new_1000_dataset", "new_2000_dataset", "new_3000_dataset"]
    
    for dataset_dir in dataset_dirs:
        dataset_path = os.path.join(script_dir, dataset_dir)
        if not os.path.exists(dataset_path):
            continue
        
        # Buscar archivos .graph
        pattern = os.path.join(dataset_path, "erdos_n*_p0c*.graph")
        graph_files = glob.glob(pattern)
        
        if not graph_files:
            continue
        
        # Agrupar archivos por densidad
        density_groups = defaultdict(list)
        
        for graph_file in graph_files:
            filename = os.path.basename(graph_file)
            density = extract_density_from_filename(filename)
            
            if density is not None:
                # Solo usar las densidades específicas: 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9
                valid_densities = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
                if density in valid_densities:
                    density_groups[density].append(graph_file)
        
        # Procesar cada grupo de densidad
        results_by_density = {}
        
        for density in sorted(density_groups.keys()):
            files = density_groups[density]
            solution_sizes = []
            execution_times = []
            
            for graph_file in files:
                solution_size, exec_time = run_experiment(executable_path, graph_file)
                
                if solution_size is not None and exec_time is not None:
                    solution_sizes.append(solution_size)
                    execution_times.append(exec_time)
            
            if solution_sizes and execution_times:
                # Calcular estadísticas
                avg_solution = statistics.mean(solution_sizes)
                avg_time = statistics.mean(execution_times)
                
                results_by_density[density] = {
                    'avg_solution': avg_solution,
                    'avg_time': avg_time
                }
        
        # Solo imprimir resumen final
        if results_by_density:
            print(f"RESULTADOS {dataset_dir.upper()}")
            print(f"Densidad Tamaño_Promedio Tiempo_Promedio_s")
            for density in sorted(results_by_density.keys()):
                stats = results_by_density[density]
                print(f"{density:.1f} {stats['avg_solution']:.2f} {stats['avg_time']:.6f}")

if __name__ == "__main__":
    main()
