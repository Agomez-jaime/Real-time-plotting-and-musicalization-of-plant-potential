
import openBCIStream
import numpy as np
import struct as st
import numpy as np
import matplotlib.pyplot as plt
import f_SignalProcFuncLibs as sigfun
from scamp import *
from matplotlib.animation import FuncAnimation
import time, threading
from timeloop import Timeloop
from datetime import timedelta


uV = (4500000)/24/(2**23-1) #convierte a uV

f1lp = 0.01
f1hp = 55
f2lp = 0.005
f2hp = 56
hayDatosParaPintar=False
procesando=False
cerrar=False
temp=80
rango = 200
volumen=0.8
longitud=0.05
conf = False
archivo = "output.wav"
instrumento="piano"
datosAPintar =  np.array([])
buffer=  np.array([])
datos = []


'''
def my_function(j):
    global datosAPintar
    global instrumento
    global rango
    global volumen
    global longitud
    global ax
    global hayDatosParaPintar
    global buffer
    global procesando
    global s

    Do = 60

    if not(hayDatosParaPintar):
       return

    if procesando:
        return
    procesando=True
    clarinet = s.new_part(instrumento)
    for i in range(0, len(buffer), 1):
        #print("i " + str(i))
        datosAPintar=np.append(datosAPintar,buffer[i])

        if i%25==0:
            val = buffer[i]
            sumador = int(val / rango)  # este cálculo cambia la nota según el número del potencial y el rango
            nota = Do + sumador  # está pensado para que funcione en tiempo real
            clarinet.play_note(nota, volumen, longitud)

    ax.plot(datosAPintar)
    espaciograf.draw()
    hayDatosParaPintar = False
    buffer =  np.array([])
    procesando = False
'''

def my_function(j):
    global datosAPintar
    global instrumento
    global rango
    global volumen
    global longitud
    global ax
    global hayDatosParaPintar
    global buffer

    global s

    Do = 60

    if not(hayDatosParaPintar):
       return



    clarinet = s.new_part(instrumento)
    for i in range(0, len(buffer), 1):
        #print("i " + str(i))
        datosAPintar=np.append(datosAPintar,buffer[i])

        if i%25==0:
            val = buffer[i]
            sumador = int(val / rango)  # este cálculo cambia la nota según el número del potencial y el rango
            nota = Do + sumador  # está pensado para que funcione en tiempo real
            ax.plot(datosAPintar)
            espaciograf.draw()
            clarinet.play_note(nota, volumen, longitud)

    #ax.plot(datosAPintar)
    #espaciograf.draw()
    hayDatosParaPintar = False
    buffer =  np.array([])




t1 = Timeloop()

@t1.job(interval=timedelta(seconds=1))
def prueba():
    global buffer
    global hayDatosParaPintar
    global procesando


    if procesando:
        return
    procesando = True
    s_FsHz = 250

    #while True:
    datosarr = np.array(board.poll(420))

    st_Filt = sigfun.f_GetIIRFilter(s_FsHz, [f1lp, f1hp], [f2lp, f2hp])
    v_SigFilt = sigfun.f_IIRBiFilter(st_Filt, datosarr[:, 0])

    buffer = np.array(v_SigFilt) * uV

    hayDatosParaPintar = True
    my_function(1)
    procesando = False

    #if not (cerrar):
    #    threading.Timer(1, prueba).start()
'''


while True:
    s_FsHz = 250
    recoger = np.zeros(2)
    #toma = np.array(sample.channels_data) * uV
    datosarr = np.array(board.poll(420))
 #   print(datosarr)
    st_Filt = sigfun.f_GetIIRFilter(s_FsHz, [f1lp, f1hp], [f2lp, f2hp])
    v_SigFilt = sigfun.f_IIRBiFilter(st_Filt, datosarr[:, 0])
    toma = np.array(v_SigFilt) * uV
    buffer = np.append(buffer, toma)
    hayDatosParaPintar = True
    my_function(1)
    time.sleep(1)  # Seconds
    #datosAPintar = np.append(datosAPintar, v_SigFilt)

    #playmusic(v_SigFilt)
 #   print(board.count)
   # print(df_ecg)

    #data = board.data()
    

    print(board.count)
    print (board.canales())
    for count, channel in enumerate(board.canales()):
        print('Datos canal %d' % channel)
        print(data[channel])
   # print(board.canales())
    #for count
    #print(df_ecg)
    break
    #ecg.extend(df_ecg.iloc[:, 0].values)
'''
'''

  
    recoger[0] = toma[0]
    recoger[1] = toma[1]
    datos.append(recoger)
    print("bringing")
    if len(datos) >= 420:
        datosarr = np.array(datos)
        datos.clear()
        st_Filt = sigfun.f_GetIIRFilter(s_FsHz, [f1lp, f1hp], [f2lp, f2hp])
        v_SigFilt = sigfun.f_IIRBiFilter(st_Filt, datosarr[:, 0])
        buffer = np.append(buffer, v_SigFilt)
        hayDatosParaPintar = True
        datosAPintar = np.append(datosAPintar, v_SigFilt)
        playmusic(v_SigFilt)
        print("ya hay datos")

'''
def Instrumentacion(instrum):
    global instrumento
    instrumento = instrum

def ActualizarFilt():
    global f1lp
    global f1hp
    global f2lp
    global f2hp
    f1lp = float(ef1lp.get())
    f1hp = float(ef1hp.get())
    f2lp = float(ef2lp.get())
    f2hp = float(ef2hp.get())

def ActualizarMusc():
    global temp
    global rango
    global volumen
    global longitud
    temp = int(etemp.get())
    rango = int(erango.get())
    volumen = float(evol.get())
    longitud = float(elong.get())

#Exportar datos
#Función que escribe los datos de la gráfica en tipo double en un archivo, de nombre elegido por el usuario
def Exportar():
    global datosAPintar
    #global nombre
    global cerrar
    print("2")
    mensaje = tk.messagebox.askquestion('¿Dejar de transmitir en vivo?', '¿Está seguro que desea dejar de transmitir en vivo y exportar?',
                                        icon='warning')
    print(mensaje)
    if mensaje == 'yes':
        nombre = etxt.get()
        print(nombre)
        file = open(nombre, "w")
        board.stop_stream()
        t1.stop()
        cerrar = True
        for dato in datosAPintar:
            file.write(str(dato) + "\n")
        file.close()
        tk.messagebox.showinfo(title="Message box",
                               message="Los datos  de la gráfica \nhan sido exportados con éxito.",
                               icon='info')  # mensaje de exportación exitosa

#Exportar sonido
def Archivar():
    archivo = ewav.get()
    playback_settings.recording_file_path = archivo
    tk.messagebox.showinfo(title="Message box",
                           message="El sonido será guardado en un archivo .wav.",
                           icon='info')


def Start():
    t1.start()
    #prueba()


def Cerrar(): #función que pregunta salida del GUI
    global cerrar
    mensaje= tk.messagebox.askquestion ('¿Cerrar Aplicación?','¿Está seguro que desea cerrar la aplicación?', icon = 'warning')
    if mensaje == 'yes':
       ventana.destroy()
       board.stop_stream()
       t1.stop()
       cerrar=True
    else:
        tk.messagebox.showinfo('Retornar','Retornando a la aplicación')

import tkinter as tk
import matplotlib
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)



matplotlib.use("TkAgg")

# 1er Parte Fundamental: Definir la VEntana!  Tk()
ventana = tk.Tk()
ventana.wm_title("Transformación de los potenciales de una planta en sonido - Andrea Gómez, 2021-20") #nombre de la ventana
ventana.geometry('850x650')
ventana.config(bg="black", cursor="gumby") #elección de cursor
titulo = tk.Label(ventana,
                  font= ('Times New Roman', 20),
                  fg= "#D3B6F9",  #color de fuente
                  bg="black",
                  text="Transformación de los potenciales \nde una planta en sonido")
titulo.place(x=230,y=15)

#frames
parametros = tk.Frame(master=ventana)
parametros.place(x=50, y=210) #se coloca el frame en la principal
parametros.config(bg="#F4D03F", width=300, height=210, relief=tk.GROOVE, bd=8) #color, relieve tamaño del frame
menu = tk.Frame(master=ventana)
menu.place(x=50, y=100) #se coloca el frame en la principal
menu.config(bg="#59D533", width=300, height=100, relief=tk.GROOVE, bd=8)
filtro = tk.Frame(master=ventana)
filtro.place(x=50, y=430) #se coloca el frame en la principal
filtro.config(bg="#33C8D5", width=300, height=200, relief=tk.GROOVE, bd=8)
exp = tk.Frame(master=ventana)
exp.place(x=400,y=525)
exp.config(bg="#BBB1FE", width=400, height=100, relief=tk.GROOVE, bd=8)

#Estilo botones
Style = ttk.Style()
Style.configure('E1.TButton', font =('Times', 10, 'underline'), foreground = '#FC0C01', background = '#FFFFFF') #primer tipo de estilo de botón
Style.map("E1.TButton",
           foreground=[('pressed', 'red'), ('active', 'tomato')],  #colores según el estado del botón
           background=[('pressed', '!disabled', 'red'), ('active', 'tomato')])
Style.configure('E2.TButton', font =('Times', 10, 'underline'), foreground = '#53AA25', background= '#FFFFFF') #segundo tipo de estilo
Style.map("E2.TButton",
           foreground=[('pressed', 'darkgreen'), ('active', '#53AA25')],   #colores según el estado del botón
           background=[('pressed', '!disabled', 'darkgreen'), ('active', '#53AA25')])
Style.configure('E3.TButton', font =('Times', 10, 'underline'), foreground = '#4608AA', background = '#FFFFFF') #tercer tipo de estilo
Style.map("E3.TButton",
           foreground=[('pressed', 'darkgreen'), ('active', '#4608AA')],   #colores según el estado del botón
           background=[('pressed', '!disabled', 'darkgreen'), ('active', '#4608AA')])

#etiquetas para el título del frame y
#los parámetros a cambiar por el usuario
lp = tk.Label(parametros,
                  font= ('Times New Roman', 17),
                  fg= "#4608AA",
                  bg = "#F4D03F",
                  text="Parámetros").place(x=7,y=2)
#Tempo
ltemp = tk.Label(parametros,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#F4D03F",
                  text="Tempo"
                  ).place(x=7,y=40)
#Rango
lrango = tk.Label(parametros,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#F4D03F",
                  text="Rango"
                  ).place(x=7,y=80)
#Volumen
lvol = tk.Label(parametros,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#F4D03F",
                  text="Volumen [0-1]"
                  ).place(x=7,y=120)
#Longitud
llong = tk.Label(parametros,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#F4D03F",
                  text="Longitud"
                  ).place(x=7,y=160)
#Instrumentos
linstr = tk.Label(menu,
                  font= ('Times New Roman', 17),
                  fg= "#4608AA",
                  bg = "#59D533",
                  text="Instrumento").place(x=7,y=2)
#Menu desplegable
llong = tk.Label(menu,
                  font= ('Times New Roman', 11),
                  fg= "#4608AA",
                  bg = "#59D533",
                  text="Haga click para despejar \nel menu"
                  ).place(x=7,y=35)
#Filtro
lfilt = tk.Label(filtro,
                  font= ('Times New Roman', 17),
                  fg= "#4608AA",
                  bg = "#33C8D5",
                  text="Filtro").place(x=7,y=2)
#Filtro 1 pasa bajas
lf1lp = tk.Label(filtro,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#33C8D5",
                  text="Filtro 1 pasa bajas"
                  ).place(x=7,y=35)
#Filtro 1 pasa altas
lf1hp = tk.Label(filtro,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#33C8D5",
                  text="Filtro 1 pasa altas"
                  ).place(x=7,y=75)
#Filtro 2 pasa bajas
lf2lp = tk.Label(filtro,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#33C8D5",
                  text="Filtro 2 pasa bajas"
                  ).place(x=7,y=115)
#Filtro 2 pasa altas
lf2hp = tk.Label(filtro,
                  font= ('Times New Roman', 14),
                  fg= "#4608AA",
                  bg = "#33C8D5",
                  text="Filtro 2 pasa altas"
                  ).place(x=7,y=155)
#Exportar sonido
lexs = tk.Label(exp,
                  font= ('Times New Roman', 11),
                  fg= "#41079F",
                  bg = "#BBB1FE",
                  text="Configure antes de transmitir"
                  ).place(x=0,y=15)
#Exportar datos
lexd = tk.Label(exp,
                  font= ('Times New Roman', 11),
                  fg= "#41079F",
                  bg = "#BBB1FE",
                  text="Configure después de transmitir"
                  ).place(x=0,y=46)
#widgets de entrada para cambiar los valores de los parámetros y insercción de valores sugeridos para cada uno
#Filtro 1 pasa bajas
sf1lp = tk.StringVar()
sf1lp.set("0.01")
ef1lp = ttk.Entry(master=filtro, textvariable=sf1lp, width=15)
ef1lp.place(x=180,y=35)
#Filtro 1 pasa altas
sf1hp = tk.StringVar()
sf1hp.set("55")
ef1hp = ttk.Entry(master=filtro, textvariable=sf1hp, width=15)
ef1hp.place(x=180,y=75)
#Filtro 2 pasa bajas
sf2lp = tk.StringVar()
sf2lp.set("0.005")
ef2lp = ttk.Entry(master=filtro, textvariable=sf2lp, width=15)
ef2lp.place(x=180,y=115)
#Filtro 2 pasa altas
sf2hp = tk.StringVar()
sf2hp.set("0.56")
ef2hp = ttk.Entry(master=filtro, textvariable=sf2hp, width=15)
ef2hp.place(x=180,y=155)

#Tempo
stemp = tk.StringVar()
stemp.set("80")
etemp = ttk.Entry(master=parametros, textvariable=stemp, width=15)
etemp.place(x=180,y=40)
#Rango
srango = tk.StringVar()
srango.set("200")
erango = ttk.Entry(master=parametros, textvariable=srango, width=15)
erango.place(x=180,y=80)
#Volumen
svol = tk.StringVar()
svol.set("0.8")
evol = ttk.Entry(master=parametros, textvariable=svol, width=15)
evol.place(x=180,y=120)
#Longitud
slong = tk.StringVar()
slong.set("0.2")
elong = ttk.Entry(master=parametros, textvariable=slong, width=15)
elong.place(x=180,y=160)

#Menú desplegable
opcionesintrumentos = ["Piano", "Strings SP1", "Trombone", "Cello", "Oboe", "Marimba", "Jazz Guitar", "Taiko Drum"]
sinstr = tk.StringVar(menu)
sinstr.set(opcionesintrumentos[0]) # default value

minstr = tk.OptionMenu(menu, sinstr, *opcionesintrumentos, command = Instrumentacion)
minstr.pack()
minstr.place(x=175, y= 40)

#Entrada para cambiar el nombre del archivo con el sonido a exportar
swav = tk.StringVar()
swav.set("SonidoPlanta.wav")
ewav = ttk.Entry(master=exp, textvariable=swav, width=18)
ewav.place(x=190,y=16)

#Entrada para cambiar el nombre del archivo con los datos a exportar
stxt = tk.StringVar()
stxt.set("PotencialesPlanta.txt")
etxt = ttk.Entry(master=exp, textvariable=stxt, width=18)
etxt.place(x=190,y=47)

#Actualizar datos pymusic
Musica = ttk.Button(master=parametros, text="Actualizar", style = "E3.TButton", command = ActualizarMusc).place(x=200,y=5)
#Actualizar datos filtro
Filtro = ttk.Button(master=filtro, text="Actualizar", style = "E3.TButton", command = ActualizarFilt).place(x=200,y=5)
#Botón que activa función de exportar sonido
Exportarsd = ttk.Button(master=exp, text="Exportar", style = "E3.TButton", command = Archivar).place(x=307, y=15)
#Botón que activa función de exportar datos
Exportartxt = ttk.Button(master=exp, text="Exportar txt", style = "E3.TButton", command = Exportar).place(x=307, y=45)
#Botón inicio
Start = ttk.Button(master=ventana, text="Start", style = "E2.TButton", command = Start).place(x=760,y=15)
#botón enlazado a función de cerrar
Cerrar = ttk.Button(master=ventana, text="X", style = "E1.TButton", command = Cerrar).place(x=8,y=15)

#Gráfica
figure = plt.Figure(figsize=(4, 4), dpi=100)
ax = figure.add_subplot(111)
ax.set_title('Potencial')
espaciograf = FigureCanvasTkAgg(figure, master = ventana)
espaciograf.get_tk_widget().place(x=400,y=100)

#Musc
s = Session(tempo=100)

#BCI
board= openBCIStream.CytonBoard("COM4")
board.start_stream()

ventana.mainloop()
