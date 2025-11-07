import time
import tracemalloc
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# ALGORITMOS
# =============================================================================
def suma_elementos(arr):
    """Suma todos los elementos de una lista."""
    suma = 0
    for elemento in arr:
        suma += elemento
    return suma

def encontrar_max_min(arr):
    """Encuentra el valor máximo y mínimo en una lista."""
    if len(arr) == 0:
        return None, None
    maximo = arr[0]
    minimo = arr[0]
    for elemento in arr:
        if elemento > maximo:
            maximo = elemento
        if elemento < minimo:
            minimo = elemento
    return maximo, minimo

def contar_pares(arr):
    """Cuenta cuántos pares de elementos existen."""
    contador = 0
    n = len(arr)
    for i in range(n):
        for j in range(i+1, n):
            contador += 1
    return contador

def suma_matriz(n):
    """Crea una matriz de n x n y suma todos sus elementos."""
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            fila.append(i + j)
        matriz.append(fila)
    suma = 0
    for i in range(n):
        for j in range(n):
            suma += matriz[i][j]
    return suma

def medir_tiempo_memoria(funcion, *args):
    """Mide el tiempo de ejecución y memoria de una función."""
    tracemalloc.start()
    mem_inicial, _ = tracemalloc.get_traced_memory()
    inicio = time.time()
    resultado = funcion(*args)
    fin = time.time()
    mem_final, mem_peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    tiempo_s = fin - inicio
    tiempo_ms = tiempo_s * 1000
    memoria_kb = mem_peak / 1024
    return tiempo_s, tiempo_ms, memoria_kb, resultado

# =============================================================================
# ANÁLISIS EMPÍRICO
# =============================================================================
def analisis_empirico():
    """Ejecuta los 4 algoritmos y mide tiempos y memoria."""
    print("\n" + "="*80, flush=True)
    print("  ANÁLISIS EMPÍRICO DE COMPLEJIDAD ALGORÍTMICA", flush=True)
    print("="*80, flush=True)
    
    tamaños = [100, 500, 1000, 2000, 5000, 7000, 10000, 15000]
    
    tiempos_s = {
        'suma_elementos': [],
        'max_min': [],
        'contar_pares': [],
        'suma_matriz': []
    }
    
    tiempos_ms = {
        'suma_elementos': [],
        'max_min': [],
        'contar_pares': [],
        'suma_matriz': []
    }
    
    memorias = {
        'suma_elementos': [],
        'max_min': [],
        'contar_pares': [],
        'suma_matriz': []
    }
    
    print("\nEjecutando análisis empírico...", flush=True)
    print("ADVERTENCIA: Los algoritmos O(n²) pueden tardar con tamaños grandes\n", flush=True)
    
    for n in tamaños:
        print(f"Procesando tamaño n = {n}...", flush=True)
        arr = list(range(n))
        
        # 1. Suma de Elementos
        t_s, t_ms, mem, _ = medir_tiempo_memoria(suma_elementos, arr)
        tiempos_s['suma_elementos'].append(t_s)
        tiempos_ms['suma_elementos'].append(t_ms)
        memorias['suma_elementos'].append(mem)
        
        # 2. Encontrar Max/Min
        t_s, t_ms, mem, _ = medir_tiempo_memoria(encontrar_max_min, arr)
        tiempos_s['max_min'].append(t_s)
        tiempos_ms['max_min'].append(t_ms)
        memorias['max_min'].append(mem)
        
        # 3. Contar Pares (solo hasta n=5000)
        if n <= 5000:
            t_s, t_ms, mem, _ = medir_tiempo_memoria(contar_pares, arr)
            tiempos_s['contar_pares'].append(t_s)
            tiempos_ms['contar_pares'].append(t_ms)
            memorias['contar_pares'].append(mem)
        else:
            tiempos_s['contar_pares'].append(None)
            tiempos_ms['contar_pares'].append(None)
            memorias['contar_pares'].append(None)
        
        # 4. Suma de Matriz (solo hasta n=5000)
        if n <= 5000:
            t_s, t_ms, mem, _ = medir_tiempo_memoria(suma_matriz, n)
            tiempos_s['suma_matriz'].append(t_s)
            tiempos_ms['suma_matriz'].append(t_ms)
            memorias['suma_matriz'].append(mem)
        else:
            tiempos_s['suma_matriz'].append(None)
            tiempos_ms['suma_matriz'].append(None)
            memorias['suma_matriz'].append(None)
    
    # Imprimir resultados
    print("\n" + "="*80, flush=True)
    print("RESULTADOS DEL ANÁLISIS EMPÍRICO", flush=True)
    print("="*80, flush=True)
    print(f"{'Tamaño (n)':<12} {'Algoritmo':<25} {'Tiempo (s)':<15} {'Tiempo (ms)':<15} {'Memoria (KB)':<15}", flush=True)
    print("-"*80, flush=True)
    
    for i, n in enumerate(tamaños):
        print(f"{n:<12} {'Suma de Elementos':<25} {tiempos_s['suma_elementos'][i]:<15.9f} "
              f"{tiempos_ms['suma_elementos'][i]:<15.6f} {memorias['suma_elementos'][i]:<15.2f}", flush=True)
        print(f"{'':<12} {'Encontrar Max/Min':<25} {tiempos_s['max_min'][i]:<15.9f} "
              f"{tiempos_ms['max_min'][i]:<15.6f} {memorias['max_min'][i]:<15.2f}", flush=True)
        
        if tiempos_s['contar_pares'][i] is not None:
            print(f"{'':<12} {'Contar Pares':<25} {tiempos_s['contar_pares'][i]:<15.9f} "
                  f"{tiempos_ms['contar_pares'][i]:<15.6f} {memorias['contar_pares'][i]:<15.2f}", flush=True)
        else:
            print(f"{'':<12} {'Contar Pares':<25} {'N/A':<15} {'N/A':<15} {'N/A':<15}", flush=True)
        
        if tiempos_s['suma_matriz'][i] is not None:
            print(f"{'':<12} {'Suma de Matriz':<25} {tiempos_s['suma_matriz'][i]:<15.9f} "
                  f"{tiempos_ms['suma_matriz'][i]:<15.6f} {memorias['suma_matriz'][i]:<15.2f}", flush=True)
        else:
            print(f"{'':<12} {'Suma de Matriz':<25} {'N/A':<15} {'N/A':<15} {'N/A':<15}", flush=True)
        print("-"*80, flush=True)
    
    print("="*80 + "\n", flush=True)
    
    generar_graficas_interactivas(tamaños, tiempos_s, memorias)
    return tamaños, tiempos_s, tiempos_ms, memorias

# =============================================================================
# GENERACIÓN DE GRÁFICAS
# =============================================================================
def generar_graficas_interactivas(tamaños, tiempos, memorias):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=('<b>Complejidad Temporal</b>', '<b>Complejidad Espacial</b>'),
        horizontal_spacing=0.10
    )
    
    # GRÁFICA 1: COMPLEJIDAD TEMPORAL
    fig.add_trace(
        go.Scatter(
            x=tamaños, 
            y=tiempos['suma_elementos'],
            mode='lines+markers',
            name='Suma de Elementos O(n)',
            line=dict(color='blue', width=3),
            marker=dict(size=10),
            legendgroup='suma',
            hovertemplate='<b>Suma de Elementos</b><br>n: %{x}<br>Tiempo: %{y:.9f}s<extra></extra>'
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=tamaños, 
            y=tiempos['max_min'],
            mode='lines+markers',
            name='Encontrar Max/Min O(n)',
            line=dict(color='green', width=3),
            marker=dict(size=10),
            legendgroup='maxmin',
            hovertemplate='<b>Encontrar Max/Min</b><br>n: %{x}<br>Tiempo: %{y:.9f}s<extra></extra>'
        ),
        row=1, col=1
    )
    
    tamaños_pares = [t for i, t in enumerate(tamaños) if tiempos['contar_pares'][i] is not None]
    tiempos_pares = [t for t in tiempos['contar_pares'] if t is not None]
    fig.add_trace(
        go.Scatter(
            x=tamaños_pares, 
            y=tiempos_pares,
            mode='lines+markers',
            name='Contar Pares O(n²)',
            line=dict(color='red', width=3),
            marker=dict(size=10),
            legendgroup='pares',
            hovertemplate='<b>Contar Pares</b><br>n: %{x}<br>Tiempo: %{y:.9f}s<extra></extra>'
        ),
        row=1, col=1
    )
    
    tamaños_matriz = [t for i, t in enumerate(tamaños) if tiempos['suma_matriz'][i] is not None]
    tiempos_matriz = [t for t in tiempos['suma_matriz'] if t is not None]
    fig.add_trace(
        go.Scatter(
            x=tamaños_matriz, 
            y=tiempos_matriz,
            mode='lines+markers',
            name='Suma de Matriz O(n²)',
            line=dict(color='purple', width=3),
            marker=dict(size=10),
            legendgroup='matriz',
            hovertemplate='<b>Suma de Matriz</b><br>n: %{x}<br>Tiempo: %{y:.9f}s<extra></extra>'
        ),
        row=1, col=1
    )
    
    # GRÁFICA 2: COMPLEJIDAD ESPACIAL
    fig.add_trace(
        go.Scatter(
            x=tamaños, 
            y=memorias['suma_elementos'],
            mode='lines+markers',
            name='Suma de Elementos O(n)',
            line=dict(color='blue', width=3),
            marker=dict(size=10),
            legendgroup='suma',
            showlegend=False,
            hovertemplate='<b>Suma de Elementos</b><br>n: %{x}<br>Memoria: %{y:.2f} KB<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.add_trace(
        go.Scatter(
            x=tamaños, 
            y=memorias['max_min'],
            mode='lines+markers',
            name='Encontrar Max/Min O(n)',
            line=dict(color='green', width=3),
            marker=dict(size=10),
            legendgroup='maxmin',
            showlegend=False,
            hovertemplate='<b>Encontrar Max/Min</b><br>n: %{x}<br>Memoria: %{y:.2f} KB<extra></extra>'
        ),
        row=1, col=2
    )
    
    memorias_pares = [m for m in memorias['contar_pares'] if m is not None]
    fig.add_trace(
        go.Scatter(
            x=tamaños_pares, 
            y=memorias_pares,
            mode='lines+markers',
            name='Contar Pares O(n²)',
            line=dict(color='red', width=3),
            marker=dict(size=10),
            legendgroup='pares',
            showlegend=False,
            hovertemplate='<b>Contar Pares</b><br>n: %{x}<br>Memoria: %{y:.2f} KB<extra></extra>'
        ),
        row=1, col=2
    )
    
    memorias_matriz = [m for m in memorias['suma_matriz'] if m is not None]
    fig.add_trace(
        go.Scatter(
            x=tamaños_matriz, 
            y=memorias_matriz,
            mode='lines+markers',
            name='Suma de Matriz O(n²)',
            line=dict(color='purple', width=3),
            marker=dict(size=10),
            legendgroup='matriz',
            showlegend=False,
            hovertemplate='<b>Suma de Matriz</b><br>n: %{x}<br>Memoria: %{y:.2f} KB<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig.update_xaxes(
        title_text="<b>Tamaño de entrada (n)</b>", 
        title_font=dict(size=14),
        tickfont=dict(size=12),
        row=1, col=1
    )
    fig.update_xaxes(
        title_text="<b>Tamaño de entrada (n)</b>", 
        title_font=dict(size=14),
        tickfont=dict(size=12),
        row=1, col=2
    )
    
    fig.update_yaxes(
        title_text="<b>Tiempo (segundos)</b>", 
        type="log", 
        title_font=dict(size=14),
        tickfont=dict(size=12),
        row=1, col=1
    )
    
    fig.update_yaxes(
        title_text="<b>Memoria pico usada (KB)</b>", 
        title_font=dict(size=14),
        tickfont=dict(size=12),
        row=1, col=2
    )
    
    fig.update_layout(
        title={
            'text': "<b>Análisis de Complejidad: Teórico vs. Empírico</b><br>" +
                    "<sub>Click en la leyenda para ocultar/mostrar líneas en AMBAS gráficas | Hover para detalles</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18}
        },
        height=700,
        width=1600,
        hovermode='closest',
        template='plotly_white',
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=1.02,
            font=dict(size=12),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="Black",
            borderwidth=2
        ),
        margin=dict(l=80, r=200, t=120, b=80)
    )
    
    html_content = fig.to_html(include_plotlyjs='cdn')
    
    css_style = """
    <style>
        body {
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 30px;
            max-width: 1700px;
            width: 100%;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #667eea;
        }
        
        .header h1 {
            color: #333;
            font-size: 28px;
            margin: 0 0 10px 0;
            font-weight: 700;
        }
        
        .header p {
            color: #666;
            font-size: 14px;
            margin: 5px 0;
        }
        
        .plotly-graph-div {
            margin: 0 auto;
            display: block;
        }
        
        .info-box {
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            padding: 15px 20px;
            margin-top: 20px;
            border-radius: 8px;
        }
        
        .info-box h3 {
            margin: 0 0 10px 0;
            color: #667eea;
            font-size: 16px;
        }
        
        .info-box ul {
            margin: 0;
            padding-left: 20px;
            color: #555;
        }
        
        .info-box li {
            margin: 5px 0;
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #888;
            font-size: 12px;
        }
    </style>
    """
    
    html_mejorado = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Análisis de Complejidad Algorítmica</title>
        {css_style}
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Análisis de Complejidad: Teórico vs. Empírico</h1>
                <p>Laboratorio de Análisis y Diseño de Algoritmos</p>
                <p style="color: #667eea; font-weight: 600;">Universidad Tecnológica de Panamá</p>
            </div>
            
            {html_content.split('<body>')[1].split('</body>')[0]}
            
            <div class="info-box">
                <h3>Instrucciones de Interactividad</h3>
                <ul>
                    <li><strong>Click en la leyenda:</strong> Oculta/muestra líneas en ambas gráficas simultáneamente</li>
                    <li><strong>Hover sobre puntos:</strong> Muestra información detallada de cada medición</li>
                    <li><strong>Zoom:</strong> Arrastra para hacer zoom en una región específica</li>
                    <li><strong>Pan:</strong> Doble click para resetear la vista</li>
                </ul>
            </div>
            
            <div class="info-box" style="border-left-color: #28a745;">
                <h3>Complejidades Analizadas</h3>
                <ul>
                    <li><strong style="color: blue;">Suma de Elementos O(n):</strong> Complejidad lineal</li>
                    <li><strong style="color: green;">Encontrar Max/Min O(n):</strong> Complejidad lineal</li>
                    <li><strong style="color: red;">Contar Pares O(n²):</strong> Complejidad cuadrática</li>
                    <li><strong style="color: purple;">Suma de Matriz O(n²):</strong> Complejidad cuadrática</li>
                </ul>
            </div>
            
            <div class="footer">
                <p>Generado automáticamente por el sistema de análisis de complejidad algorítmica</p>
                <p>2025 - Laboratorio de Algoritmos y Estructura de Datos</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open('analisis_complejidad_interactivo.html', 'w', encoding='utf-8') as f:
        f.write(html_mejorado)
    
    print("\nGráfica interactiva con diseño mejorado guardada en 'analisis_complejidad_interactivo.html'", flush=True)
    print("Abre el archivo HTML manualmente desde tu explorador de archivos\n", flush=True)

# =============================================================================
# MENÚ PRINCIPAL
# =============================================================================
def menu():
    while True:
        print("\n" + "="*80, flush=True)
        print("  LABORATORIO N.7: ANÁLISIS DE COMPLEJIDAD TEÓRICO vs. EMPÍRICO", flush=True)
        print("="*80, flush=True)
        print("  1) Ver Algoritmo 1: Suma de Elementos", flush=True)
        print("  2) Ver Algoritmo 2: Encontrar Máximo y Mínimo", flush=True)
        print("  3) Ver Algoritmo 3: Contar Pares de Elementos", flush=True)
        print("  4) Ver Algoritmo 4: Suma de Matriz", flush=True)
        print("  5) Ejecutar Análisis Empírico Completo (GRÁFICAS INTERACTIVAS)", flush=True)
        print("  6) Salir", flush=True)
        print("="*80, flush=True)
        
        opcion = input("\nSeleccione una opción (1-6): ").strip()
        
        if opcion == '1':
            print("\n--- ALGORITMO 1: SUMA DE ELEMENTOS ---", flush=True)
            print("Complejidad Teórica: O(n)", flush=True)
            arr_test = list(range(1000))
            t_s, t_ms, mem, resultado = medir_tiempo_memoria(suma_elementos, arr_test)
            print(f"Resultado: La suma es {resultado}", flush=True)
            print(f"Tiempo: {t_s:.9f} segundos ({t_ms:.6f} milisegundos)", flush=True)
            print(f"Memoria: {mem:.2f} KB", flush=True)
            
        elif opcion == '2':
            print("\n--- ALGORITMO 2: ENCONTRAR MÁXIMO Y MÍNIMO ---", flush=True)
            print("Complejidad Teórica: O(n)", flush=True)
            arr_test = list(range(1000))
            t_s, t_ms, mem, resultado = medir_tiempo_memoria(encontrar_max_min, arr_test)
            print(f"Resultado: Max={resultado[0]}, Min={resultado[1]}", flush=True)
            print(f"Tiempo: {t_s:.9f} segundos ({t_ms:.6f} milisegundos)", flush=True)
            print(f"Memoria: {mem:.2f} KB", flush=True)
            
        elif opcion == '3':
            print("\n--- ALGORITMO 3: CONTAR PARES DE ELEMENTOS ---", flush=True)
            print("Complejidad Teórica: O(n²)", flush=True)
            arr_test = list(range(100))
            t_s, t_ms, mem, resultado = medir_tiempo_memoria(contar_pares, arr_test)
            print(f"Resultado: {resultado} pares encontrados", flush=True)
            print(f"Tiempo: {t_s:.9f} segundos ({t_ms:.6f} milisegundos)", flush=True)
            print(f"Memoria: {mem:.2f} KB", flush=True)
            
        elif opcion == '4':
            print("\n--- ALGORITMO 4: SUMA DE MATRIZ ---", flush=True)
            print("Complejidad Teórica: O(n²)", flush=True)
            t_s, t_ms, mem, resultado = medir_tiempo_memoria(suma_matriz, 100)
            print(f"Resultado: Suma de matriz = {resultado}", flush=True)
            print(f"Tiempo: {t_s:.9f} segundos ({t_ms:.6f} milisegundos)", flush=True)
            print(f"Memoria: {mem:.2f} KB", flush=True)
            
        elif opcion == '5':
            analisis_empirico()
            
        elif opcion == '6':
            print("\n¡Gracias por usar el programa! Hasta pronto.\n", flush=True)
            break
            
        else:
            print("\nOpción inválida. Seleccione 1-6.", flush=True)
        
        input("\nPresione ENTER para continuar...")

if __name__ == "__main__":
    menu()
