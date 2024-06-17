import tkinter as tk
from PopupGame import YahtzeeGame

#Yahtzee
startVar = None
entryNumJugadores = None
entryNumLanzamientos = None
numJugadores = 0
numLanzamientos = 0

def start():
    global startVar
    startVar = tk.Tk()
    startVar.geometry("400x300")

    label = tk.Label(startVar, text="Yahtzee", font=("Arial", 20, "bold"))
    label.pack()

    button = tk.Button(startVar, text="Nuevo Juego", command=configJuego)
    button.pack()

    startVar.mainloop()

def configJuego():
    global startVar
    global entryNumJugadores
    global entryNumLanzamientos

    startVar.destroy()
    startVar = tk.Tk()
    startVar.geometry("400x300")
    label = tk.Label(startVar, text="Parametros del Juego", font=("Arial", 20, "bold"))
    label.pack(anchor='w', pady=10, padx=10)

    validateCommand = startVar.register(only_numbers)

    labelNumJugadores = tk.Label(startVar, text="Numero de Jugadores")
    labelNumJugadores.pack(anchor='w', padx=10)

    entryNumJugadores = tk.Entry(startVar, validate="key", validatecommand=(validateCommand, '%S'))
    entryNumJugadores.pack(pady=2, padx=10, fill='x', ipadx='5', ipady='5')

    labelNumLanzamientos = tk.Label(startVar, text="Numero de Lanzamientos")
    labelNumLanzamientos.pack(anchor='w', padx=10)

    entryNumLanzamientos = tk.Entry(startVar, validate="key", validatecommand=(validateCommand, '%S'))
    entryNumLanzamientos.pack(pady=2, padx=10, fill='x', ipadx='5', ipady='5')

    button = tk.Button(startVar, text="Continuar", command=startGame)
    button.pack(anchor='w', pady=5, padx=10, fill='x', ipadx='5', ipady='5')

    startVar.mainloop() 

def startGame():
    global numJugadores
    global numLanzamientos
    global entryNumJugadores
    global entryNumLanzamientos
    global startVar

    numJugadoresStr = entryNumJugadores.get()
    numLanzamientosStr = entryNumLanzamientos.get()

    if numJugadoresStr == "" or numLanzamientosStr == "":
        tk.messagebox.showerror("Error", "Debe llenar todos los campos")
        return
    
    numJugadores = int(numJugadoresStr)
    numLanzamientos = int(numLanzamientosStr)

    startVar.destroy()
    newGame = YahtzeeGame(numJugadores, numLanzamientos)
    newGame.start()

def only_numbers(char):
    return char.isdigit()

start()