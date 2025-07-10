def preguntar_si(texto):
    respuesta = input(texto + ' (s/n): ').strip().lower()
    return respuesta == 's'

def calcular_superficie():
    nombre = input("Nombre del espacio: ")
    largo = float(input("Largo (en metros): "))
    ancho = float(input("Ancho (en metros): "))
    alto = float(input("Alto (en metros): "))

    superficie_total = 0

    if preguntar_si("¿Querés pintar las 4 paredes?"):
        superficie_total += 2 * largo * alto + 2 * ancho * alto
    elif preguntar_si("¿Querés pintar solo una pared?"):
        superficie_total += float(input("Ancho (en metros) de esa pared: ")) * float(input("Alto (en metros) de esa pared: "))

    if preguntar_si("¿Querés pintar el techo?"):
        superficie_total += largo * ancho

    if preguntar_si("¿Querés pintar el piso?"):
        superficie_total += largo * ancho

    print(f'\n>> {nombre} – Superficie total a pintar: {superficie_total:.2f} m²')

# Programa principal
seguir = True
while seguir:
    calcular_superficie()
    seguir = preguntar_si("\n¿Querés agregar otro espacio?")
