#!/bin/bash

# Nombre del archivo que contiene el listado de URLs (una por línea)
URL_FILE="urls.txt"

# Verifica si el archivo de URLs existe
if [ ! -f "$URL_FILE" ]; then
    echo "Error: El archivo de listado '$URL_FILE' no se encontró."
    echo "Crea un archivo llamado '$URL_FILE' con una URL por línea."
    exit 1
fi

echo "--- Iniciando verificación de sitios web ---"
echo "URLs a verificar en: $URL_FILE"
echo "-------------------------------------------"

# Lee el archivo línea por línea
while IFS= read -r url
do
    # Limpia posibles espacios en blanco (xargs es útil para esto)
    url=$(echo "$url" | xargs)

    # Omite líneas vacías o comentarios (usa grep para una simple verificación de comentario)
    if [ -z "$url" ] || echo "$url" | grep -q "^#"; then
        continue
    fi

    # Muestra la URL que se está verificando
    echo -n "Verificando $url... "

    # Usa curl para obtener el código de estado HTTP
    # -s: Modo silencioso
    # -o /dev/null: Descarta el cuerpo de la respuesta
    # -w "%{http_code}\n": Imprime solo el código de estado HTTP
    # --max-time 5: Tiempo máximo de espera de 5 segundos
    http_code=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url")

    # Comprueba el código de estado con sintaxis simple [ ... ]
    # Un código 200 a 399 indica éxito o redirección (ACTIVO)
# Comprueba el código de estado
    if [ "$http_code" -ge 200 ] && [ "$http_code" -lt 400 ]; then
        echo "✅ ACTIVO (Código: $http_code)"
    elif [ "$http_code" -ge 500 ] && [ "$http_code" -lt 600 ]; then
        echo "⚠️ ERROR DE SERVIDOR (Código: $http_code - Temporal)"
    elif [ "$http_code" -ge 400 ] && [ "$http_code" -lt 500 ]; then
        echo "🛑 ERROR DE CLIENTE (Código: $http_code - Ejemplo: 404 No encontrado)"
    else
        # Captura códigos 000 (tiempo agotado o fallo de red) y otros no cubiertos
        echo "❌ FALLO DE CONEXIÓN O RESPUESTA (Código: $http_code)"
    fi

done < "$URL_FILE"

echo "-------------------------------------------"
echo "Verificación finalizada."