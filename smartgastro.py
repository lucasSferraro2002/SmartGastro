class Producto:
    def __init__(self, nombre, precio, stock, stock_minimo):
        self.nombre = nombre
        self.precio = precio
        self._stock = stock
        self.stock_minimo = stock_minimo

    def get_stock(self):
        return self._stock

    def agregar_stock(self, cantidad):
        if cantidad <= 0:
            print("Error: la cantidad debe ser mayor a 0.")
            return
        self._stock += cantidad
        print(f"Stock actualizado. Stock actual de {self.nombre}: {self._stock}")

    def vender(self, cantidad):
        if cantidad <= 0:
            print("Error: la cantidad debe ser mayor a 0.")
            return False
        if self._stock == 0:
            print(f"Error: {self.nombre} no tiene stock disponible.")
            return False
        if cantidad > self._stock:
            print(f"Error: stock insuficiente. Stock actual de {self.nombre}: {self._stock}")
            return False
        self._stock -= cantidad
        if self._stock <= self.stock_minimo:
            print(f"⚠️  Alerta: el stock de {self.nombre} está por debajo del mínimo.")
        return True

    def mostrar_info(self):
        print(f"Producto: {self.nombre} | Precio: ${self.precio} | Stock: {self._stock} | Mínimo: {self.stock_minimo}")


class Inventario:
    def __init__(self):
        self._productos = []

    def agregar_producto(self, producto):
        for p in self._productos:
            if p.nombre.lower() == producto.nombre.lower():
                print(f"Error: el producto '{producto.nombre}' ya existe en el inventario.")
                return
        self._productos.append(producto)
        print(f"Producto '{producto.nombre}' agregado al inventario.")

    def buscar_producto(self, nombre):
        for p in self._productos:
            if p.nombre.lower() == nombre.lower():
                return p
        return None

    def mostrar_inventario(self):
        if len(self._productos) == 0:
            print("El inventario está vacío.")
            return
        print("\n--- INVENTARIO ACTUAL ---")
        for p in self._productos:
            p.mostrar_info()
        print("------------------------\n")


class Foodtruck:
    def __init__(self, nombre):
        self.nombre = nombre
        self.inventario = Inventario()
        self._ventas = []

    def registrar_venta(self, nombre_producto, cantidad):
        producto = self.inventario.buscar_producto(nombre_producto)
        if producto is None:
            print(f"Error: el producto '{nombre_producto}' no existe en el inventario.")
            return
        if producto.vender(cantidad):
            venta = {
                "producto": producto.nombre,
                "cantidad": cantidad,
                "subtotal": producto.precio * cantidad
            }
            self._ventas.append(venta)
            print(f"Venta registrada: {cantidad}x {producto.nombre} — Subtotal: ${venta['subtotal']}")

    def mostrar_resumen_ventas(self):
        if len(self._ventas) == 0:
            print("No hay ventas registradas.")
            return
        print("\n--- RESUMEN DE VENTAS ---")
        total = 0
        for v in self._ventas:
            print(f"{v['cantidad']}x {v['producto']} — ${v['subtotal']}")
            total += v['subtotal']
        print(f"Total del día: ${total}")
        print("-------------------------\n")


def menu():
    print("\n¡Bienvenido a SmartGastro!")
    nombre_truck = input("Ingresá el nombre de tu Foodtruck: ")
    truck = Foodtruck(nombre_truck)

    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Agregar producto al inventario")
        print("2. Registrar una venta")
        print("3. Mostrar inventario actual")
        print("4. Ver resumen de ventas")
        print("5. Salir")
        print("----------------------")

        opcion = input("Elegí una opción: ")

        if opcion == "1":
            nombre = input("Nombre del producto: ")
            try:
                precio = float(input("Precio: "))
                stock = int(input("Stock inicial: "))
                stock_minimo = int(input("Stock mínimo: "))
            except ValueError:
                print("Error: ingresá un número válido.")
                continue
            producto = Producto(nombre, precio, stock, stock_minimo)
            truck.inventario.agregar_producto(producto)

        elif opcion == "2":
            nombre = input("Nombre del producto a vender: ")
            try:
                cantidad = int(input("Cantidad: "))
            except ValueError:
                print("Error: ingresá un número entero válido.")
                continue
            truck.registrar_venta(nombre, cantidad)

        elif opcion == "3":
            truck.inventario.mostrar_inventario()

        elif opcion == "4":
            truck.mostrar_resumen_ventas()

        elif opcion == "5":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida. Ingresá un número del 1 al 5.")


menu()
