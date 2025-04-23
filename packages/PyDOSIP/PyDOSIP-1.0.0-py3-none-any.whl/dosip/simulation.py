import numpy as np
import matplotlib.pyplot as plt
import csv
import yaml
from typing import Tuple, List
import os
import sys

# Añadir el directorio padre al path para importaciones
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dosip.core import PyDOSIP
from dosip.buffer import Buffer


def load_config(config_path: str) -> dict:
    """
    Carga la configuración desde un archivo YAML.

    Parameters:
    -----------
    config_path : str
        Ruta al archivo de configuración YAML.

    Returns:
    --------
    dict
        Diccionario con la configuración cargada.
    """
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def load_pumping_data_from_csv(file_path: str, flow_column: str, pressure_column: str) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Carga datos de flujo y presión desde un archivo CSV sin usar pandas.

    Parameters:
    -----------
    file_path : str
        Ruta al archivo CSV.
    flow_column : str
        Nombre de la columna de flujo en el archivo CSV.
    pressure_column : str
        Nombre de la columna de presión en el archivo CSV.

    Returns:
    --------
    Tuple[np.ndarray, np.ndarray, np.ndarray]
        Tupla con (tiempo, flujo, presión)
    """
    flow = []
    pressure = []
    
    # Leer el archivo CSV
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            flow.append(float(row[flow_column]))
            pressure.append(float(row[pressure_column]))
    
    # Convertir listas a arrays de numpy
    flow = np.array(flow)
    pressure = np.array(pressure)
    
    # Generar vector de tiempo
    t = np.arange(len(flow))  # Asumimos un intervalo de tiempo constante entre muestras
    
    return t, flow, pressure


def detect_operating_states(
        flow: np.ndarray, 
        pressure: np.ndarray, 
        buffer_size: int = 60,
        threshold: float = 0.5,
        threshold_shutin: float = 10.0,
        times_to_trigger: int = 10
    ) -> List[Tuple[int, str]]:
    """
    Detecta los estados de operación usando PyDOSIP.
    """
    # Inicializar PyDOSIP
    dosip = PyDOSIP(
        window_size=buffer_size, 
        threshold=threshold,
        threshold_shutin=threshold_shutin, 
        times_to_trigger=times_to_trigger
    )
    
    # Inicializar buffers
    fbuffer = Buffer(buffer_size)
    pbuffer = Buffer(buffer_size)
    
    # Lista para almacenar cambios de estado
    state_changes = []
    last_state = None
    
    # Procesar cada punto de datos
    for i in range(len(flow)):
        # Actualizar buffers usando __call__
        fbuffer(flow[i])
        pbuffer(pressure[i])
        
        # Detectar estado (PyDOSIP maneja internamente la verificación del buffer)
        current_state = dosip(flow[i], pressure[i])
        
        # Si el estado cambió, registrar el cambio
        if current_state != last_state:
            state_changes.append((i, current_state))
            last_state = current_state
    
    return state_changes


def plot_pumping_data(t: np.ndarray, flow: np.ndarray, pressure: np.ndarray, state_changes: List[Tuple[int, str]] = None):
    """
    Grafica los datos de flujo y presión con las transiciones de estado.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
    
    # Graficar flujo
    ax1.plot(t, flow, 'b-', label='Flujo')
    ax1.set_ylabel('Flujo (bbl/hr)')
    ax1.set_title('Simulación de Proceso de Bombeo')
    ax1.grid(True)
    ax1.legend()
    
    # Graficar presión
    ax2.plot(t, pressure, 'r-', label='Presión')
    ax2.set_xlabel('Tiempo (s)')
    ax2.set_ylabel('Presión (psi)')
    ax2.grid(True)
    ax2.legend()
    
    # Agregar líneas verticales para marcar las fases simuladas
    for ax in [ax1, ax2]:
        # Líneas de estado detectado (rojo)
        if state_changes:
            for idx, state in state_changes:
                ax.axvline(x=t[idx], color='r', linestyle=':', alpha=0.5, label='Estado Detectado')
                # Agregar texto del estado
                ax.text(t[idx], ax.get_ylim()[1], state, 
                       rotation=90, va='top', ha='right', 
                       color='r', alpha=0.7)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import sys
    
    # Verificar que se haya pasado un archivo de configuración
    if len(sys.argv) != 2:
        sys.exit(1)
    
    # Cargar configuración
    config_path = sys.argv[1]
    config = load_config(config_path)
    
    # Ruta al archivo CSV
    csv_file_path = config['csv_file_path']
    
    # Parametros de PyDOSIP
    buffer_size = config['pydosip']['buffer_size']
    times_to_trigger = config['pydosip']['times_to_trigger']
    threshold = config['pydosip']['threshold']
    threshold_shutin = config['pydosip']['threshold_shutin']
    
    # Cargar datos desde el archivo CSV
    t, flow, pressure = load_pumping_data_from_csv(
        csv_file_path,
        config['csv_columns']['flow'],
        config['csv_columns']['pressure']
    )
    
    # Detectar estados de operación
    state_changes = detect_operating_states(
        flow, 
        pressure, 
        buffer_size=buffer_size,
        threshold=threshold, 
        threshold_shutin=threshold_shutin, 
        times_to_trigger=times_to_trigger
    )
    
    # Graficar datos con estados detectados
    plot_pumping_data(t, flow, pressure, state_changes) 