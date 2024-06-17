from functools import partial
import tkinter as tk
from  tkinter import ttk
import numpy as np
import Dado as Dado
from tkinter import messagebox
from collections import Counter

#Yahtzee
class YahtzeeGame:
    def __init__(self, numJugadores, numLanzamientos):
        self.startVar = None
        self.numJugadores = numJugadores
        self.numLanzamientos = numLanzamientos
        self.jugadores = []
        self.lanzamiento = 0
        self.lanzamientoLabel = None


    def start(self):
        self.startVar = tk.Tk()
        self.startVar.geometry("800x800")
        sizeDado = 100

        inner_frame = tk.Frame(self.startVar)

        tk.Scrollbar(self.startVar, orient='vertical').pack(side='right', fill='y')

        label = tk.Label(self.startVar, text="Yahtzee", font=("Arial", 20, "bold"))
        label.pack()

        self.lanzamientoLabel = tk.Label(self.startVar, text="Lanzamientos", font=("Arial", 15, "bold"))
        self.lanzamientoLabel.pack(anchor='w', pady=10, padx=10)

        # Columnas de lanzamientos
        for jug in range(self.numJugadores):
            frame_jugador = tk.Frame(inner_frame)
            frame_jugador.pack(fill='x', pady=10)
            labelJugador = tk.Label(frame_jugador, text="Jugador "+str(jug+1), font=("Arial", 15, "bold"))
            labelJugador.pack(side='left')

            dadosList = []
            for i in range(5):
                random = np.random.randint(1, 6)
                canvas = tk.Canvas(frame_jugador, width=sizeDado, height=sizeDado,highlightthickness=2, highlightbackground="black")

                dad = Dado.Dado(random, sizeDado, canvas)
                dad.draw()
                canvas.bind("<Button-1>", dad.bloquearx)
                dadosList.append(dad)
                canvas.pack(side='left', padx=10)

            self.jugadores.append({
                "id": jug,
                "dados": dadosList,
                "puntaje": self.puntosListInicial(),
                "puntosDraw": [],
                "canChangeValue": True
            })

        inner_frame.pack(fill='x', pady=10, padx=10)


        #Columnas de puntajes
        labelPuntajes = tk.Label(self.startVar, text="Puntajes", font=("Arial", 15, "bold"))
        labelPuntajes.pack(anchor='w', pady=10, padx=10)

        self.drawTable()

        tk.Button(self.startVar, text="Lanzar", command=self.lanzar).pack(side='left', padx=10)
        tk.Button(self.startVar, text="Nueva Ronda", command=self.nuevaRonda).pack(side='left', padx=10)
        self.startVar.mainloop()

    def lanzar(self):
        if self.lanzamiento >= self.numLanzamientos:
            return
        self.lanzamiento += 1
        self.lanzamientoLabel.config(text="Lanzamientos: "+str(self.lanzamiento) + " de " + str(self.numLanzamientos))
        for jugador in self.jugadores:
            if(jugador["canChangeValue"]):
                for dado in jugador["dados"]:
                    dado.lanzar()

    def nuevaRonda(self):
        self.lanzamiento = 0
        self.lanzamientoLabel.config(text="Lanzamientos: "+str(self.lanzamiento) + " de " + str(self.numLanzamientos))
        for jugador in self.jugadores:
            jugador["canChangeValue"] = True
            for dado in jugador["dados"]:
                dado.reinicio()

    def drawTable(self):
        # Crear el marco principal
        main_frame = tk.Frame(self.startVar)
        main_frame.pack(fill='both', expand=True)
        validateCommand = self.startVar.register(self.only_numbers)

        # Crear los encabezados
        headers = ["Jugador", "1", "2", "3", "4", "5", "6", "3Iguales", "4Iguales", "Full", "EscaleraMenor", "EscaleraMayor", "Poker", "Chance"]
        for i, header in enumerate(headers):
            label = tk.Label(main_frame, text=header)
            label.grid(row=0, column=i)

        # Crear las filas de datos
        for j, jugador in enumerate(self.jugadores, start=1):
            for i, value in enumerate(headers):
                if(i == 0):
                    label = tk.Label(main_frame, text=j)
                else:
                    label = tk.Entry(main_frame, text="", name=str(j)+"-"+value, validate="key", validatecommand=(validateCommand, '%S'))
                    #label.bind("<FocusOut>", self.changeValue)
                    label.bind("<FocusOut>", self.changeValue)

                    jugador["puntosDraw"].append(label)
                label.grid(row=j, column=i)
        
        main_frame.pack()

    def changeValue(self, event):
        valor = event.widget.get()
        if(valor == ''):
            return
        split = event.widget.winfo_name().split("-")
        jugador = int(split[0])-1
        print(jugador)
        print(split[1])

        if(not self.jugadores[jugador]["canChangeValue"]):
            messagebox.showerror("Error", "No puedes cambiar el valor")
            self.jugadores[jugador]["puntaje"][split[1]] = 0
            event.widget.delete(0, 'end')
            event.widget.insert(0, 0)
            return

        self.jugadores[jugador]["puntaje"][split[1]] = 0 if valor == '' else int(valor)

        if(not self.validarPuntage(self.jugadores[jugador]["puntaje"][split[1]], jugador, split[1])):
            messagebox.showerror("Error", "El puntaje no es valido")
            self.jugadores[jugador]["puntaje"][split[1]] = 0
            event.widget.delete(0, 'end')
            event.widget.insert(0, 0)
            return
        
        self.jugadores[jugador]["canChangeValue"] = False

        #messagebox.showinfo("Título del cuadro de diálogo", "Mensaje de información")

    def only_numbers(self, char):
        return char.isdigit()

    def puntosListInicial(self):
        return {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0,
            "6": 0,
            "3Iguales": 0,
            "4Iguales": 0,
            "Full": 0,
            "EscaleraMenor": 0,
            "EscaleraMayor": 0,
            "Poker": 0,
            "Chance": 0,
        }


    def validarPuntage(self, puntaje, jugador, puntosId):
        puntosPersona = self.jugadores[jugador]["dados"]
        valorDados = []
        for x in puntosPersona:
            valorDados.append(x.lados)

        if("1" == puntosId):
            print(sum(x for x in valorDados if x == 1))
            return sum(x for x in valorDados if x == 1) == puntaje

        if("2" == puntosId):
            print(sum(x for x in valorDados if x == 2))
            sum(x for x in valorDados if x == 2) == puntaje
        
        if("3" == puntosId):
            print(sum(x for x in valorDados if x == 3))
            sum(x for x in valorDados if x == 3) == puntaje

        if("4" == puntosId):
            print(sum(x for x in valorDados if x == 4))
            sum(x for x in valorDados if x == 4) == puntaje

        if("5" == puntosId):
            print(sum(x for x in valorDados if x == 5))
            sum(x for x in valorDados if x == 5) == puntaje
        
        if("6" == puntosId):
            print(sum(x for x in valorDados if x == 6))
            sum(x for x in valorDados if x == 6) == puntaje

        if("4Iguales" == puntosId):
            return self.cuatroIguales(valorDados) == puntaje

        if("3Iguales" == puntosId):
            print(self.tresIguales(valorDados))
            return self.tresIguales(valorDados) == puntaje
        
        if("Full" == puntosId):
            if(self.full(valorDados)):
                return 25 == puntaje
            return False
        
        if("EscaleraMenor" == puntosId):
            if(self.escaleraMenor(valorDados)):
                return 30 == puntaje
            return False
        
        if("EscaleraMayor" == puntosId):
            if(self.escaleraMayor(valorDados)):
                return 40 == puntaje
            return False
        
        if("Poker" == puntosId):
            if(self.poker(valorDados)):
                return 50 == puntaje
        
        if("Chance" == puntosId):
            return sum(valorDados) == puntaje

        return True
    
    def tresIguales(self, valorDados):
        conteo = Counter(valorDados)
        print(conteo)
        for numero, cantidad in conteo.items():
            if cantidad >= 3:
                return numero * 3
        return 0
    
    def cuatroIguales(self, valorDados):
        conteo = Counter(valorDados)
        print(conteo)
        for numero, cantidad in conteo.items():
            if cantidad >= 4:
                return numero * 4
        return 0
    
    def full(self, valorDados):
        return any(valorDados.count(x) == 3 for x in valorDados) and any(valorDados.count(x) == 2 for x in valorDados)
    
    def escaleraMenor(self, valorDados):
        return True
        return any(valorDados.count(x) == 1 for x in valorDados) and any(valorDados.count(x) == 2 for x in valorDados) and any(valorDados.count(x) == 3 for x in valorDados) and any(valorDados.count(x) == 4 for x in valorDados)
    
    def escaleraMayor(self, valorDados):
        return True
        return any(valorDados.count(x) == 2 for x in valorDados) and any(valorDados.count(x) == 3 for x in valorDados) and any(valorDados.count(x) == 4 for x in valorDados) and any(valorDados.count(x) == 5 for x in valorDados)
    
    def poker(self, valorDados):
        conteo = Counter(valorDados)
        print(conteo)
        for numero, cantidad in conteo.items():
            if cantidad >= 5:
                return True
        return False
    