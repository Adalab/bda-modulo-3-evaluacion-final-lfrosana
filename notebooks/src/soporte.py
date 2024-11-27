# Tratamiento de datos
# -----------------------------------------------------------------------
import pandas as pd
import numpy as np

# Imputación de nulos usando métodos avanzados estadísticos
# -----------------------------------------------------------------------
from sklearn.impute import SimpleImputer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.impute import KNNImputer

# Visualización
# ------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import seaborn as sns

# Evaluar linealidad de las relaciones entre las variables
# y la distribución de las variables
# -------------------------------------------------------------------------------

import scipy.stats as stats
from scipy.stats import shapiro, levene
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
from scipy.stats import chi2_contingency
from sklearn.linear_model import LinearRegression

# Configuración
# -----------------------------------------------------------------------
pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames

# Gestión de los warnings
# -----------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore")

pd.set_option('display.max_columns', None) # para poder visualizar todas las columnas de los DataFrames
# Para explorar los DFs





def exploracion(df):
    
    """ 
    Realiza una exploración inicial y descriptiva de un DataFrame para identificar información relevante 
    sobre los datos, como valores nulos, duplicados, tipos de datos, y estadísticas generales. 
    La función también imprime un resumen de las columnas categóricas y numéricas del DataFrame.
    
    Parámetros:
    -----------
    dataframe (DataFrame): El DataFrame que contiene los datos.
    
    Descripción:
    ------------
    La función realiza los siguientes análisis y genera la siguiente información:
    
    - El número de filas y columnas del DataFrame.
    - La cantidad de datos duplicados y su porcentaje en relación al total.
    - La cantidad de columnas con valores nulos y las columnas sin valores nulos.
    - El tipo de dato de cada columna.
    - El número de valores únicos por columna.
    
    Además, la función imprime estadísticas descriptivas de las columnas categóricas (si las hay) y 
    numéricas (si las hay) del DataFrame."""
    
    df_info = pd.DataFrame()

    df_info["% nulos"] = round(df.isna().sum() / df.shape[0] * 100, 2).astype(str) + "%"
    df_info["% no_nulos"] = (
        round(df.notna().sum() / df.shape[0] * 100, 2).astype(str) + "%"
    )
    df_info["tipo_dato"] = df.dtypes
    df_info["num_valores_unicos"] = (
        df.nunique()
    )  # devuelve el número de valores únicos en la columna.

    print(f"""El DataFrame tiene {df.shape[0]} filas y {df.shape[1]} columnas.
Tiene {df.duplicated().sum()} datos duplicados, lo que supone un porcentaje de {round(df.duplicated().sum()/df.shape[0]*100, 2)}% de los datos.

Hay {len(list(df_info[(df_info["% nulos"] != "0.0%")].index))} columnas con datos nulos, y son: 
{list(df_info[(df_info["% nulos"] != "0.0%")].index)}

y sin nulos hay {len(list(df_info[(df_info["% nulos"] == "0.0%")].index))} columnas y son: 
{list(df_info[(df_info["% nulos"] == "0.0%")].index)}


A continuación tienes un detalle sobre los datos nulos y los tipos y número de datos:""")

    print("Principales estadísticos de las columnas categóricas:")

    if (
        df.select_dtypes(include="object").shape[1] > 0
    ):  # Verificar si hay columnas categóricas
        display(df.describe(include="O").T)
    else:
        print("No hay columnas categóricas en el DataFrame.")

    print("Principales estadísticos de las columnas numéricas:")

    if (
        df.select_dtypes(exclude="object").shape[1] > 0
    ):  # Verificar si hay columnas numéricas
        display(df.describe(exclude="O").T)
    else:
        print("No hay columnas numéricas en el DataFrame.")

    return df_info



# lo primero que hacemos es comprobar la normalidad de los datos usando esta función:

def normalidad(dataframe, columna):
    """
    Evalúa la normalidad de una columna de datos de un DataFrame utilizando la prueba de Shapiro-Wilk.

    Parámetros:
        dataframe (DataFrame): El DataFrame que contiene los datos.
        columna (str): El nombre de la columna en el DataFrame que se va a evaluar para la normalidad.

    Returns:
        None: Imprime un mensaje indicando si los datos siguen o no una distribución normal.
    """

    statistic, p_value = stats.shapiro(dataframe[columna])
    if p_value > 0.05:
        print(f"Para la columna {columna} los datos siguen una distribución normal.")
    else:
        print(f"Para la columna {columna} los datos no siguen una distribución normal.")