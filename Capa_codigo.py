import time
import math
import tracemalloc
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# PARTE I - ALGORITMO PRINCIPAL: ASIGNACIÓN DE RUTAS DE ENTREGA
# =============================================================================
def asignar_rutas():
    print("\n" + "="*80)
    print(" ALGORITMO PRINCIPAL: ASIGNACIÓN DE RUTAS DE ENTREGA ")
    print("="*80)

    # Entradas del usuario
    n = int(input("Ingrese el número de puntos de entrega: "))

    print("\nIngrese la matriz de distancias (en kilómetros):")
    matriz = []
    for i in range(n):
        fila = list(map(int, input(f"Fila {i} (separe las distancias con espacio): ").split()))
        matriz.append(fila)

    capacidad = int(input("\nCapacidad máxima de paquetes por conductor: "))
    total_paquetes = int(input("Cantidad total de paquetes a distribuir: "))

    num_conductores = math.ceil(total_paquetes / capacidad)
    paquetes_restantes = total_paquetes

    print("\n--- RESULTADOS DE ASIGNACIÓN DE RUTAS ---")
    for c in range(num_conductores):
        if paquetes_restantes >= capacidad:
            paquetes = capacidad
        else:
            paquetes = paquetes_restantes
        paquetes_restantes -= paquetes

        # Asignación secuencial
        inicio = 0
        fin = min(n - 1, (c + 1) * paquetes - 1)

        distancia_total = 0
        for i in range(inicio, fin):
            distancia_total += matriz[i][i + 1]
        distancia_total += matriz[fin][0]  # retorno al origen

        print(f"\nConductor {c + 1}:")
        print(f"  Paquetes asignados: {paquetes}")
        print(f"  Ruta: {list(range(inicio, fin + 1)) + [0]}")
        print(f"  Distancia total recorrida: {distancia_total} km")

    print("\nAsignación completada correctamente.\n")


# =============================================================================
# PARTE II - ANÁLISIS EMPÍRICO DE COMPLEJIDAD
# =============================================================================
def asignar_rutas_automatico(n):
    """Versión automática para medición empírica."""
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


def medir_tiempo_memoria(funcion, *args):
    """Mide tiempo y memoria de ejecución."""
    tracemalloc.start()
    inicio = time.time()
    funcion(*args)
    fin = time.time()
    _, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return (fin - inicio) * 1000, memoria_pico / (1024 * 1024)


def analisis_empirico():
    print("\n" + "="*80)
    print(" ANÁLISIS EMPÍRICO DE COMPLEJIDAD DEL ALGORITMO DE RUTAS ")
    print("="*80)

    tamanos = [50, 100, 500, 1000, 2000, 3000]
    tiempos = []
    memorias = []

    for n in tamanos:
        tiempo_ms, memoria_mb = medir_tiempo_memoria(asignar_rutas_automatico, n)
        tiempos.append(tiempo_ms)
        memorias.append(memoria_mb)
        print(f"n={n} → Tiempo: {tiempo_ms:.2f} ms | Memoria: {memoria_mb:.4f} MB")

    generar_grafico_interactivo(tamanos, tiempos, memorias)
    print("\nAnálisis empírico completado. Archivo HTML generado.\n")


# =============================================================================
# PARTE III - GRÁFICO INTERACTIVO (Plotly HTML con diseño tipo Lab7)
# =============================================================================
def generar_grafico_interactivo(tamanos, tiempos, memorias):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Complejidad Temporal", "Complejidad Espacial"),
        horizontal_spacing=0.12
    )

    # Gráfica de tiempo
    fig.add_trace(
        go.Scatter(
            x=tamanos, y=tiempos, mode="lines+markers",
            name="Tiempo (ms)", line=dict(color="royalblue", width=4),
            marker=dict(size=10),
            hovertemplate="n: %{x}<br>Tiempo: %{y:.2f} ms<extra></extra>"
        ), row=1, col=1
    )

    # Gráfica de memoria
    fig.add_trace(
        go.Scatter(
            x=tamanos, y=memorias, mode="lines+markers",
            name="Memoria (MB)", line=dict(color="mediumvioletred", width=4),
            marker=dict(size=10),
            hovertemplate="n: %{x}<br>Memoria: %{y:.4f} MB<extra></extra>"
        ), row=1, col=2
    )

    # Configuración general
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
            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
            bgcolor="rgba(255,255,255,0.8)", bordercolor="black", borderwidth=1
        ),
        margin=dict(l=60, r=60, t=100, b=80)
    )

    fig.update_xaxes(title_text="Tamaño de entrada (n)", row=1, col=1)
    fig.update_yaxes(title_text="Tiempo (ms)", row=1, col=1)
    fig.update_xaxes(title_text="Tamaño de entrada (n)", row=1, col=2)
    fig.update_yaxes(title_text="Memoria (MB)", row=1, col=2)

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
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 10px;
        }
        h3 {
            text-align: center;
            color: #666;
            margin-bottom: 40px;
        }
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

    print("\nGráfica guardada en 'analisis_rutas_interactivo.html'.")
    print("Puedes abrirla en tu navegador para visualizar las dos gráficas.\n")


# =============================================================================
# PARTE IV - MENÚ PRINCIPAL
# =============================================================================
def menu():
    while True:
        print("\n" + "="*80)
        print("   PARCIAL II - RUTAS DE ENTREGA CON ANÁLISIS DE COMPLEJIDAD")
        print("="*80)
        print("1) Ejecutar algoritmo principal (entradas manuales)")
        print("2) Ejecutar análisis empírico (gráficas interactivas)")
        print("3) Salir")
        print("="*80)
        opcion = input("Seleccione una opción (1-3): ").strip()

        if opcion == '1':
            asignar_rutas()
        elif opcion == '2':
            analisis_empirico()
        elif opcion == '3':
            print("\nGracias por usar el programa. ¡Hasta pronto!\n")
            break
        else:
            print("\nOpción inválida. Intente nuevamente.\n")


# =============================================================================
# EJECUCIÓN
# =============================================================================
if __name__ == "__main__":
    menu()

