import random


class Dado:
    def __init__(self, lados, size, canvas):
        self.size = size
        self.canvas = canvas
        self._bloquear = False
        self.x = (self.canvas.winfo_width() - self.size) / 2
        self.y = (self.canvas.winfo_height() - self.size) / 2
        self._color = 'black'
        if(lados < 1):
            self._lados = self.ladosRandom()
        else:
            self._lados = lados

    def ladosRandom(self):
        return random.randint(1, 6)
    
    def lanzar(self):
        if self._bloquear:
            return
        
        self._lados = self.ladosRandom()
        self.cleanCanvas()
        self.draw()
    
    def cleanCanvas(self):
        self.canvas.delete("all")
    
    def __str__(self):
        return str(self._lados) + " lados"
    
    
    @property
    def lados(self):
        return self._lados
    
    @property
    def bloquear(self):
        return self._bloquear
    
    @bloquear.setter
    def bloquear(self, event, value = False):
        self._bloquear = value

    def bloquearx(self, event):
        self._bloquear = not self._bloquear
        if(self._bloquear):
            self._color = 'yellow'
        else:
            self._color = 'black'

        self.cleanCanvas()
        self.draw()

    def reinicio(self):
        self._bloquear = False
        self._color = 'black'
        self.cleanCanvas()
        self.draw()

    def draw(self):
        sizePercent = self.size*0.08
        sizeDiv = self.size/4

        if(self._lados == 2 or self._lados == 3 or self._lados == 4 or self._lados == 5 or self._lados == 6):
            #superior izquierda
            self.canvas.create_oval(sizeDiv-sizePercent, sizeDiv-sizePercent, sizeDiv+sizePercent, sizeDiv+sizePercent, fill=self._color)
            #inferior derecha
            self.canvas.create_oval((sizeDiv*3)-sizePercent, (sizeDiv*3)-sizePercent, (sizeDiv*3)+sizePercent, (sizeDiv*3)+sizePercent, fill=self._color)

        if(self._lados == 4 or self._lados == 5 or self._lados == 6):
            #inferior izquierda
            self.canvas.create_oval(sizeDiv-sizePercent, (sizeDiv*3)-sizePercent, sizeDiv+sizePercent, (sizeDiv*3)+sizePercent, fill=self._color)
            #superior derecha
            self.canvas.create_oval((sizeDiv*3)-sizePercent, sizeDiv-sizePercent, (sizeDiv*3)+sizePercent, sizeDiv+sizePercent, fill=self._color)

        if(self._lados == 6):
            #superior centro
            self.canvas.create_oval((sizeDiv*2)-sizePercent, sizeDiv-sizePercent, (sizeDiv*2)+sizePercent, sizeDiv+sizePercent, fill=self._color)
            #inferior centro
            self.canvas.create_oval((sizeDiv*2)-sizePercent, (sizeDiv*3)-sizePercent, (sizeDiv*2)+sizePercent, (sizeDiv*3)+sizePercent, fill=self._color)
            #centro izquierda
            self.canvas.create_oval(sizeDiv-sizePercent, (sizeDiv*2)-sizePercent, sizeDiv+sizePercent, (sizeDiv*2)+sizePercent, fill=self._color)
            #centro derecha
            self.canvas.create_oval((sizeDiv*3)-sizePercent, (sizeDiv*2)-sizePercent, (sizeDiv*3)+sizePercent, (sizeDiv*2)+sizePercent, fill=self._color)

        if(self._lados == 1 or self._lados == 3 or self._lados == 5 or self._lados == 6):
            #centro
            self.canvas.create_oval((sizeDiv*2)-sizePercent, (sizeDiv*2)-sizePercent, (sizeDiv*2)+sizePercent, (sizeDiv*2)+sizePercent, fill=self._color)
        
    