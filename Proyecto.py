# -*- coding: utf-8 -*-
"""
Created on Sun May 12 16:51:53 2024

@author: danie
"""

#---------------------------------------PROYECTO INTEGRADOR---------------------------------------
#Zuly Gonzalez
#Daniel Marquez
import matplotlib.pyplot as plt
import pandas as pd
# Se carga el archivo principal del cual se obtendrán los datos a analizar.
# Los datos de interés filtrados para obtener el archivo son los siguientes:
# Dataset original: EOD – eBird Observation Dataset
# Coordenasas limitantes: POLYGON((-73.9053 5.17865,-72.14778 5.17865,-72.14778 5.95608,-73.9053 5.95608,-73.9053 5.17865))
# País: Colombia
# Años: Entre inicio 2023 y fin de 2024
# Nombre cientifico: Aves
# Link consulta descargada: https://www.gbif.org/occurrence/download/0001046-240506114902167
# La base de datos se seleccionó ya que da un panorama claro y completo de las frecuencias en las que se observan las diferentes especies
# de aves en el departamento de Boyacá y con dicha información se puede realizar un análisis estadistico que permita inferir sobre la biodiversidad
# de especies de aves presente en este departamento.


file = "Dataset EOD – eBird.xlsx"
selectedRows=['gbifID','kingdom','phylum','class','order','family','genus','species','locality','stateProvince','individualCount','eventDate']
df = pd.read_excel(file,usecols=selectedRows)
# Definimos la primera columna (gbifID) como llave principal ya que es el ID unico del avistamiento
df.set_index('gbifID', inplace=True)

# Traemos registros de avistamientos de fauna en Boyacá con datos de altitud en la que se observó
# Dataset original: Caracterización de fauna en diferentes gradientes altitudinales del departamento de Boyacá, Colombia
altitud = "Altitud.xlsx"
altitudRows = ['species','elevation']
df_altitud= pd.read_excel(altitud,usecols=altitudRows)
# Agrupamos sus registros unicamente por la especie y traemos un promedio de los datos de altitud y redondeamos dicho promedio
df_resaltitud=df_altitud.groupby('species')['elevation'].mean().reset_index()
df_resaltitud['elevation']=df_resaltitud['elevation'].round()

# Realizamos una unión de los dos dataframes utilizando como campo de coincidencia 'species' y traemos los datos de elevación promedio en la que se observó
df= pd.merge(df,df_resaltitud,on='species',how='left')

# Obtenemos la cantidad de filas y columnas del dataframe resultante
num_filas, num_columnas = df.shape
print("Número de filas: "+str(num_filas))
print("Número de columnas: "+str(num_columnas))


#Definimos los tipos de datos que contiene cada columna para estandarizar la información de entrada.
column_types = {
    'gbifID': int,
    'kingdom': str,
    'phylum': str,
    'class': str,
    'order': str,
    'family': str,
    'genus': str,
    'species': str,
    'locality': str,
    'stateProvince': str,
    'individualCount': int,
    'eventDate': str
}


#Encontramos el porcentaje de valores faltantes en cada columna

porc_faltantes= df.isna().mean()*100
print("Porcentaje de faltantes en cada columna:\n"+str(porc_faltantes))
# Se evidencia que hay datos faltantes en las columnas genus, species, individual count y elevation
# Limpiamos los datos de la siguiente manera:
# 1. Cambiando los registros no encontrados por un valor igual al promedio de las demás elevaciones en la columna 'elevation'
df['elevation'] = df['elevation'].fillna(df['elevation'].mean())
# 2. Asumiendo que en los faltantes en la columna individualCount el valor es 1 ya que se observa por lo menos un especimen.
df['individualCount'] = df['individualCount'].fillna(1)
# 3. Genus y Species no poseen datos ya que estas son generos o especies unicas, por lo tanto se replican los valores de family y genus, respectivamente
df['genus'] = df['genus'].fillna(df['family'])
df['species'] = df['species'].fillna(df['genus'])


# Contamos valores unicos en las distintas clasificaciones de las especies de aves para determinar cual genera una agrupación adecuada para el análisis de los datos.
unicos_categ = df[['order', 'family', 'genus']].nunique()
print("Valores unicos en cada categoría:\n"+ str(unicos_categ))

#Se selecciona el campo order para poder representar la distribución de las especies ya que parece ser el mas adecuado para un histograma, sin embargo generamos diferentes histogramas para para corrobar esta decisión
# Agrupar por 'order' y calcular la suma de 'individualCount'
order_counts = df.groupby('order')['individualCount'].sum()

# Crear el histograma para 'order'
plt.figure(figsize=(8, 6))
plt.bar(order_counts.index, order_counts.values)
plt.xlabel('Order')
plt.ylabel('Individual Count')
plt.title('Histograma por Order')
plt.xticks(rotation=45)
plt.show()

# Agrupar por 'family' y calcular la suma de 'individualCount'
family_counts = df.groupby('family')['individualCount'].sum()

# Crear el histograma para 'family'
plt.figure(figsize=(8, 6))
plt.bar(family_counts.index, family_counts.values)
plt.xlabel('Family')
plt.ylabel('Individual Count')
plt.title('Histograma por Family')
plt.xticks(rotation=45)
plt.show()

# Agrupar por 'genus' y calcular la suma de 'individualCount'
genus_counts = df.groupby('genus')['individualCount'].sum()

# Crear el histograma para 'genus'
plt.figure(figsize=(8, 6))
plt.bar(genus_counts.index, genus_counts.values)
plt.xlabel('Genus')
plt.ylabel('Individual Count')
plt.title('Histograma por Genus')
plt.xticks(rotation=45)
plt.show()

# Se observa que 'order' es el campo adecuado, sin enmbargo, hace falta depurar los datos considerando solo las 10 categorías con mayor avistamientos
top_10_order = order_counts.nlargest(10)
plt.figure(figsize=(8, 6))
plt.bar(top_10_order.index, top_10_order.values)
plt.xlabel('Order')
plt.ylabel('Individual Count')
plt.title('Histograma por Order (sum > 5000)')
plt.xticks(rotation=45)
plt.show()


# Adicional podemos realizar un diagrama que represente las frecuencias por meses
df['eventDate'] = pd.to_datetime(df['eventDate'])
df['month'] = df['eventDate'].dt.month
monthly_counts = df.groupby('month')['individualCount'].sum()
plt.figure(figsize=(8, 6))
plt.bar(monthly_counts.index, monthly_counts.values)
plt.xlabel('Mes')
plt.ylabel('Cantidad de registros')
plt.title('Histograma de registros por meses')
plt.xticks(range(1, 13))
plt.show()
