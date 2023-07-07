import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class SistemaDeVenta:
    def __init__(self):
        self.sistema_de_venta = tk.Tk()
        self.sistema_de_venta.title("SISTEMA DE VENTA")

        # Variables
        self.productos = self.lista_productos()

        # Crear ventana principal
        self.crear_interfaz()

    def lista_productos(self):
        productos = [
            {"codigo": "001", "nombre": "pan", "precio": 10.99},
            {"codigo": "002", "nombre": "coca cola", "precio": 5.99},
            {"codigo": "003", "nombre": "inca cola", "precio": 15.99},
            # ...
        ]
        return productos

    def crear_interfaz(self):
        # Crear árbol (Treeview) con las columnas "Código", "Nombre" y "Precio"
        self.tabla_lista = ttk.Treeview(self.sistema_de_venta, columns=("codigo", "nombre", "precio"))
        self.tabla_lista.grid(row=0, column=0, columnspan=3)
        self.tabla_lista.column("#0", width=0)
        self.tabla_lista.heading("codigo", text="Código")
        self.tabla_lista.heading("nombre", text="Nombre")
        self.tabla_lista.heading("precio", text="Precio")

        # Insertar los productos en la tabla
        self.cargar_productos()

        # Texto de los productos
        tk.Label(text="Nombre:", font=("Arial", 12, "bold")).grid(row=2, column=0, padx=8, pady=5)
        tk.Label(text="Precio:", font=("Arial", 12, "bold")).grid(row=2, column=1, padx=8, pady=5)
        tk.Label(text="Código:", font=("Arial", 12, "bold")).grid(row=2, column=2, padx=8, pady=5)

        # Entrada de texto
        self.entry_nombre = tk.Entry(self.sistema_de_venta)
        self.entry_nombre.config(font="Arial")
        self.entry_nombre.grid(row=1, column=0, padx=8, pady=5)

        self.entry_precio = tk.Entry(self.sistema_de_venta)
        self.entry_precio.config(font="Arial")
        self.entry_precio.grid(row=1, column=1, padx=8, pady=5)

        self.entry_codigo = tk.Entry(self.sistema_de_venta)
        self.entry_codigo.config(font=("Arial"))
        self.entry_codigo.grid(row=1, column=2, padx=8, pady=5)

        # Botones de agregar, editar y eliminar
        tk.Button(
            text="Agregar", width=20, font=("Arial", 8, "bold"), fg="#FFFFFF", bg="#DC143C",
            command=self.agregar_producto
        ).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(
            text="Editar", width=20, font=("Arial", 8, "bold"), fg="#FFFFFF", bg="#DC143C",
            command=self.editar_producto
        ).grid(row=4, column=1, padx=10, pady=5)
        tk.Button(
            text="Eliminar", width=20, font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#DC143C",
            command=self.eliminar_producto
        ).grid(row=4, column=2, padx=8, pady=5)

        # Texto de la lista de productos en el carrito
        tk.Label(
            text="LISTA DE PRODUCTOS EN CARRITO", font=("Arial", 10)
        ).grid(row=5, column=1)

        # Lista de productos en el carrito
        self.tabla_carro = ttk.Treeview(self.sistema_de_venta, columns=("codigo", "nombre", "precio"))
        self.tabla_carro.grid(row=6, column=0, columnspan=3)
        self.tabla_carro.column("#0", width=0)
        self.tabla_carro.heading("codigo", text="Código")
        self.tabla_carro.heading("nombre", text="Nombre")
        self.tabla_carro.heading("precio", text="Precio")

        # Texto para el total
        tk.Label(text="TOTAL", font=("Arial", 10, "bold")).grid(row=7, column=1, pady=5, columnspan=2)

        # Entry para el total
        self.entry_total = tk.Entry(self.sistema_de_venta)
        self.entry_total.config(font=("Arial"))
        self.entry_total.grid(row=7, column=2)

        # Entry para el código del producto a agregar al carrito
        self.entry_codigo_para_agregar_a_carrito = tk.Entry(self.sistema_de_venta, width=15)
        self.entry_codigo_para_agregar_a_carrito.config(font=("Arial"))
        self.entry_codigo_para_agregar_a_carrito.grid(row=7, column=1)

        # Botones de agregar al carrito, nueva compra y venta
        tk.Button(
            text="AGREGAR AL CARRITO", width=20, font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#DC143C",
            command=self.agregar_al_carrito
        ).grid(row=7, column=0, pady=5)
        tk.Button(
            text="NUEVA COMPRA", width=20, font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#DC143C",
            command=self.nueva_compra
        ).grid(row=8, column=0, pady=5)
        tk.Button(
            text="VENTA", width=20, font=("Arial", 10, "bold"), fg="#FFFFFF", bg="#DC143C",
            command=self.realizar_venta
        ).grid(row=8, column=2, pady=5)

    def cargar_productos(self):
        # Limpiar tabla de productos
        for item in self.tabla_lista.get_children():
            self.tabla_lista.delete(item)

        # Insertar los productos en la tabla
        for producto in self.productos:
            codigo = producto["codigo"]
            nombre = producto["nombre"]
            precio = producto["precio"]
            self.tabla_lista.insert("", tk.END, values=(codigo, nombre, precio))

    def agregar_producto(self):
        nombre = self.entry_nombre.get()
        precio = self.entry_precio.get()
        codigo = self.entry_codigo.get()

        # Validar campos no vacíos
        if nombre and precio and codigo:
            nuevo_producto = {"codigo": codigo, "nombre": nombre, "precio": precio}
            self.productos.append(nuevo_producto)
            self.cargar_productos()
            self.limpiar_campos()

    def editar_producto(self):
        # Obtener el producto seleccionado
        item = self.tabla_lista.focus()
        if item:
            nombre = self.entry_nombre.get()
            precio = self.entry_precio.get()
            codigo = self.entry_codigo.get()

            # Validar campos no vacíos
            if nombre and precio and codigo:
                nuevo_producto = {"codigo": codigo, "nombre": nombre, "precio": precio}

                # Actualizar el producto en la lista
                index = self.tabla_lista.index(item)
                self.productos[index] = nuevo_producto

                self.cargar_productos()
                self.limpiar_campos()

    def eliminar_producto(self):
        # Obtener el producto seleccionado
        item = self.tabla_lista.focus()
        if item:
            # Eliminar el producto de la lista
            index = self.tabla_lista.index(item)
            del self.productos[index]

            self.cargar_productos()
            self.limpiar_campos()

    def agregar_al_carrito(self):
        codigo = self.entry_codigo_para_agregar_a_carrito.get()

        # Buscar el producto en la lista de productos
        producto = next((p for p in self.productos if p["codigo"] == codigo), None)
        if producto:
            # Insertar el producto en la tabla del carrito
            codigo = producto["codigo"]
            nombre = producto["nombre"]
            precio = producto["precio"]
            self.tabla_carro.insert("", tk.END, values=(codigo, nombre, precio))
            self.calcular_total()

    def calcular_total(self):
        total = 0
        # Obtener los precios de los productos en el carrito
        for item in self.tabla_carro.get_children():
            precio = float(self.tabla_carro.item(item)["values"][2])
            total += precio

        self.entry_total.delete(0, tk.END)
        self.entry_total.insert(tk.END, total)

    def nueva_compra(self):
        # Limpiar tabla del carrito y el campo del total
        for item in self.tabla_carro.get_children():
            self.tabla_carro.delete(item)
        self.entry_total.delete(0, tk.END)

    def generar_factura(self):
        # Crear el documento PDF
        c = canvas.Canvas("factura.pdf", pagesize=letter)

        # Título de la factura
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "FACTURA DE VENTA")

        # Información de los productos en el carrito
        y = 700
        for item in self.tabla_carro.get_children():
            codigo = self.tabla_carro.item(item)["values"][0]
            nombre = self.tabla_carro.item(item)["values"][1]
            precio = self.tabla_carro.item(item)["values"][2]
            c.setFont("Helvetica", 12)
            c.drawString(50, y, f"Código: {codigo}")
            c.drawString(150, y, f"Nombre: {nombre}")
            c.drawString(300, y, f"Precio: ${precio}")
            y -= 20

        # Total
        total = self.entry_total.get()
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y - 20, f"Total: ${total}")

        # Guardar y cerrar el documento PDF
        c.save()

    def realizar_venta(self):
        # Realizar las acciones necesarias para finalizar la venta
        self.generar_factura()
        self.nueva_compra()
        # Agregar aquí el código para guardar los datos de la venta, imprimir ticket, etc.

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_codigo.delete(0, tk.END)

    def iniciar_sistema(self):
        self.sistema_de_venta.mainloop()


# Crear instancia del sistema de venta y ejecutarlo
sistema_venta = SistemaDeVenta()
sistema_venta.iniciar_sistema()