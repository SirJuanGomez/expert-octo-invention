import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
from collections import deque
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Importación necesaria

# Nombre del archivo JSON
json_filename = 'sensor_data.json'

# Configuración de la ventana principal de Tkinter
root = Tk()
root.title("Gráficas de Sensores")
root.state('zoomed')  # Abrir en pantalla completa

# Crear los frames para las gráficas y los datos del giroscopio/UV
main_frame = ttk.Frame(root)
main_frame.pack(fill=BOTH, expand=1)

graph_frame = ttk.Frame(main_frame)
graph_frame.pack(side=LEFT, fill=BOTH, expand=1)

data_frame = ttk.Frame(main_frame)
data_frame.pack(side=RIGHT, fill=BOTH, padx=10, pady=10)

# Configuración de la gráfica
fig, axs = plt.subplots(3, 1, figsize=(8, 8))
ax1, ax2, ax3 = axs

# Configuración de las listas de datos
max_len = 100  # Número máximo de puntos en la gráfica
temperature_data = deque(maxlen=max_len)
pressure_data = deque(maxlen=max_len)
altitude_data = deque(maxlen=max_len)
timestamps = deque(maxlen=max_len)

# Configuración de la gráfica de temperatura
line_temp, = ax1.plot([], [], marker='o', linestyle='-', color='b', label='Temperatura (°C)')
ax1.set_xlabel('Tiempo (s)')
ax1.set_ylabel('Temperatura (°C)')
ax1.set_title('Temperatura en Tiempo Real')
ax1.grid(True)
ax1.legend()

# Configuración de la gráfica de presión
line_pres, = ax2.plot([], [], marker='o', linestyle='-', color='r', label='Presión (hPa)')
ax2.set_xlabel('Tiempo (s)')
ax2.set_ylabel('Presión (hPa)')
ax2.set_title('Presión en Tiempo Real')
ax2.grid(True)
ax2.legend()

# Configuración de la gráfica de altitud
line_alt, = ax3.plot([], [], marker='o', linestyle='-', color='g', label='Altitud (m)')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Altitud (m)')
ax3.set_title('Altitud en Tiempo Real')
ax3.grid(True)
ax3.legend()

# Configuración de los datos del giroscopio y UV y Grados
gx_label = Label(data_frame, text="Giroscopio X:", font=('Arial', 12))
gx_label.pack(anchor='w')
gx_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
gx_value.pack(anchor='w', fill=X)

gy_label = Label(data_frame, text="Giroscopio Y:", font=('Arial', 12))
gy_label.pack(anchor='w')
gy_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
gy_value.pack(anchor='w', fill=X)

gz_label = Label(data_frame, text="Giroscopio Z:", font=('Arial', 12))
gz_label.pack(anchor='w')
gz_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
gz_value.pack(anchor='w', fill=X)

bx_label = Label(data_frame, text="Grados en  X:", font=('Arial', 12))
bx_label.pack(anchor='w')
bx_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
bx_value.pack(anchor='w', fill=X)

by_label = Label(data_frame, text="Grados en Y:", font=('Arial', 12))
by_label.pack(anchor='w')
by_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
by_value.pack(anchor='w', fill=X)

bz_label = Label(data_frame, text="Grados en Z:", font=('Arial', 12))
bz_label.pack(anchor='w')
bz_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
bz_value.pack(anchor='w', fill=X)

uv_label = Label(data_frame, text="Voltaje UV:", font=('Arial', 12))
uv_label.pack(anchor='w')
uv_value = Label(data_frame, text="", font=('Arial', 12), relief=SUNKEN)
uv_value.pack(anchor='w', fill=X)

# Función para leer los datos del archivo JSON
def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            try:
                data = json.load(file)
                # Si los datos no están en una lista, los convertimos en una lista
                if isinstance(data, dict):
                    return [data]
                return data
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error al leer el archivo JSON: {e}")
                return []
    return []

# Función de inicialización para el gráfico
def init():
    line_temp.set_data([], [])
    line_pres.set_data([], [])
    line_alt.set_data([], [])
    gx_value.config(text="")
    gy_value.config(text="")
    gz_value.config(text="")
    bx_value.config(text="")
    by_value.config(text="")
    bz_value.config(text="")
    uv_value.config(text="")
    return line_temp, line_pres, line_alt

# Función de actualización para la animación
def update(frame):
    data_list = load_data(json_filename)

    if not data_list:
        return line_temp, line_pres, line_alt

    # Extraer timestamps, temperaturas, presiones y altitudes
    global timestamps, temperature_data, pressure_data, altitude_data

    latest_data = data_list[-1]
    timestamps.append(latest_data['timestamp'])
    temperature_data.append(latest_data['temperature'])
    pressure_data.append(latest_data['pressure'])
    altitude_data.append(latest_data['altitude'])

    # Actualizar gráficos
    line_temp.set_data(timestamps, temperature_data)
    line_pres.set_data(timestamps, pressure_data)
    line_alt.set_data(timestamps, altitude_data)
    
    # Ajustar los límites de los ejes
    ax1.set_xlim(min(timestamps), max(timestamps))
    ax1.set_ylim(min(temperature_data) - 5, max(temperature_data) + 5)
    
    ax2.set_xlim(min(timestamps), max(timestamps))
    ax2.set_ylim(min(pressure_data) - 10, max(pressure_data) + 10)
    
    ax3.set_xlim(min(timestamps), max(timestamps))
    ax3.set_ylim(min(altitude_data) - 5, max(altitude_data) + 5)
    
    # Actualizar valores del giroscopio y UV
    gx_value.config(text=f"{latest_data['gx']}")
    gy_value.config(text=f"{latest_data['gy']}")
    gz_value.config(text=f"{latest_data['gz']}")
    gz_value.config(text=f"{latest_data['gz']}")
    uv_value.config(text=f"{latest_data['uvVoltage']:.2f} V")
    
    return line_temp, line_pres, line_alt

# Crear la animación
ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=1000)  # Intervalo en milisegundos

# Integrar la gráfica en el frame de Tkinter
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.get_tk_widget().pack(fill=BOTH, expand=1)

plt.tight_layout()
root.mainloop()
