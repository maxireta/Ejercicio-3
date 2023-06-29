import requests
from tkinter import *
from tkinter import ttk

class Ventana:
    def __init__(self):
        self.__ventana = Tk()
        self.__ventana.geometry("300x130")
        self.__ventana.title("Conversor de moneda")
        self.__dolar = StringVar()
        self.__pesos = DoubleVar()
        todo = LabelFrame(self.__ventana, width= 300, height=130, borderwidth=2, relief= "sunken").place(x=0, y=0)
        ttk.Label(todo, text="Dólares").place(x=160, y=20)
        ttk.Label(todo, text="Pesos").place(x=160, y= 50)
        ttk.Label(todo, text="Es equivalente a:").place(x=5, y=50)
        ttk.Label(todo, textvariable= self.__pesos).place(x=100, y=50)
        self.__en = ttk.Entry(todo, width= 8, textvariable= self.__dolar).place(x=100, y=20)
        ttk.Button(todo, text= "Salir", width= 12, command= self.__ventana.destroy).place(x=160, y=70)
        self.__dolar.trace("w", self.calcular)
        self.__ventana.mainloop()
    def calcular(self, *args):
        try:
            dolar = self.__dolar.get()
            dolar = dolar.replace(",", ".")
            dolar = float(dolar)
            coti = self.cotizar()
            pesos = (dolar * coti)
            self.__pesos.set(round(pesos, 2))
        except ValueError:
            self.__pesos.set("")
    def cotizar(self):
        try:
            url = requests.get("https://www.dolarsi.com/api/api.php?type=dolar")
            data = url.json()
            band = False
            i = 0
            while band is False and i < len(data):
                casa = data[i]
                if casa['casa']['nombre'] == 'Oficial':
                    cotizar = casa['casa']['venta']
                    cotizar = cotizar.replace(",", ".")
                    cotizar = float(cotizar)
                    band = True
                i += 1
            return cotizar
            raise Exception("No se encontró la cotización del dolar oficial.")
        except (requests.exceptions.RequestException, ValueError, KeyError):
            raise Exception('Error al obtener la cotización del dólar')