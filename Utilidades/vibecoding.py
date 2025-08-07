import re
import csv

def limpiar_texto(t):
    t = t.replace("/", " ")
    t = re.sub(r'\s+', ' ', t)
    return t.strip()

def extraer_datos_bloque_por_bloque(texto):
    bloques = re.split(r'\n\s*\n', texto.strip())
    registros = []
    ignorados = []

    for idx, bloque in enumerate(bloques):
        bloque_limpio = limpiar_texto(bloque)

        nombre_match = re.search(
            r'^[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+\s+[A-ZÁÉÍÓÚÑa-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑa-záéíóúñ]+)?',
            bloque_limpio
        )
        afiliado_match = re.search(r'\b\d{12}\b', bloque_limpio)
        dni_match = re.search(r'\bdni[:\s]*?(\d{7,8})\b', bloque_limpio, re.IGNORECASE)
        altura_match = re.search(r'(\d,\d)\s*m', bloque_limpio)
        peso_match = re.search(r'(\d{2,3})\s*kg', bloque_limpio, re.IGNORECASE)
        edad_match = re.search(r'(\d{1,3})\s*años', bloque_limpio, re.IGNORECASE)

        if all([nombre_match, afiliado_match, dni_match, altura_match, peso_match, edad_match]):
            altura_metros = altura_match.group(1).replace(",", ".")
            altura_cm = int(float(altura_metros) * 100)

            dni = dni_match.group(1).zfill(8)

            registros.append({
                "nombre": nombre_match.group(0).strip(),
                "afiliado": afiliado_match.group(0),
                "documento": dni,
                "altura": str(altura_cm),  # en centímetros
                "peso": peso_match.group(1),
                "edad": edad_match.group(1)
            })
        else:
            ignorados.append((idx + 1, bloque.strip()))

    return registros, ignorados

def main():
    archivo_entrada = "archivo.txt"

    with open(archivo_entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    datos, ignorados = extraer_datos_bloque_por_bloque(texto)

    total_bloques = len(datos) + len(ignorados)
    print(f"\n🔍 Total de bloques procesados: {total_bloques}")
    print(f"✅ Registros válidos: {len(datos)}")
    print(f"❌ Registros ignorados: {len(ignorados)}")

    for i, persona in enumerate(datos, 1):
        print(f"\nPersona {i}:")
        for campo, valor in persona.items():
            print(f"  {campo}: {valor}")

    with open("personas.csv", "w", newline="", encoding="utf-8") as f:
        campos = ["nombre", "documento", "afiliado", "altura", "peso", "edad"]
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)

    print("\n✅ Datos guardados en personas.csv")

    if ignorados:
        print("\n⚠️ Registros ignorados (faltan datos):")
        for idx, bloque in ignorados:
            print(f"\nBloque {idx}:")
            print(bloque[:150] + ("..." if len(bloque) > 150 else ""))

if __name__ == "__main__":
    main()
