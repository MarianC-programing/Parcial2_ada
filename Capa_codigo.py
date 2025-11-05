import math
import random
import time
import tracemalloc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Variables globales para almacenar la matriz y el tamaño 
matriz_global = None
n_global = None


# =============================================================================
# PARTE I - ALGORITMO PRINCIPAL: ASIGNACIÓN DE RUTAS DE ENTREGA
# =============================================================================
def generar_matriz_automatica(n):
    """Genera una matriz aleatoria de distancias."""
    return [[random.randint(1, 20) if i != j else 0 for j in range(n)] for i in range(n)]


def mostrar_matriz(matriz):
    print("\nMATRIZ DE DISTANCIAS (KM):")
    for fila in matriz:
        print("  ".join(f"{x:3}" for x in fila))


def editar_matriz(matriz):
    """Permite editar rutas específicas sin reingresar toda la matriz."""
    while True:
        opcion = input("\n¿Desea modificar alguna distancia? (S/N): ").strip().lower()
        if opcion != "s":
            break

        try:
            i = int(input("Ingrese el punto de origen (índice): "))
            j = int(input("Ingrese el punto de destino (índice): "))
            nuevo_valor = int(input("Ingrese la nueva distancia (km): "))

            if i == j or i < 0 or j < 0 or i >= len(matriz) or j >= len(matriz):
                print(" Índices inválidos. Intente nuevamente.")
                continue

            matriz[i][j] = nuevo_valor
            matriz[j][i] = nuevo_valor  # simétrica
            print(f" Distancia entre {i} y {j} actualizada a {nuevo_valor} km.")
        except ValueError:
            print(" Entrada inválida. Debe ser un número entero.")


def mostrar_rutas_disponibles(n):
    """Muestra las rutas disponibles basadas en las filas de la matriz."""
    print("\n=== RUTAS DISPONIBLES ===")
    for i in range(n):
        ruta = list(range(n))  # Todos los puntos en orden
        ruta.pop(i)  # Eliminar el punto actual
        print(f"Ruta {i + 1}: 0 -> {' -> '.join(map(str, ruta))} -> 0")
    print("=" * 40)

def asignar_rutas_manual(num_conductores, n):
    """Permite asignar rutas predefinidas a los conductores."""
    rutas = {}
    
    # Mostrar las rutas disponibles
    mostrar_rutas_disponibles(n)
    
    print("\n=== Asignación de Rutas a Conductores ===")
    print("Para cada conductor, indique el número de ruta que desea asignarle")
    
    rutas_asignadas = set()  # Para llevar control de rutas ya asignadas
    
    for i in range(num_conductores):
        while True:
            try:
                ruta_num = int(input(f"Número de ruta para Conductor {i + 1}: "))
                if ruta_num < 1 or ruta_num > n:
                    print(f"El número de ruta debe estar entre 1 y {n}")
                    continue
                    
                if ruta_num in rutas_asignadas:
                    print(" Esta ruta ya fue asignada a otro conductor")
                    continue
                    
                # Crear la ruta basada en el número seleccionado
                puntos = list(range(n))  # Todos los puntos
                punto_inicio = ruta_num - 1
                puntos.pop(punto_inicio)  # Eliminar el punto de inicio
                ruta_completa = [0] + puntos + [0]
                
                rutas[i + 1] = ruta_completa
                rutas_asignadas.add(ruta_num)
                print(f"Ruta {ruta_num} asignada al Conductor {i + 1}")
                break
                
            except ValueError:
                print("Por favor, ingrese un número válido")
    
    return rutas

def asignar_rutas():
    global matriz_global, n_global

    print("\n" + "=" * 80)
    print(" ALGORITMO PRINCIPAL: ASIGNACIÓN DE RUTAS DE ENTREGA ")
    print("=" * 80)

    if matriz_global is None:
        n_global = int(input("Ingrese el número de puntos de entrega: "))
        matriz_global = generar_matriz_automatica(n_global)
        print("\n Matriz generada automáticamente.")
    else:
        print("\n Usando la matriz previamente generada.")

    mostrar_matriz(matriz_global)
    editar_matriz(matriz_global)

    capacidad = int(input("\nCapacidad máxima de paquetes por conductor: "))
    total_paquetes = int(input("Cantidad total de paquetes a distribuir: "))

    num_conductores = math.ceil(total_paquetes / capacidad)
    paquetes_restantes = total_paquetes

    # Agregamos la asignación manual de rutas
    rutas_asignadas = asignar_rutas_manual(num_conductores, n_global)

    print("\n--- RESULTADOS DE ASIGNACIÓN DE RUTAS ---")
    for c in range(num_conductores):
        paquetes = capacidad if paquetes_restantes >= capacidad else paquetes_restantes
        paquetes_restantes -= paquetes

        inicio = 0
        fin = min(n_global - 1, (c + 1) * paquetes - 1)

        distancia_total = sum(matriz_global[i][i + 1] for i in range(inicio, fin))
        distancia_total += matriz_global[fin][0]

        ruta_asignada = rutas_asignadas.get(c + 1, list(range(inicio, fin + 1)) + [0])
        print(f"\nConductor {c + 1}:")
        print(f"  Paquetes asignados: {paquetes}")
        print(f"  Ruta: {ruta_asignada}")
        
        # Calcular distancia total para la ruta asignada
        distancia_total = 0
        for i in range(len(ruta_asignada) - 1):
            origen = ruta_asignada[i]
            destino = ruta_asignada[i + 1]
            distancia_total += matriz_global[origen][destino]
            
        print(f"  Distancia total recorrida: {distancia_total} km")

    print("\nAsignación completada correctamente.\n")


# =============================================================================
# PARTE II - ANÁLISIS EMPÍRICO DE COMPLEJIDAD
# =============================================================================
def asignar_rutas_automatico(n):
    matriz = generar_matriz_automatica(n)
    capacidad = 3
    total_paquetes = n // 2
    num_conductores = math.ceil(total_paquetes / capacidad)
    paquetes_restantes = total_paquetes

    for c in range(num_conductores):
        paquetes = capacidad if paquetes_restantes >= capacidad else paquetes_restantes
        paquetes_restantes -= paquetes

        inicio = 0
        fin = min(n - 1, (c + 1) * paquetes - 1)
        distancia_total = sum(matriz[i][i + 1] for i in range(inicio, fin))
        distancia_total += matriz[fin][0]

    return distancia_total


def medir_tiempo_memoria(funcion, *args):
    tracemalloc.start()
    inicio = time.time()
    funcion(*args)
    fin = time.time()
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return (fin - inicio) * 1000, memoria_pico / (1024 * 1024)


def analisis_empirico():
    print("\n" + "=" * 80)
    print(" ANÁLISIS EMPÍRICO DE COMPLEJIDAD DEL ALGORITMO DE RUTAS ")
    print("=" * 80)

    tamanos = [50, 100, 500, 1000, 2000, 3000]
    tiempos_por_n = {}
    memorias_por_n = {}

    for n in tamanos:
        tiempos = []
        memorias = []
        for _ in range(5):  # 5 repeticiones para promedio
            t, m = medir_tiempo_memoria(asignar_rutas_automatico, n)
            tiempos.append(t)
            memorias.append(m)
        tiempos_por_n[n] = tiempos
        memorias_por_n[n] = memorias

    generar_grafico_interactivo(tiempos_por_n, memorias_por_n)
    print("\nAnálisis empírico completado. Archivo HTML generado.\n")


# =============================================================================
# PARTE III - GRÁFICO INTERACTIVO 
# =============================================================================
def generar_grafico_interactivo(tiempos_por_n, memorias_por_n):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Tiempo (ms)", "Memoria (MB)"))

    colores = ["red", "blue", "green", "orange", "purple", "brown"]
    for i, (n, tiempos) in enumerate(tiempos_por_n.items()):
        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(tiempos) + 1)),
                y=tiempos,
                mode="lines+markers",
                name=f"n={n}",
                line=dict(color=colores[i % len(colores)], width=3)
            ),
            row=1, col=1
        )

    for i, (n, memorias) in enumerate(memorias_por_n.items()):
        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(memorias) + 1)),
                y=memorias,
                mode="lines+markers",
                name=f"n={n}",
                line=dict(color=colores[i % len(colores)], width=3)
            ),
            row=1, col=2
        )

    fig.update_layout(
        title="Análisis Empírico del Algoritmo de Rutas",
        hovermode="x unified",
        template="plotly_white",
        legend=dict(title="Tamaño n", itemclick="toggleothers", itemdoubleclick="toggle"),
    )

    fig.update_xaxes(title_text="Iteración")
    fig.update_yaxes(title_text="Tiempo (ms)", row=1, col=1)
    fig.update_yaxes(title_text="Memoria (MB)", row=1, col=2)

    fig.write_html("analisis_rutas_interactivo.html")
    print("\n Gráfica guardada en 'analisis_rutas_interactivo.html'.")


# ===============================================================
# MENÚ PRINCIPAL
# ===============================================================
def menu():
    while True:
        print("\n" + "x" * 70)
        print("   PARCIAL II - RUTAS DE ENTREGA CON ANÁLISIS DE COMPLEJIDAD")
        print("x" * 70)
        print("1) Ejecutar algoritmo principal")
        print("2) Ejecutar análisis empírico")
        print("3) Salir")
        print("=" * 70)
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == "1":
            asignar_rutas()
        elif opcion == "2":
            analisis_empirico()
        elif opcion == "3":
            print("\nGracias por usar el programa. ¡Goodbye!\n")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.\n")


if __name__ == "__main__":
    menu()
