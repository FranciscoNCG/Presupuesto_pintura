from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

espacios = []  # Lista para guardar todos los datos ingresados

def preguntar_si(texto):
    respuesta = input(texto + ' (s/n): ').strip().lower()
    return respuesta == 's'

def calcular_superficie():
    print("\n📐 Empecemos con un nuevo espacio...")
    nombre = input("👉 Nombre del espacio: ")
    largo = float(input("   Largo (en metros): "))
    ancho = float(input("   Ancho (en metros): "))
    alto = float(input("   Alto (en metros): "))

    superficie_total = 0
    detalle_paredes = []

    if preguntar_si("🎨 ¿Querés pintar las 4 paredes?"):
        pared1 = largo * alto
        pared2 = largo * alto
        pared3 = ancho * alto
        pared4 = ancho * alto
        detalle_paredes = [pared1, pared2, pared3, pared4]
        superficie_total += sum(detalle_paredes)
    elif preguntar_si("🧱 ¿Querés seleccionar cuántas paredes pintar?"):
        cantidad = int(input("¿Cuántas paredes querés pintar? (1 a 3): "))
        for i in range(1, cantidad + 1):
            print(f"   👉 Medidas de la pared {i}:")
            base = float(input("      Ancho o largo (en metros): "))
            altura = float(input("      Altura (en metros): "))
            superficie = base * altura
            detalle_paredes.append(superficie)
            superficie_total += superficie

    if preguntar_si("🪄 ¿Querés pintar el techo?"):
        techo = largo * ancho
        superficie_total += techo
    else:
        techo = 0

    if preguntar_si("🧽 ¿Querés pintar el piso?"):
        piso = largo * ancho
        superficie_total += piso
    else:
        piso = 0

    print(f'\n✅ {nombre} – Superficie total a pintar: {superficie_total:.2f} m²')

    espacios.append({
        "nombre": nombre,
        "largo": largo,
        "ancho": ancho,
        "alto": alto,
        "paredes": detalle_paredes,
        "techo": techo,
        "piso": piso,
        "superficie_total": superficie_total
    })

def obtener_numero_presupuesto():
    archivo = "contador.txt"
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            f.write("1")
        return "P-0001"
    with open(archivo, "r+") as f:
        numero = int(f.read().strip())
        siguiente = numero + 1
        f.seek(0)
        f.write(str(siguiente))
        f.truncate()
    return f"P-{numero:04d}"

def exportar_presupuesto_a_pdf(lista_espacios, cliente, contacto, direccion, precio_m2, numero_presupuesto, archivo="presupuesto_final.pdf"):
    c = canvas.Canvas(archivo, pagesize=A4)
    ancho, alto = A4
    margen = 50
    y = alto - 60

    try:
        c.drawImage("logo.png", ancho - 130, y - 20, width=80, preserveAspectRatio=True, mask='auto')
    except:
        pass

    c.setFont("Helvetica-Bold", 16)
    c.drawString(margen, y, "Presupuesto de Pintura")
    c.setFont("Helvetica", 10)
    c.drawString(margen, y - 20, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    c.drawString(margen, y - 35, f"Número: {numero_presupuesto}")
    y -= 60

    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, f"Cliente: {cliente}")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(margen, y, f"Domicilio: {direccion}")
    y -= 15
    c.drawString(margen, y, f"Contacto: {contacto}")
    y -= 30

    for espacio in lista_espacios:
        if y < 180:
            c.showPage()
            y = alto - 60

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen, y, f"🔹 {espacio['nombre']}")
        y -= 20
        c.setFont("Helvetica", 10)
        c.drawString(margen + 10, y, f"Dimensiones: {espacio['largo']} x {espacio['ancho']} x {espacio['alto']} m")
        y -= 20

        data = [["Elemento", "Superficie (m²)"]]
        for i, sup in enumerate(espacio['paredes'], 1):
            data.append([f"Pared {i}", f"{sup:.2f}"])
        if espacio['techo']:
            data.append(["Techo", f"{espacio['techo']:.2f}"])
        if espacio['piso']:
            data.append(["Piso", f"{espacio['piso']:.2f}"])
        data.append(["Total", f"{espacio['superficie_total']:.2f}"])

        tabla = Table(data, colWidths=[120, 100])
        tabla.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))
        w, h = tabla.wrapOn(c, 0, 0)
        tabla.drawOn(c, margen, y - h)
        y -= h + 10

        total = espacio['superficie_total'] * precio_m2
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margen + 10, y, f"💰 Estimación: {espacio['superficie_total']:.2f} m² x ${precio_m2} = ${total:,.2f}")
        y -= 40

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(margen, 30, "Presupuesto generado por CG Pintores – Gracias por elegirnos 🖌️")

    c.save()
    print(f"\n📄 Presupuesto guardado como '{archivo}'")

# --- PROGRAMA PRINCIPAL ---
print("🛠️ Bienvenido a CG Pintores – Generador de Presupuestos 🎨")

# Datos del cliente
cliente = input("🧑 Nombre del cliente: ")
direccion = input("🏠 Domicilio: ")
contacto = input("☎️ Contacto (teléfono o email): ")

# Precio por m²
while True:
    try:
        precio_m2 = float(input("💰 Precio por metro cuadrado ($): "))
        break
    except ValueError:
        print("Por favor, ingresá un número válido.")

# Ingreso de espacios
seguir = True
while seguir:
    calcular_superficie()
    seguir = preguntar_si("➕ ¿Querés agregar otro ambiente?")

# Mostrar resumen
print("\n🧾 Resumen general:")
for espacio in espacios:
    print(f"🔸 {espacio['nombre']}: {espacio['superficie_total']:.2f} m² totales")

# Generar presupuesto
numero = obtener_numero_presupuesto()
exportar_presupuesto_a_pdf(espacios, cliente, contacto, direccion, precio_m2, numero)