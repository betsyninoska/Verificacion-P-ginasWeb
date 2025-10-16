import urllib.request
import urllib.error
import ssl
import sys

# Nombre del archivo que contiene el listado de URLs (una por línea)
URL_FILE = "urls.txt"
TIMEOUT_SECONDS = 5

def verificar_url(url):
    """Verifica si una URL está activa y devuelve el código de estado."""
    # Agrega el esquema 'https://' si falta, para evitar errores de urllib
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    # Usamos un contexto SSL no verificado (opcional, para entornos difíciles)
    ssl_context = ssl._create_unverified_context()

    try:
        # Configuración de la solicitud (HEAD es más rápido que GET)
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; URLChecker/1.0)')

        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS, context=ssl_context) as response:
            return response.getcode()

    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return 0
    except Exception as e:
        return -1

def clasificar_codigo(code):
    """Clasifica el código de estado para una salida legible."""
    if 200 <= code < 400:
        return f"✅ ACTIVO (Código: {code})"
    elif 400 <= code < 500:
        return f"🛑 ERROR CLIENTE (Código: {code} - Ej: 404 No encontrado)"
    elif 500 <= code < 600:
        return f"⚠️ ERROR SERVIDOR (Código: {code} - Ej: 503 Temporal)"
    elif code == 0:
        return "❌ FALLO CONEXIÓN (DNS, TimeOut o No Responde)"
    else:
        return f"❓ FALLO DESCONOCIDO (Código: {code})"

def generar_reporte():
    """Lee las URLs y genera el reporte completo como una cadena de texto."""
    reporte = []
    
    try:
        with open(URL_FILE, 'r') as f:
            urls = f.readlines()
    except FileNotFoundError:
        return f"Error: El archivo de listado '{URL_FILE}' no se encontró."

    reporte.append("--- Iniciando verificación de sitios web (Python) ---")
    reporte.append(f"URLs a verificar en: {URL_FILE}")
    reporte.append("-----------------------------------------------------")

    for line in urls:
        url = line.strip()

        if not url or url.startswith('#'):
            continue
        
        # Simula la impresión en una sola línea y añade el resultado
        code = verificar_url(url)
        resultado = clasificar_codigo(code)
        reporte.append(f"Verificando {url}... {resultado}")

    reporte.append("-----------------------------------------------------")
    reporte.append("Verificación finalizada.")
    
    return "\n".join(reporte) # Devuelve todo el reporte como una única cadena

def main():
    # La función main simplemente imprime el reporte completo.
    # Esto asegura que GitHub Actions pueda capturarlo completamente.
    print(generar_reporte())

if __name__ == "__main__":
    main()