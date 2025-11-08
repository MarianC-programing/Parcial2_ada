import math
import random
import time
import tracemalloc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Variables globales para almacenar la matriz, tamaño y rutas
matriz_global = None
n_global = None
rutas_asignadas_global = None


# =============================================================================
# PARTE I - ALGORITMO PRINCIPAL: ASIGNACIÓN DE RUTAS DE ENTREGA
# =============================================================================
def generar_matriz_automatica(n):
    """Genera una matriz aleatoria de distancias."""
    return [[random.randint(1, 20) if i != j else 0 for j in range(n)] for i in range(n)]


def mostrar_matriz(matriz):
    n = len(matriz)
    print("\nMatriz de distancias (en kilómetros):")
    
    # Imprimir encabezado
    print("   De/A", end="")
    for i in range(n):
        print(f" {i:3}", end="")
    print()  # Nueva línea
    
    # Imprimir filas con índices
    for i in range(n):
        print(f"     {i}", end="")  # Índice de fila
        for j in range(n):
            print(f" {matriz[i][j]:3}", end="")
        print()


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
    global matriz_global, n_global, rutas_asignadas_global

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
    rutas_asignadas_global = asignar_rutas_manual(num_conductores, n_global)

    print("\n--- RESULTADOS DE ASIGNACIÓN DE RUTAS ---")
    for c in range(num_conductores):
        paquetes = capacidad if paquetes_restantes >= capacidad else paquetes_restantes
        paquetes_restantes -= paquetes

        inicio = 0
        fin = min(n_global - 1, (c + 1) * paquetes - 1)

        distancia_total = sum(matriz_global[i][i + 1] for i in range(inicio, fin))
        distancia_total += matriz_global[fin][0]

        ruta_asignada = rutas_asignadas_global.get(c + 1, list(range(inicio, fin + 1)) + [0])
        print(f"\nConductor {c + 1}:")
        print(f"  Paquetes asignados: {paquetes}")
        print(f"  Ruta: [{' → '.join(map(str, ruta_asignada))}]")
        
        # Calcular distancia total para la ruta asignada
        distancia_total = 0
        for i in range(len(ruta_asignada) - 1):
            origen = ruta_asignada[i]
            destino = ruta_asignada[i + 1]
            distancia_total += matriz_global[origen][destino]
            
        print(f"  Distancia total recorrida: {distancia_total} km")

    print("\nAsignación completada correctamente.\n")


# =============================================================================
# CONSULTA DE RUTAS
# =============================================================================
def encontrar_mejor_ruta(origen, destino, matriz):
    """Encuentra la mejor ruta entre dos puntos usando todos los puntos intermedios posibles."""
    n = len(matriz)
    puntos_intermedios = [i for i in range(n) if i != origen and i != destino]
    mejor_ruta = None
    menor_distancia = float('inf')
    
    # Probar todas las posibles combinaciones de puntos intermedios
    from itertools import permutations
    for permutacion in permutations(puntos_intermedios):
        ruta_actual = [origen] + list(permutacion) + [destino]
        distancia_actual = sum(matriz[ruta_actual[i]][ruta_actual[i+1]] 
                             for i in range(len(ruta_actual)-1))
        
        if distancia_actual < menor_distancia:
            menor_distancia = distancia_actual
            mejor_ruta = ruta_actual
            
    return mejor_ruta, menor_distancia

def consultar_rutas():
    if matriz_global is None:
        print("\n No hay matriz generada. Primero ejecute el algoritmo principal.")
        return
        
    print("\n" + "=" * 80)
    print(" CONSULTA DE RUTAS Y DISTANCIAS ")
    print("=" * 80)
    
    mostrar_matriz(matriz_global)
    
    while True:
        print("\n=== OPCIONES DE CONSULTA ===")
        print("1) Consultar ruta específica entre dos puntos")
        print("2) Ver todas las rutas y distancias")
        print("3) Volver al menú principal")
        
        opcion = input("\nSeleccione una opción (1-3): ").strip()
        
        if opcion == "1":
            try:
                print("\nConsulta de ruta específica")
                print("Puntos disponibles:", ", ".join(map(str, range(n_global))))
                origen = int(input("Ingrese el punto de origen: "))
                destino = int(input("Ingrese el punto de destino: "))
                
                if origen < 0 or destino < 0 or origen >= n_global or destino >= n_global:
                    print(" Puntos inválidos. Deben estar entre 0 y", n_global-1)
                    continue
                    
                # Encontrar la mejor ruta entre los puntos
                mejor_ruta, distancia = encontrar_mejor_ruta(origen, destino, matriz_global)
                
                print("\n=== RESULTADO DE LA CONSULTA ===")
                print(f"Mejor ruta encontrada: {' → '.join(map(str, mejor_ruta))}")
                print(f"Distancia total: {distancia} km")
                
                # Mostrar el desglose de la ruta
                print("\nDesglose de la ruta:")
                for i in range(len(mejor_ruta)-1):
                    punto_actual = mejor_ruta[i]
                    punto_siguiente = mejor_ruta[i+1]
                    distancia_tramo = matriz_global[punto_actual][punto_siguiente]
                    print(f"  {punto_actual} → {punto_siguiente}: {distancia_tramo} km")
                
            except ValueError:
                print(" Por favor, ingrese números válidos.")
                
        elif opcion == "2":
            if rutas_asignadas_global:
                print("\n=== RUTAS ASIGNADAS ===")
                total_km_asignados = 0
                
                for conductor, ruta in rutas_asignadas_global.items():
                    distancia = sum(matriz_global[ruta[i]][ruta[i+1]] 
                                  for i in range(len(ruta)-1))
                    total_km_asignados += distancia
                    print(f"\nConductor {conductor}:")
                    print(f"  Ruta: {' → '.join(map(str, ruta))}")
                    print(f"  Distancia total: {distancia} km")
                
                print(f"\nTotal kilómetros en rutas asignadas: {total_km_asignados} km")
                
                # Mostrar rutas no asignadas
                print("\n=== RUTAS NO ASIGNADAS ===")
                rutas_asignadas_nums = {ruta[1] for ruta in rutas_asignadas_global.values() 
                                      if len(ruta) > 2}
                
                total_km_no_asignados = 0
                for i in range(n_global):
                    if i not in rutas_asignadas_nums:
                        puntos = list(range(n_global))
                        puntos.pop(i)
                        ruta = [0] + puntos + [0]
                        distancia = sum(matriz_global[ruta[j]][ruta[j+1]] 
                                      for j in range(len(ruta)-1))
                        total_km_no_asignados += distancia
                        print(f"\nRuta {i + 1}:")
                        print(f"  Secuencia: {' → '.join(map(str, ruta))}")
                        print(f"  Distancia: {distancia} km")
                
                print(f"\nTotal kilómetros en rutas no asignadas: {total_km_no_asignados} km")
                print(f"Total kilómetros global: {total_km_asignados + total_km_no_asignados} km")
            else:
                print("\n No hay rutas asignadas todavía.")
                mostrar_rutas_disponibles(n_global)
                
        elif opcion == "3":
            break
            
        else:
            print("\n Opción inválida. Por favor, seleccione 1, 2 o 3.")

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
    import time
    import tracemalloc
    import math
    import random

    print("\n" + "=" * 80)
    print(" ANÁLISIS EMPÍRICO DE COMPLEJIDAD DEL ALGORITMO DE RUTAS ")
    print("=" * 80)

    # Tamaños de entrada que se analizarán
    tamanos = [50, 100, 500, 1000, 2000, 3000]

    # Diccionarios para almacenar los resultados
    tiempos_por_n = {}
    memorias_por_n = {}

    # Función automática para medir rendimiento
    def asignar_rutas_automatico(n):
        matriz = [[random.randint(1, 20) if i != j else 0 for j in range(n)] for i in range(n)]
        capacidad = 3
        total_paquetes = n // 2
        num_conductores = math.ceil(total_paquetes / capacidad)
        paquetes_restantes = total_paquetes

        for c in range(num_conductores):
            if paquetes_restantes >= capacidad:
                paquetes = capacidad
            else:
                paquetes = paquetes_restantes
            paquetes_restantes -= paquetes

            inicio = 0
            fin = min(n - 1, (c + 1) * paquetes - 1)
            distancia_total = 0
            for i in range(inicio, fin):
                distancia_total += matriz[i][i + 1]
            distancia_total += matriz[fin][0]
        return distancia_total

    # Medición de tiempo y memoria
    def medir_tiempo_memoria(funcion, *args):
        tracemalloc.start()
        inicio = time.time()
        funcion(*args)
        fin = time.time()
        _, memoria_pico = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return (fin - inicio) * 1000, memoria_pico / (1024 * 1024)

    # === Bucle de análisis ===
    for n in tamanos:
        tiempos_n = []
        memorias_n = []

        # Ejecuta varias veces para obtener promedios más estables
        for _ in range(5):
            tiempo_ms, memoria_mb = medir_tiempo_memoria(asignar_rutas_automatico, n)
            tiempos_n.append(tiempo_ms)
            memorias_n.append(memoria_mb)

        tiempos_por_n[n] = tiempos_n
        memorias_por_n[n] = memorias_n

        print(f"n={n} → Tiempo medio: {sum(tiempos_n)/len(tiempos_n):.2f} ms | "
              f"Memoria media: {sum(memorias_n)/len(memorias_n):.4f} MB")
    # === Generar gráfico interactivo sincronizado ===
    generar_grafico_interactivo(tamanos, tiempos_por_n, memorias_por_n)

    print("\n Análisis empírico completado. Archivo HTML generado correctamente.\n")


# =============================================================================
# PARTE III - GRÁFICO INTERACTIVO 
# =============================================================================
def generar_grafico_interactivo(tamanos, tiempos_por_n, memorias_por_n):
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    colores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Complejidad Temporal", "Complejidad Espacial"),
        horizontal_spacing=0.12
    )

    # === GRÁFICA DE TIEMPO ===
    for i, n in enumerate(tamanos):
        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(tiempos_por_n[n]) + 1)),
                y=tiempos_por_n[n],
                mode="lines+markers",
                name=f"n={n}",
                legendgroup=f"grupo{n}",  # grupo común
                line=dict(color=colores[i % len(colores)], width=3),
                marker=dict(size=8),
                hovertemplate="Iteración %{x}<br>Tiempo: %{y:.2f} ms<extra></extra>"
            ),
            row=1, col=1
        )

    # === GRÁFICA DE MEMORIA ===
    for i, n in enumerate(tamanos):
        fig.add_trace(
            go.Scatter(
                x=list(range(1, len(memorias_por_n[n]) + 1)),
                y=memorias_por_n[n],
                mode="lines+markers",
                name=f"n={n}",
                legendgroup=f"grupo{n}",  
                showlegend=False, 
                line=dict(color=colores[i % len(colores)], width=3),
                marker=dict(size=8),
                hovertemplate="Iteración %{x}<br>Memoria: %{y:.4f} MB<extra></extra>"
            ),
            row=1, col=2
        )

    # === CONFIGURACIÓN ===
    fig.update_layout(
        title=dict(
            text="<b>Análisis Empírico del Algoritmo de Rutas</b><br><sub>Universidad Tecnológica de Panamá</sub>",
            x=0.5, font=dict(size=20)
        ),
        hovermode="x unified",
        template="plotly_white",
        height=700,
        width=1500,
        legend=dict(
            title="Tamaño n",
            orientation="h",
            yanchor="bottom",
            y=-0.18,
            xanchor="center",
            x=0.5,
            groupclick="togglegroup",  
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="black",
            borderwidth=1
        ),
        margin=dict(l=60, r=60, t=100, b=80)
    )

    fig.update_xaxes(title_text="Iteraciones", row=1, col=1)
    fig.update_yaxes(title_text="Tiempo (ms)", row=1, col=1)
    fig.update_xaxes(title_text="Iteraciones", row=1, col=2)
    fig.update_yaxes(title_text="Memoria (MB)", row=1, col=2)

    # === Guardar HTML ===
    html = fig.to_html(full_html=False, include_plotlyjs='cdn')
    estilo = """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            max-width: 1600px;
            margin: auto;
        }
        h1 { text-align: center; margin-bottom: 10px; }
        h3 { text-align: center; margin-bottom: 40px; color: #555; }
        .footer {
            text-align: center;
            color: #999;
            font-size: 12px;
            margin-top: 30px;
            border-top: 1px solid #ccc;
            padding-top: 10px;
        }
    </style>
    """
    html_final = f"""
    <!DOCTYPE html>
    <html lang='es'>
    <head><meta charset='UTF-8'><title>Análisis Empírico</title>{estilo}</head>
    <body>
        <div class='container'>
            <h1>Parcial II - Rutas de Entrega</h1>
            <h3>Gráficas Interactivas de Complejidad Temporal y Espacial</h3>
            {html}
            <div class='footer'>
                <p>Facultad de Ingeniería de Sistemas Computacionales — Universidad Tecnológica de Panamá</p>
                <p>Curso: Análisis y Diseño de Algoritmos — 2025</p>
            </div>
        </div>
    </body>
    </html>
    """

    with open("analisis_rutas_interactivo.html", "w", encoding="utf-8") as f:
        f.write(html_final)

    print("\n Gráfica sincronizada guardada en 'analisis_rutas_interactivo.html'.")
    print("Al ocultar una línea en una gráfica, también se ocultará en la otra.\n")

# ===============================================================
# MENÚ PRINCIPAL
# ===============================================================
def menu():
    while True:
        print("\n" + "=" * 80)
        print("   PARCIAL II - RUTAS DE ENTREGA CON ANÁLISIS DE COMPLEJIDAD")
        print("=" * 80)
        print("1) Ejecutar algoritmo principal")
        print("2) Consultar rutas y distancias")
        print("3) Ejecutar análisis empírico")
        print("4) Salir")
        print("=" * 80)
        opcion = input("Seleccione una opción (1-4): ").strip()

        if opcion == "1":
            asignar_rutas()
        elif opcion == "2":
            consultar_rutas()
        elif opcion == "3":
            analisis_empirico()
        elif opcion == "4":
            print("\nGracias por usar el programa. ¡Goodbye!\n")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.\n")


if __name__ == "__main__":
    menu()
