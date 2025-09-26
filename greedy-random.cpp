#include <iostream>
#include <fstream>
#include <vector>
#include <chrono>
#include <unordered_set>
#include <iomanip>
#include <random>
#include <algorithm>

using namespace std;
using Clock_timer = chrono::high_resolution_clock;

int main(int argc, char** argv) {
    // leer grupo de grafos, densidad y instancia del problema
     if (argc != 9) {
        cerr << "Uso: " << argv[0] << " -n <nodos> -d <densidad> -i <instancia> -k <grupo>\n";
        return 1;
    }
    
    int n = 0, instancia = 0, grupo = 0;
    double densidad = 0.0;
    for (int i = 1; i < argc; i += 2) {
        string arg = argv[i];
        if (arg == "-n") n = stoi(argv[i+1]);
        else if (arg == "-d") densidad = stod(argv[i+1]);
        else if (arg == "-i") instancia = stoi(argv[i+1]);
        else if (arg == "-k") grupo = stoi(argv[i+1]);
        else {
            cerr << "Argumento desconocido: " << arg << "\n";
            return 1;
        }
    }

    if (n != 1000 && n != 2000 && n != 3000) {
        cerr << "Solo se permiten 1000, 2000 o 3000 nodos.\n";
        return 1;
    }

    // Construir nombre de archivo
    ostringstream densidad_str;
    densidad_str << fixed << setprecision(1) << densidad;
    string carpeta = to_string(n);
    string filename = "dataset_grafos_no_dirigidos/new_"+ carpeta + "_dataset" + "/erdos_n" + to_string(n) + "_p0c" + densidad_str.str() + "_" + to_string(instancia) + ".graph";

    ifstream in(filename);
    if (!in) {
        cerr << "No se pudo abrir el archivo: " << filename << "\n";
        return 1;
    }


    vector<vector<int>> adj(n);
    vector<unordered_set<int>> adj_set(n);

    int u, v;
    while (in >> u >> v) {
        if (u < 0 || u >= n || v < 0 || v >= n) continue; // ignorar aristas inválidas
        if (u == v) continue; // ignorar lazos
        // evitar duplicados
        if (adj_set[u].insert(v).second) {
            adj[u].push_back(v);
        }
        if (adj_set[v].insert(u).second) {
            adj[v].push_back(u);
        }
    }
    in.close();

    // grado actual (solo vecinos no eliminados). Inicialmente es adj[].size()
    vector<int> curr_deg(n);
    for (int i = 0; i < n; ++i) curr_deg[i] = (int)adj[i].size();

    vector<char> removed(n, 0);
    int remaining = n;
    int solution_size = 0;

    int k = grupo;
    bool first_iteration = true;

    //medir tiempo
    auto t0 = Clock_timer::now();

    while (remaining > 0) {
        vector<int> bestH; 
        double bestDensity = numeric_limits<double>::infinity();

           
            // Recolectar todos los candidatos con su densidad
            vector<pair<double, vector<int>>> candidatos;

            for (int a = 0; a < n; ++a) {
                if (removed[a]) continue;
                double density = (double)curr_deg[a];
                candidatos.push_back({density, {a}});

                for (int b = a + 1; b < n; ++b) {
                    if (removed[b]) continue;
                    if (adj_set[a].find(b) != adj_set[a].end()) continue;
                    double pair_density = (double)(curr_deg[a] + curr_deg[b]) / 2.0;
                    candidatos.push_back({pair_density, {a, b}});
                }
            }

            if (candidatos.empty()) break;

            // Ordenar por densidad ascendente
            sort(candidatos.begin(), candidatos.end());
            int limite = min(k, (int)candidatos.size());

            // Elegir uno al azar entre los k mejores
            random_device rd;
            mt19937 gen(rd());
            uniform_int_distribution<> dis(0, limite - 1);
            int elegido = dis(gen);
            bestH = candidatos[elegido].second;

            first_iteration = false;


        

        if (bestH.empty()) break; // seguridad
        // agregar H a la solución
        solution_size += (int)bestH.size();

        // construir S = H U vecinos(H)
        vector<char> inS(n, 0);
        vector<int> Slist;
        for (int x : bestH) {
            if (!inS[x]) { inS[x] = 1; Slist.push_back(x); }
        }
        for (int x : bestH) {
            for (int nb : adj[x]) {
                if (!inS[nb] && !removed[nb]) { inS[nb] = 1; Slist.push_back(nb); }
            }
        }

        // eliminar vértices en Slist (actualizar removed y grados)
        for (int s : Slist) {
            if (removed[s]) continue;
            removed[s] = 1;
            remaining--;
            // disminuir grado de sus vecinos que aún no estén removidos
            for (int nb : adj[s]) {
                if (!removed[nb]) curr_deg[nb]--;
            }
            curr_deg[s] = 0;
        }
    }

    auto t1 = Clock_timer::now();
    double elapsed = chrono::duration<double>(t1 - t0).count();

    
    cout << solution_size << " " << fixed << setprecision(6) << elapsed << "\n";
    return 0;
}