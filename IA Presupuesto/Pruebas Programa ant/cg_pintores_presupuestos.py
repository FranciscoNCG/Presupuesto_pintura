from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

espacios = []  # Lista para guardar todos los datos de los ambientes

# 👉 Función para preguntar respuestas sí/no
def preguntar_si(texto):
    respuesta = input(texto + ' (s/n): ').strip().lower()
    return respuesta == 's'

# 🎯 Función para calcular la superficie de cada espacio
def calcular_superficie():
    print("\n📐 Empecemos con un nuevo ambiente...")
    nombre = input("👉 Nombre del espacio: ")
    largo = float(input("   Largo (en metros): "))
    ancho = float(input("   Ancho (en metros): "))
    alto = float(input("   Alto (en metros): "))

    superficie_total = 0
    detalle_paredes = []

    if preguntar_si("🎨 ¿Querés pintar las 4 paredes?"):
        detalle_paredes = [largo * alto] * 2 + [ancho * alto] * 2
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

    techo = largo * ancho if preguntar_si("🪄 ¿Querés pintar el techo?") else 0
    superficie_total += techo

    piso = largo * ancho if preguntar_si("🧽 ¿Querés pintar el piso?") else 0
    superficie_total += piso

    print(f'\n✅ {nombre} – Superficie total a pintar: {superficie_total:.2f} m²')

    # Guardamos los datos
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

# 🔢 Genera o incrementa el número del presupuesto
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

# 🖨️ Genera el PDF con estilo profesional
def exportar_presupuesto_a_pdf(lista_espacios, cliente, contacto, direccion, precio_m2, numero_presupuesto, archivo="presupuesto_final.pdf"):
    c = canvas.Canvas(archivo, pagesize=A4)
    ancho, alto = A4
    margen = 50
    y = alto - 60

    # 🔲 Encabezado con fondo gris claro
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.rect(0, alto - 80, ancho, 80, fill=1, stroke=0)
    c.setFillColor(colors.black)

    try:
        c.drawImage(logo.png, ancho - 140, alto - 70, width=80, preserveAspectRatio=True, mask='auto')
    except:
        c.setFont("Helvetica", 8)
        c.drawString(ancho - 140, alto - 30, "[logo.png no encontrado]")

    c.setFont("Helvetica-Bold", 18)
    c.drawString(margen, alto - 40, "Presupuesto de Pintura")
    c.setFont("Helvetica", 10)
    c.drawString(margen, alto - 55, f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
    c.drawString(margen, alto - 68, f"Número: {numero_presupuesto}")
    y = alto - 100

    # 🧑 Datos del cliente
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margen, y, f"Cliente: {cliente}")
    y -= 15
    c.setFont("Helvetica", 10)
    c.drawString(margen, y, f"Domicilio: {direccion}")
    y -= 15
    c.drawString(margen, y, f"Contacto: {contacto}")
    y -= 25

    # ➕ Ambientes
    for espacio in lista_espacios:
        if y < 180:
            c.showPage()
            y = alto - 100

        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen, y, f"🔹 {espacio['nombre']}")
        y -= 18
        c.setFont("Helvetica", 10)
        c.drawString(margen + 10, y, f"Dimensiones: {espacio['largo']} x {espacio['ancho']} x {espacio['alto']} m")
        y -= 20

        # Tabla con superficies
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
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DDDDDD')),
            ('GRID', (0, 0), (-1, -1), 0.4, colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ]))

        w, h = tabla.wrapOn(c, 0, 0)
        tabla.drawOn(c, margen, y - h)
        y -= h + 10

        # Estimación
        total = espacio['superficie_total'] * precio_m2
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margen + 10, y, f"💰 Estimación: {espacio['superficie_total']:.2f} m² x ${precio_m2:.2f} = ${total:,.2f}")
        y -= 35

    # 🖋️ Pie de página
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawCentredString(ancho / 2, 40, "Presupuesto generado por CG Pintores · Gracias por confiar en nosotros 🖌️")
    c.setFillColor(colors.black)
    c.save()

    print(f"\n📄 Presupuesto guardado como '{archivo}'")

# 🧱 INICIO DEL PROGRAMA
print("🎉 Bienvenido a CG Pintores – Generador de Presupuestos 🖌️")

cliente = input("👤 Nombre del cliente: ")
direccion = input("🏠 Domicilio: ")
contacto = input("📞 Teléfono o email: ")

while True:
    try:
        precio_m2 = float(input("💰 Precio por metro cuadrado ($): "))
        break
    except ValueError:
        print("❌ Por favor ingresá un valor numérico válido.")

seguir = True
while seguir:
    calcular_superficie()
    seguir = preguntar_si("➕ ¿Agregar otro ambiente?")

print("\n📦 Resumen:")
for espacio in espacios:
    print(f"🔸 {espacio['nombre']}: {espacio['superficie_total']:.2f} m²")

numero = obtener_numero_presupuesto()
exportar_presupuesto_a_pdf(espacios, cliente, contacto, direccion, precio_m2, numero)