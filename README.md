# PARCIAL II: RUTAS DE ENTREGA CON ANÁLISIS DE COMPLEJIDAD

![Portada del Proyecto](Presentation.jpg)

---

## 📖 Descripción General

Este proyecto fue desarrollado como parte del **Parcial II** de la asignatura *Análisis y Diseño de Algoritmos* de la **Universidad Tecnológica de Panamá**.

Su objetivo principal es **gestionar rutas de entrega** mediante un algoritmo que simula la distribución de paquetes entre varios conductores, y posteriormente **analizar empíricamente la complejidad temporal y espacial** del algoritmo implementado.  
El programa también genera una **visualización interactiva en HTML** que permite explorar el rendimiento en distintas escalas de entrada (*n*).

---

## 🚀 Uso

1. Ejecutar el archivo principal:
   ```bash
   python pr.py
Seleccionar una opción del menú principal:

Copiar código
1) Ejecutar algoritmo principal
2) Consultar rutas y distancias
3) Ejecutar análisis empírico
4) Salir
En la opción 1, el programa:

Genera automáticamente una matriz de distancias.

Permite editar rutas específicas sin reingresar toda la matriz.

Asigna rutas manualmente a los conductores.

Calcula la distancia total por cada conductor.

En la opción 3, el sistema:

Realiza un análisis empírico de complejidad midiendo tiempo y memoria.

Genera el archivo analisis_rutas_interactivo.html, el cual contiene dos gráficas sincronizadas:

Complejidad temporal (tiempo).

Complejidad espacial (memoria).

🧩 Estructura del Código

bash

Copiar código

📁 Proyecto_Rutas_Entrega
│
├── pr.py                          # Archivo principal del programa
├── analisis_rutas_interactivo.html # Gráfico interactivo generado
├── Presentation.jpg               # Imagen de portada
└── README.md                      # Documentación del proyecto

Principales secciones del código:
Generación de matriz automática: crea distancias aleatorias entre puntos.

Edición de matriz: permite modificar valores individuales sin reescribir toda la matriz.

Asignación manual de rutas: asigna rutas específicas a los conductores.

Consulta de rutas: permite consultar distancias y rutas asignadas.

Análisis empírico: mide el rendimiento del algoritmo para distintos tamaños de entrada (n).

Gráficos interactivos: genera visualizaciones sincronizadas de tiempo y memoria con Plotly.

🛠️ Tecnologías Utilizadas
Python 3.12

Plotly – Para la generación de gráficos interactivos.

Math, Random, Time, Tracemalloc – Para el cálculo, simulación y medición de rendimiento.

Autores

Universidad Tecnológica de Panamá

Facultad de Ingeniería de Sistemas Computacionales

Materia: Análisis y Diseño de Algoritmos

Año: 2025

📄 Licencia

Proyecto académico — uso exclusivo con fines educativos.
