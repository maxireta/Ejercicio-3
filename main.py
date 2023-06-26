from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests

class Aplicacion():
    __ventana= None
    __dolares= None
    __pesos= None

    def __init__(self):
        self.__ventana = Tk()
        self.__ventana.geometry("300x150")
        self.__ventana.configure(bg='lightgrey')
        self.__ventana.title("Conversor de moneda")

        mainframe = ttk.Frame(self.__ventana, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        mainframe['borderwidth'] = 2
        mainframe['relief'] = 'sunken'

        self.__dolares = StringVar()
        self.__pesos = StringVar()
        self.__dolares.trace('w', self.calcular)

        self.dolaresEntry = ttk.Entry(mainframe, width=7, textvariable=self.__dolares)
        self.dolaresEntry.grid(column=2, row=1, sticky=(W, E))
            
        ttk.Label(mainframe, textvariable=self.__pesos).grid(column=2, row=2, sticky=(W, E))
        ttk.Label(mainframe, text=" dólares").grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text=" pesos").grid(column=3, row=2, sticky=W)

        ttk.Button(mainframe, text='Salir', command=self.__ventana.destroy).grid(column=3, row=3, sticky=W)
        ttk.Label(mainframe, text="es equivalente a").grid(column=1, row=2, sticky=W)

        for child in mainframe.winfo_children():
             child.grid_configure(padx=5, pady=5)
        self.dolaresEntry.focus()
        self.__ventana.mainloop()

    def calcular(self, *args):
        if self.dolaresEntry.get() != '':
            try:
                dolares = float(self.dolaresEntry.get())
                cotizacion= self.obtenerCotizacion()
                pesos = dolares * cotizacion
                self.__pesos.set(pesos)
                
            except ValueError:
                messagebox.showerror(title="Error de tipo", message="Debe ingresar un número")
                self.__pesos.set('')
                self.dolaresEntry.focus()
        else:
            self.__pesos.set('')

    def obtenerCotizacion(self):
        url = ' https://www.dolarsi.com/api/api.php?type=dolar'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            cotizacion = float(data[0]['casa']['venta'].replace(',','.'))
            return cotizacion
        else:
            messagebox.showerror(title="Error de conexión", message="No se pudo obtener la cotización")
            return 0

def testAPP():
    mi_app = Aplicacion()

if __name__ == '__main__':
    testAPP()
