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

    # Usamos un contexto SSL no verificado para manejar certificados autofirmados/antiguos,
    # común en entornos de prueba o locales. En producción, esto no es recomendable.
    ssl_context = ssl._create_unverified_context()

    try:
        # Configuración de la solicitud (HEAD es más rápido que GET)
        req = urllib.request.Request(url, method='HEAD')
        
        # Simula un navegador para evitar ser bloqueado
        req.add_header('User-Agent', 'Mozilla/5.0 (compatible; URLChecker/1.0)')

        # Abre la URL y espera la respuesta con un tiempo límite
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS, context=ssl_context) as response:
            return response.getcode() # Devuelve el código de estado (e.g., 200)

    except urllib.error.HTTPError as e:
        return e.code  # Devuelve códigos de error HTTP (e.g., 404, 503)
    except urllib.error.URLError as e:
        # Esto captura fallos de DNS, timeouts (si el servidor no responde nada), etc.
        return 0  # Código 0 para fallos de red/conexión
    except Exception as e:
        # Captura otros errores inesperados
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

def main():
    """Función principal del script."""
    try:
        with open(URL_FILE, 'r') as f:
            urls = f.readlines()
    except FileNotFoundError:
        print(f"Error: El archivo de listado '{URL_FILE}' no se encontró.")
        print(f"Crea un archivo llamado '{URL_FILE}' con una URL por línea.")
        sys.exit(1)

    print("--- Iniciando verificación de sitios web (Python) ---")
    print(f"URLs a verificar en: {URL_FILE}")
    print("-----------------------------------------------------")

    for line in urls:
        # Limpia espacios y caracteres de nueva línea
        url = line.strip()

        # Omite líneas vacías o comentarios (que comienzan con #)
        if not url or url.startswith('#'):
            continue
        
        # Muestra la URL que se está verificando
        print(f"Verificando {url}...", end=" ")

        # Realiza la verificación y clasificación
        code = verificar_url(url)
        resultado = clasificar_codigo(code)

        print(resultado)

    print("-----------------------------------------------------")
    print("Verificación finalizada.")

if __name__ == "__main__":
    main()