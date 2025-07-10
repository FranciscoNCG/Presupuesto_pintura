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

    # Guardamos los datos en la lista general
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

# --- Programa principal ---
print("🛠️ Bienvenido al Calculador de Superficies, versión personalizada 😎")
seguir = True
while seguir:
    calcular_superficie()
    seguir = preguntar_si("\n➕ ¿Querés agregar otro espacio?")

print("\n🧾 Resumen general de espacios ingresados:")
for espacio in espacios:
    print(f"🔸 {espacio['nombre']}: {espacio['superficie_total']:.2f} m² totales")

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def exportar_presupuesto_a_pdf(lista_espacios, archivo="presupuesto_final.pdf"):
    c.drawImage("logo.png", 450, y, width=100, preserveAspectRatio=True, mask='auto')
    c = canvas.Canvas(archivo, pagesize=A4)
    ancho, alto = A4
    y = alto - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "🧾 Presupuesto de Pintura")
    y -= 30
    c.setFont("Helvetica", 11)

    for espacio in lista_espacios:
        if y < 150:
            c.showPage()
            y = alto - 50
            c.setFont("Helvetica", 11)

        c.drawString(50, y, f"🔹 {espacio['nombre']}")
        y -= 20
        c.drawString(70, y, f"Dimensiones: {espacio['largo']} x {espacio['ancho']} x {espacio['alto']} m")
        y -= 20
        for i, sup in enumerate(espacio['paredes'], 1):
            c.drawString(90, y, f"Pared {i}: {sup:.2f} m²")
            y -= 15

        if espacio["techo"]:
            c.drawString(90, y, f"Techo: {espacio['techo']:.2f} m²")
            y -= 15
        if espacio["piso"]:
            c.drawString(90, y, f"Piso: {espacio['piso']:.2f} m²")
            y -= 15

        c.drawString(70, y, f"✅ Total: {espacio['superficie_total']:.2f} m²")
        y -= 30

    c.save()
    print(f"\n📄 Presupuesto guardado en '{archivo}'")

exportar_presupuesto_a_pdf(espacios)

