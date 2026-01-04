import pandas as pd
import scipy.stats
import streamlit as st
import time

#Variables de estado que se conservan cuando Streamlit vuelve a ejecutar el script
if 'experiment_no' not in st.session_state:#Si 'experiment_no' no está en el estado de la sesión
    st.session_state['experiment_no'] = 0 #Inicializa 'experiment_no' en 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iteraciones', 'media']) #Inicializa un DataFrame vacío con columnas específicas


st.header('Lanzar una moneda')

chart = st.line_chart([0.5]) #Crea un gráfico de líneas con un valor inicial de 0.5

def toss_coin(n): #Define una función para lanzar una moneda n veces
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n) #Genera resultados de lanzamientos de moneda (0 o 1) usando una distribución Bernoulli n veces

    mean = None #Inicializa la variable mean
    outcome_no = 0 #Inicializa el contador de resultados
    outcome_1_count = 0 #Inicializa el contador de caras (1s)

    for r in trial_outcomes: #Itera a través de los resultados de los lanzamientos
        outcome_no += 1
        if r == 1:#Si el resultado es 1 (cara)
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no #Calcula la media de caras obtenidas hasta ahora
        chart.add_rows([mean]) #Agrega la media actual al gráfico de líneas
        time.sleep(0.05)#Pausa de 0.05 segundos para simular el tiempo entre lanzamientos
    return mean #Devuelve la media final de caras obtenidas



number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10) #pide a los usuarios que seleccionen un número entre 1 y 1000, con un valor predeterminado de 10
start_button = st.button('Ejecutar')#Crea un botón etiquetado como "Ejecutar"

if start_button:#Si el botón "Ejecutar" es presionado
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    st.session_state['experiment_no'] += 1 #Incrementa el número de experimento en el estado de la sesión
    mean = toss_coin(number_of_trials) #Llama a la función toss_coin con el número seleccionado de intentos
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        pd.DataFrame(data=[[st.session_state['experiment_no'],
                             number_of_trials,
                             mean]],
                             columns=['no', 'iteraciones', 'media'])
    ],
    axis=0)
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])#Muestra el DataFrame de resultados de experimentos en la aplicación

