# Maximum Independent Set Problem (MISP)

Proyecto semestral: Implementación de dos heurísticas para el Maximum Independent Set Problem:
1. greedy (determinista)
2. greedy-random (aleatorizado con parámetro k)

## Estructura de directorios
```
Proyecto-Semestral-Sistemas-Adaptativos--MISP/
├── greedy.cpp               # Heurística greedy
├── greedy-random.cpp        # Heurística greedy aleatorizada
├── greedy_misp              # Ejecutable (greedy) tras compilar
├── greedy-random            # Ejecutable (greedy-random) tras compilar
├── new_1000_dataset/        # Grafos n=1000
├── new_2000_dataset/        # Grafos n=2000
├── new_3000_dataset/        # Grafos n=3000
├── run_greedy_experiments.py        # Corre todos los grafos con greedy (resumen)
├── run_greedy_random_experiments.py # Corre todos los grafos con greedy-random (pide k)
```
Cada archivo de grafo sigue el patrón:
```
erdos_n<NUM_NODOS>_p0c<DENSIDAD>_<INSTANCIA>.graph
Ejemplo: erdos_n2000_p0c0.3_12.graph
```
Densidades usadas: 0.1 ... 0.9
Instancias: 1..30

## Requisitos
- g++ (C++11 o superior)
- Python 3.8+

## Compilación
Desde la carpeta raíz del proyecto:
```bash
g++ -std=c++11 -O2 -o greedy_misp greedy.cpp
g++ -std=c++11 -O2 -o greedy-random greedy-random.cpp
```
Verifica que los ejecutables tengan permisos:
```bash
ls -l greedy_misp greedy-random
```

## Ejecución individual (manual)
Greedy determinista:
```bash
./greedy_misp -n 1000 -d 0.3 -i 5
```
Salida: "<tamaño_solución> <tiempo_segundos>"

Greedy aleatorizado (k = tamaño del grupo de candidatos):
```bash
./greedy-random -n 1000 -d 0.3 -i 5 -k 3
```

## Correr todos los experimentos (greedy)
```bash
python3 run_greedy_experiments.py
```
Genera promedios por densidad y dataset.

## Correr todos los experimentos (greedy-random)
```bash
python3 run_greedy_random_experiments.py
```
El script solicita k y luego procesa todas las instancias.

## Notas sobre rutas
Los códigos C++ construyen internamente las rutas de los grafos como:
```
new_<n>_dataset/erdos_n<n>_p0c<densidad>_<instancia>.graph
```
Asegúrate de que los directorios `new_1000_dataset`, `new_2000_dataset`, `new_3000_dataset` estén en la raíz del proyecto. Dentro de ellos tienen que estar los grafos de la categoria que corresponda.