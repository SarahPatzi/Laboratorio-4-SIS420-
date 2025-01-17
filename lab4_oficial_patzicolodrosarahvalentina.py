# -*- coding: utf-8 -*-
"""Lab4_Oficial-PatziColodroSarahValentina.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wyCfJ9uFQYUrqxZjCF9rtkB7Z3GZ_J7Q

### **LABORATORIO 04 - GRUPO 1**
Para este laboratorio usaremos un dataset que contenga al menos 11 propiedades (n>10) y por lo menos 20000 ejemplos (m>=20000), para entrenar el modelo de regresión logística (clasificación multiclase).  

* **Universitario:** Patzi Colodro Sarah Valentina
* **Nombre del Dataset:** Sloan Digital Sky Survey - DR18
* **URL del Dataset:** https://www.kaggle.com/datasets/diraf0/sloan-digital-sky-survey-dr18
* **Temática del Dataset:** clasificacion de objetos astronómicos
* **Variables de Entrada:** objid,specobjid,ra,dec,u,g,r,i,z,run,rerun,camcol,field,plate,mjd,fiberid,petroRad_u,petroRad_g,petroRad_i,petroRad_r,petroRad_z,petroFlux_u,petroFlux_g,petroFlux_i,petroFlux_r,petroFlux_z,petroR50_u,petroR50_g,petroR50_i,petroR50_r,petroR50_z,psfMag_u,psfMag_r,psfMag_g,psfMag_i,psfMag_z,expAB_u,expAB_g,expAB_r,expAB_i,expAB_z,redshift

* **Variables de Salida:** class

* **Formato:** 100000 filas × 43 columnas

### **Importar carpetas de drive**
"""

from google.colab import drive
drive.mount('/content/drive')

"""### **Importar Librerias**"""

# Commented out IPython magic to ensure Python compatibility.
# utilizado para la manipulación de directorios y rutas
import os
# Biblioteca para la manipulación y el análisis de datos
import pandas as pd
#importa una clase que permite usar las Máquinas de Vectores de Soporte para clasificar datos
from sklearn.svm import SVC
# Cálculo científico y vectorial para python
import numpy as np
# Libreria para graficos
from matplotlib import pyplot
# Modulo de optimizacion en scipy
from scipy import optimize
# modulo para cargar archivos en formato MATLAB
from scipy.io import loadmat
# le dice a matplotlib que incruste gráficos en el cuaderno
from sklearn.model_selection import train_test_split

#para graficar el costo
import matplotlib.pyplot as plt

# le dice a matplotlib que incruste gráficos en el cuaderno
# %matplotlib inline

"""### **Carga y Verificación de Datos del Dataset**
El código carga un conjunto de datos desde el archivo CSV **SDSS_DR18.csv** utilizando la función **read_csv de pandas** y lo almacena en un DataFrame. Luego, muestra el DataFrame para verificar que los datos se hayan cargado correctamente.
Se utiliza **data.isnull().sum()** para contar los valores nulos en cada columna.
"""

# Cargamos el dataset
data = pd.read_csv('/content/drive/MyDrive/IA/LaboratoriosOficiales/Lab4-PatziColodroSarahValentina/SDSS_DR18.csv', delimiter=',')
display(data)

# Verificamos valores nulos
data.isnull().sum()

#imprimir el data
display(data)

"""### **Reemplazo de valores categóricos en un DataFrame**


Este código convierte valores categóricos de la columna '**class**' en el DataFrame **data** a valores numéricos mediante un **diccionario (cambio_letras)** que asigna 1 a 'GALAXY', 2 a 'STAR', y 3 a 'QSO'. Luego, utiliza map() para reemplazar cada valor de texto con su número correspondiente y finalmente imprime el DataFrame modificado para verificar los cambios.
"""

cambio_letras = {'GALAXY': 1, 'STAR': 2, 'QSO': 3}
data['class'] = data['class'].map(cambio_letras)

# Imprimo el DataFrame para verificar la columna 'class' modificada
print(data)

"""### **Selección de características y variable de salida en el DataFrame**

El código extrae las primeras 42 columnas como características (X) y la última columna como la variable de salida (y), imprime sus tamaños para ver cuántas filas y columnas tiene cada uno, y verifica las primeras filas de los datos para asegurarse de que la selección es correcta.
"""

X = data.iloc[:, :42].values  # Las primeras 42 columnas
y = data.iloc[:, -1].values   # Solo la última columna (si esta sigue siendo la variable de salida)
# Imprimo el tamaño de las características y del label que usaré
print(X.shape)
print(y.shape)

# Verificar las primeras 100 filas
print(X[:100])
print(y[:1])

"""### **Definición de parámetros del modelo y verificación de etiquetas únicas**

 Definimos la cantidad de características de entrada, las etiquetas únicas y el número de ejemplos del modelo, luego imprimimos estos valores para asegurar que la configuración del modelo sea correcta y que todas las etiquetas en "y" estén bien identificadas.

 * **X.shape[1]:** Devuelve el número de columnas que tiene X.
 * **len(np.unique(y))**: Cuenta cuántos valores únicos o diferentes hay en y. Si y es una lista de etiquetas o categorías (como tipos de objetos), esta función te dice cuántos tipos diferentes existen.
"""

# Defino variables
input_layer_size = X.shape[1]  # Número de columnas en X
num_labels = len(np.unique(y))  # Número de clases únicas en y, Muestra todas las etiquetas únicas presentes en y
m = y.size
#imprimir input_layer size
print(input_layer_size)
#imprimir num_labels
print(num_labels)
#imprimir m
print(m)

# Muestra todas las etiquetas únicas presentes en y
etiquetas_unicas = np.unique(y)
print('Etiquetas: ', etiquetas_unicas)

"""### **Función para Normalizar Características de Datos**

La función featureNormalize ajusta los valores de X para que tengan una media de 0 y una desviación estándar de 1
"""

def featureNormalize(X):
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    epsilon = 1e-8
    sigma += epsilon
    X_norm = (X - mu) / sigma
    return X_norm, mu, sigma

X_norm, mu, sigma = featureNormalize(X)

print(X)
print('Media calculada:', mu)
print('Desviación estandar calculada:', sigma)
print(X_norm)

"""### **División de datos en conjuntos de entrenamiento y prueba**

El código divide los datos normalizados en conjuntos de entrenamiento y prueba, usando un 80% de datos para entrenar y un 20% para probar el modelo, e imprime los tamaños de ambos conjuntos para confirmar la correcta separación de los datos.

* **X_norm** y **y** son los datos normalizados y las etiquetas.
* **test_size=0.2** significa que el 20% de los datos se asigna al conjunto de prueba y el 80% al conjunto de entrenamiento.
* **random_state=50** establece una semilla para que la división sea reproducible, es decir, siempre se obtenga la misma separación al ejecutar el código.
"""

X_train, X_test, y_train, y_test = train_test_split(X_norm, y, test_size=0.2, random_state=50)
#Imprimo el tamaño de los datos de entrenamiento y test
print(X_train.shape)
print(X_test.shape)

"""### **Cálculo de la función sigmoide para regresión logística**

La función calcularSigmoide calcula la probabilidad usando la función sigmoide, limitando primero el valor de z para evitar errores de cálculo con números demasiado grandes o pequeños
"""

def calcularSigmoide(z):
    # Limitar los valores de z para evitar overflow
    z = np.clip(z, -500, 500) #limita el valor de z para evitar errores de cálculo cuando hay datos muy grandes o pequeños
    return 1.0 / (1.0 + np.exp(-z))

"""### **Cálculo del costo y gradiente con regularización en regresión logística**

Calcula el error del modelo y cómo deben ajustarse los parámetros para minimizar este error, utilizando la regularización para prevenir sobreajuste

* h = np.clip(h, epsilon, 1 - epsilon): Ajusta los valores de h para que nunca sean exactamente 0 o 1, evitando problemas al calcular el logaritmo.
"""

def calcularCosto(theta, X_norm, y, lambda_):
    # Inicializa algunos valores utiles
    m = y.size

    # Convierte las etiquetas a valores enteros si son booleanos
    if y.dtype == bool:
        y = y.astype(int)

    J = 0
    grad = np.zeros(theta.shape)

    # Calcula la hipótesis usando la función sigmoide
    h = calcularSigmoide(X_norm.dot(theta.T))

    # Evita valores de h que sean exactamente 0 o 1
    epsilon = 1e-10
    h = np.clip(h, epsilon, 1 - epsilon)

    # Crea una copia de theta y asegura que el primer elemento no esté regularizado
    temp = np.copy(theta)
    temp[0] = 0

    # Calcula el costo con regularización
    J = (1 / m) * np.sum(-y.dot(np.log(h)) - (1 - y).dot(np.log(1 - h))) + (lambda_ / (2 * m)) * np.sum(np.square(temp))

    # Calcula el gradiente con regularización
    grad = (1 / m) * (h - y).dot(X_norm)
    grad = grad + (lambda_ / m) * temp

    return J, grad

"""### **Generación de valores de prueba para la validación del modelo de regresión logística**

Genera valores aleatorios para las características de los datos (X_t) y las etiquetas de clase (y_t) que se utilizarán para probar el modelo de regresión logística. Los valores de los parámetros (theta_t) se establecen manualmente y representan los pesos iniciales del modelo que deseas probar.

* **theta_t:** Se define un array de valores (theta_t) que representa los parámetros iniciales del modelo de regresión logística. Estos valores se usarán para calcular la hipótesis y el costo.

* **X_t:** Genera un conjunto de datos de prueba X_t: np.concatenate((np.ones((100000, 1)), np.random.rand(100000, 41)), axis=1): Crea un array X_t con 100,000 ejemplos y 42 características.
Añade una columna de unos (de tamaño 100000 x 1) para incluir el término de sesgo (intercepto).
Las otras 41 columnas son valores aleatorios generados con np.random.rand, lo que simula características diversas.
* **y_t:** Crea un array de etiquetas de clase y_t con 100,000 valores aleatorios entre 0 y 2 (tres posibles clases). Esto sirve para probar el modelo con múltiples clases.

* **lambda_t:** Define el valor de regularización (lambda_t = 0.2), que controla cuánto penalizamos los valores grandes de los parámetros theta para evitar el sobreajuste.

"""

#Valor de prueba para theta
theta_t = np.array([0.5, 0.2, 0.8, 0.3, 0.1, 0.4, 0.7, 0.1, 0.2, 0.5, 0.6, 0.6, 0.3, 0.7, 0.4, 0.8, 0.942, 0.8, 0.4,
                    0.3996321, 0.86057145, 0.68559515, 0.57892679, 0.22481491, 0.22479562, 0.14646689, 0.79294092,
                    0.58089201, 0.66645806, 0.1164676, 0.87592788, 0.76595411, 0.26987129, 0.24545997, 0.24672361,
                    0.34339379, 0.51980515, 0.44555601, 0.33298331, 0.58948232, 0.21159509, 0.33371572], dtype=float)

# Valores de prueba para las entradas X
X_t = np.concatenate((np.ones((100000, 1)), np.random.rand(100000, 41)), axis=1)
print(X_t)

# Valores de prueba para las clases
y_t = np.random.randint(0, 3, 100000)

# Valor de prueba para la regularización
lambda_t = 0.2

"""Calculo y muestro el costo y los gradientes del modelo usando los datos generados aleatoriamente. El costo indica qué tan bien el modelo se ajusta a los datos, mientras que los gradientes muestran cómo deben ajustarse los parámetros para mejorar ese ajuste.

* Un costo cercano a cero significa que la diferencia entre las predicciones del modelo y los valores reales es muy pequeña.
En este caso tenemos un costo cercano a cero por lo cual indica que el modelo está haciendo un buen trabajo al ajustar los datos.

* Y los gradientes son valores pequeños, lo cual indica que el modelo ya está bastante cerca de un punto óptimo
"""

J, grad = calcularCosto(theta_t, X_t, y_t, lambda_t)

print('Costo         : {:.6f}'.format(J))
#print('Costo esperado: ')
print('-----------------------')
print('Gradientes:')
print(' [{:.6f}, {:.6f}, {:.6f}, {:.6f}]'.format(*grad))
#print('Gradientes esperados:')
#print(' [0.146561, -0.548558, 0.724722, 1.398003]');

"""### **Entrenamiento de un clasificador One-vs-All**

Le paso todas las X agregando lo del sesgo, luego las Y, las etiquetas, le paso lambda que es para la regularizacion

ya que es una multiclase se debe tener todos los tethas para todas las etiquetas

* **options = {'maxiter': 5000}:** Establece el número máximo de iteraciones para el algoritmo de optimización.
"""

def oneVsAll(X, y, num_labels, lambda_):

    m, n = X.shape
    all_theta = np.zeros((num_labels, n + 1)) #crea un array del numero de etiquetas para las filas, y le pasa las columnas sin el sesgo el +1 es para el sesgo
    #imprimir all_theta size
    print(all_theta.shape)
    X = np.concatenate([np.ones((m, 1)), X], axis=1)

    for c in np.arange(num_labels):
        initial_theta = np.zeros(n + 1)
        options = {'maxiter': 5000}
        res = optimize.minimize(calcularCosto,
                                initial_theta,
                                (X, (y == (c + 1)), lambda_),
                                jac=True,
                                method='BFGS',
                                options=options)
        all_theta[c] = res.x
    return all_theta

lambda_ = 0.2
all_theta = oneVsAll(X_train, y_train, num_labels, lambda_)
#Imprimo las thetas
print(all_theta)
#imprimir tamaño de all_theta
print(all_theta.shape)

"""Esta función utiliza el modelo entrenado para predecir la clase más probable de cada ejemplo en X.
* **return p + 1:** Retorna las predicciones ajustando el índice para que coincida con las etiquetas originales (asumiendo que las etiquetas empiezan en 1)

Usamos return p + 1 porque las etiquetas  se han mapeado a los números 1, 2, 3 en lugar de los índices típicos de Python que comienzan en 0, sumamos 1 para que las predicciones coincidan correctamente con estos valores de etiqueta originales.
"""

def predictOneVsAll(all_theta, X):
    m = X.shape[0];
    num_labels = all_theta.shape[0]

    p = np.zeros(m)

    # Add ones to the X data matrix
    X = np.concatenate([np.ones((m, 1)), X], axis=1)
    p = np.argmax(calcularSigmoide(X.dot(all_theta.T)), axis = 1) #todos los tethas (en este caso son 3 filas por 42 columnas de X) se multiplican por todas las X, luego salen varios resultados y el argmax regresa el indice del que tiene mayor probabilidad

    return p + 1

"""### Hacemos las pruebas de precisión y predicciones

Como las etiquetas en el conjunto de datos están mapeadas a 1 (para "GALAXY"), 2 (para "STAR"), y 3 (para "QSO"), se añade 1 al resultado de argmax para que las predicciones se alineen correctamente con estas etiquetas.
"""

pred_train = predictOneVsAll(all_theta, X_train)
#calculamos la precisión del entrenamiento (80%)
precision_entrenamiento = np.mean(pred_train == y_train) * 100
print('Precisión del conjunto de entrenamiento: {:.2f}%'.format(precision_entrenamiento))

XPrueba = X_test[:100].copy()
yPrueba = y_test.copy()
#concatenamos la columna de unos a XPrueba
XPrueba = np.concatenate((np.ones((100, 1)), XPrueba), axis=1)
print(XPrueba)
#Hacemos las predicciones del test (20%)
pred_prueba = np.argmax(calcularSigmoide(XPrueba.dot(all_theta.T)), axis=1)

print('Predicciones en el conjunto de prueba:')
print(pred_prueba + 1)

# Datos para prueba (fila 1)
datos = [ [1.240000e+18, 3.250000e+17, 184.95, 0.73, 18.87, 17.6, 17.11, 16.84, 16.71, 756, 301, 5, 462, 288, 52000, 456, 7.28, 7, 6.86, 7.11, 6.93, 30.66, 95.12, 181.72, 146.99, 207.03, 3.83, 3.66, 3.49, 3.62, 3.61, 21.12, 19.5, 19.96, 19.25, 19.05, 0.48, 0.52, 0.52, 0.51, 0.49, 0.04]]
XX = np.array(datos)

# IMPORTANTE NORMALIZAR !!
# Normalizar XX utilizando mu y sigma del conjunto de entrenamiento
XX_norm = (XX - mu) / sigma  # Normaliza usando los mismos parámetros

# Copia los datos normalizados para la prueba
XPrueba = XX_norm.copy()
yPrueba = y_test.copy()

# Concatenamos la columna de unos a XPrueba
XPrueba = np.concatenate((np.ones((XX_norm.shape[0], 1)), XPrueba), axis=1)
print(XPrueba)

# Hacemos las predicciones del test (20%)
pred_prueba = np.argmax(calcularSigmoide(XPrueba.dot(all_theta.T)), axis=1)

print('Prediccion en la prueba:', pred_prueba+1)
print('Prediccion esperada: 1 (GALAXY)')

# Datos para prueba (fila 17)
datos = [ [1.24E+18,2.88E+18,186.1506447,0.684432945,18.3146,16.79596,16.25018,16.03951,15.94311,756,301,5,470,2558,54140,538,1.404998,1.301747,1.153099,1.139226,1.144206,45.24086,181.9437,360.9119,302.9594,397.5954,0.7034816,0.6556676,0.5964427,0.5918828,0.6007596,18.33955,16.24669,16.80719,16.04553,15.941,0.8582829,0.9774393,0.9999605,0.8446276,0.3467041,0.000102763]]
XX = np.array(datos)

# IMPORTANTE NORMALIZAR !!
# Normalizar XX utilizando mu y sigma del conjunto de entrenamiento
XX_norm = (XX - mu) / sigma  # Normaliza usando los mismos parámetros

# Copia los datos normalizados para la prueba
XPrueba = XX_norm.copy()
yPrueba = y_test.copy()

# Concatenamos la columna de unos a XPrueba
XPrueba = np.concatenate((np.ones((XX_norm.shape[0], 1)), XPrueba), axis=1)
print(XPrueba)

# Hacemos las predicciones del test (20%)
pred_prueba = np.argmax(calcularSigmoide(XPrueba.dot(all_theta.T)), axis=1)

print('Prediccion en la prueba:', pred_prueba+1)
print('Prediccion esperada: 2 (STAR)')

# Datos para prueba (fila 22)
datos = [ [1.24E+18,3.24E+17,185.0711481,0.718114239,19.46431,19.33361,19.14591,19.0513,19.03554,756,301,5,463,288,52000,447,1.402337,1.214442,1.199927,1.241184,1.191545,15.95607,17.43523,22.49177,21.19154,24.38496,0.7076668,0.6191955,0.5979597,0.6310332,0.643189,19.46762,19.16031,19.33522,19.05376,19.05335,0.9998865,0.1421806,0.6105502,0.9996712,0.3386156,1.275072]]
XX = np.array(datos)

# IMPORTANTE NORMALIZAR !!
# Normalizar XX utilizando mu y sigma del conjunto de entrenamiento
XX_norm = (XX - mu) / sigma  # Normaliza usando los mismos parámetros

# Copia los datos normalizados para la prueba
XPrueba = XX_norm.copy()
yPrueba = y_test.copy()

# Concatenamos la columna de unos a XPrueba
XPrueba = np.concatenate((np.ones((XX_norm.shape[0], 1)), XPrueba), axis=1)
print(XPrueba)

# Hacemos las predicciones del test (20%)
pred_prueba = np.argmax(calcularSigmoide(XPrueba.dot(all_theta.T)), axis=1)

print('Prediccion en la prueba:', pred_prueba+1)
print('Prediccion esperada: 3 (QSO)')

"""### **Entrenamiento y Evaluación de un Modelo SVM**

Se crea un modelo de clasificación usando una Máquina de Soporte Vectorial (SVM) con SVC() de scikit-learn.
 * Primero, el modelo se entrena con los datos de entrenamiento (X_train y y_train).
 * Luego, se evalúa el modelo calculando su precisión con el conjunto de prueba (X_test y y_test).
 * La precisión del modelo se muestra como un porcentaje, indicando qué tan bien el modelo predice las etiquetas del conjunto de prueba.
"""

classifier =  SVC()

classifier.fit(X_train, y_train)

score = classifier.score(X_test, y_test)*100
print('Precisión del conjunto: {:.2f}%'.format(score))