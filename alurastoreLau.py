# ==============================================================================
# Script de Análisis de Datos para el Desafío de Alura Store
# Este script carga datos de ventas de 4 tiendas, los analiza y genera
# visualizaciones para ayudar al Sr. Juan a tomar una decisión.
# ==============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import sys

# URLs de los archivos CSV de las tiendas
# Estos enlaces se usan para cargar los datos directamente desde GitHub
url_tienda1 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_1%20.csv"
url_tienda2 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_2.csv"
url_tienda3 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_3.csv"
url_tienda4 = "https://raw.githubusercontent.com/alura-es-cursos/challenge1-data-science-latam/refs/heads/main/base-de-datos-challenge1-latam/tienda_4.csv"

# --- Parte 1: Carga y Preparación de Datos ---
try:
    print("Cargando datos desde URLs...")
    # Cargar cada archivo CSV en un DataFrame de pandas
    df_tienda1 = pd.read_csv(url_tienda1)
    df_tienda2 = pd.read_csv(url_tienda2)
    df_tienda3 = pd.read_csv(url_tienda3)
    df_tienda4 = pd.read_csv(url_tienda4)
    print("Datos cargados exitosamente.")

except Exception as e:
    print(f"Error al cargar los datos desde las URLs: {e}", file=sys.stderr)
    print("Asegúrate de tener conexión a Internet y que las URLs sean correctas.", file=sys.stderr)
    # Si la carga falla, el script se detiene para evitar errores posteriores.
    sys.exit(1)

# Añadir una columna 'Tienda' a cada DataFrame para identificar el origen de los datos
df_tienda1['Tienda'] = 'Tienda 1'
df_tienda2['Tienda'] = 'Tienda 2'
df_tienda3['Tienda'] = 'Tienda 3'
df_tienda4['Tienda'] = 'Tienda 4'

# Concatenar todos los DataFrames en uno solo para facilitar el análisis global
df_all_stores = pd.concat([df_tienda1, df_tienda2, df_tienda3, df_tienda4], ignore_index=True)

# Convertir la columna 'Fecha de Compra' a formato de fecha
df_all_stores['Fecha de Compra'] = pd.to_datetime(df_all_stores['Fecha de Compra'], format='%d/%m/%Y')

# --- Parte 2: Análisis de Métricas Clave ---

print("\nRealizando el análisis de métricas clave...")

# Calcular los ingresos totales de cada tienda (usando la columna 'Precio')
total_revenue_per_store = df_all_stores.groupby('Tienda')['Precio'].sum().sort_values(ascending=False)

# Calcular la calificación promedio de cada tienda
average_rating_per_store = df_all_stores.groupby('Tienda')['Calificación'].mean().sort_values(ascending=False)

# Calcular el costo de envío promedio de cada tienda
average_shipping_cost_per_store = df_all_stores.groupby('Tienda')['Costo de envío'].mean().sort_values(ascending=False)

# Identificar las top 3 categorías más vendidas (en ingresos) por tienda
top_categories_per_store = df_all_stores.groupby(['Tienda', 'Categoría del Producto'])['Precio'].sum().reset_index()
top_categories_per_store = top_categories_per_store.sort_values(['Tienda', 'Precio'], ascending=False).groupby('Tienda').head(3)

# Identificar los top 3 productos más vendidos (en ingresos) por tienda
top_products_per_store = df_all_stores.groupby(['Tienda', 'Producto'])['Precio'].sum().reset_index()
top_products_per_store = top_products_per_store.sort_values(['Tienda', 'Precio'], ascending=False).groupby('Tienda').head(3)

# --- Parte 3: Impresión de Resultados y Recomendación ---

print("\n--- Resultados del Análisis ---")
print("\nIngresos Totales por Tienda:")
print(total_revenue_per_store)
print("\nCalificación Promedio por Tienda:")
print(average_rating_per_store)
print("\nCosto de Envío Promedio por Tienda:")
print(average_shipping_cost_per_store)
print("\nTop 3 Categorías más Vendidas (por ingresos) por Tienda:")
print(top_categories_per_store)
print("\nTop 3 Productos más Vendidos (por ingresos) por Tienda:")
print(top_products_per_store)

print("\n--- Recomendación para el Sr. Juan ---")
print("Basándonos en el análisis, la Tienda 4 es la que presenta los ingresos totales más bajos.")
print("Aunque tiene el costo de envío más eficiente, su bajo rendimiento en ventas la hace la candidata ideal para vender.")
print("La Tienda 1, a pesar de tener calificaciones más bajas y altos costos de envío, compensa con los ingresos más altos.")
print("Por lo tanto, se recomienda vender la Tienda 4 para capitalizar el capital y reorientar el negocio.")

# --- Parte 4: Visualizaciones de Datos ---

print("\nGenerando visualizaciones...")

# Configurar el estilo de los gráficos con seaborn
sns.set_style("whitegrid")

# Gráfico 1: Ingresos Totales por Tienda
plt.figure(figsize=(10, 6))
sns.barplot(x=total_revenue_per_store.index, y=total_revenue_per_store.values, palette="viridis")
plt.title('Ingresos Totales por Tienda', fontsize=16)
plt.xlabel('Tienda', fontsize=12)
plt.ylabel('Ingresos Totales (COP)', fontsize=12)
plt.ticklabel_format(style='plain', axis='y') # Evita notación científica
plt.tight_layout()
plt.savefig('ingresos_totales_por_tienda.png')
plt.show()
plt.close()

# Gráfico 2: Calificación Promedio por Tienda
plt.figure(figsize=(10, 6))
sns.barplot(x=average_rating_per_store.index, y=average_rating_per_store.values, palette="mako")
plt.title('Calificación Promedio por Tienda', fontsize=16)
plt.xlabel('Tienda', fontsize=12)
plt.ylabel('Calificación Promedio', fontsize=12)
plt.ylim(0, 5) # Establece el rango del eje Y de 0 a 5
plt.tight_layout()
plt.savefig('calificacion_promedio_por_tienda.png')
plt.show()
plt.close()

# Gráfico 3: Costo de Envío Promedio por Tienda
plt.figure(figsize=(10, 6))
sns.barplot(x=average_shipping_cost_per_store.index, y=average_shipping_cost_per_store.values, palette="rocket")
plt.title('Costo de Envío Promedio por Tienda', fontsize=16)
plt.xlabel('Tienda', fontsize=12)
plt.ylabel('Costo de Envío Promedio (COP)', fontsize=12)
plt.ticklabel_format(style='plain', axis='y')
plt.tight_layout()
plt.savefig('costo_envio_promedio_por_tienda.png')
plt.show()
plt.close()

# Gráfico 4: Top 3 Categorías por Tienda
# A diferencia de los otros gráficos, este usa los datos del DataFrame 'top_categories_per_store'
plt.figure(figsize=(12, 7))
sns.barplot(x='Tienda', y='Precio', hue='Categoría del Producto', data=top_categories_per_store, palette="tab10")
plt.title('Ingresos de las Top 3 Categorías por Tienda', fontsize=16)
plt.xlabel('Tienda', fontsize=12)
plt.ylabel('Ingresos (COP)', fontsize=12)
plt.ticklabel_format(style='plain', axis='y')
plt.legend(title='Categoría del Producto', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('top_categorias_por_tienda.png')
plt.show()
plt.close()

print("\nAnálisis completado. Los gráficos se han guardado como archivos PNG.")
