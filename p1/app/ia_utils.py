import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Análisis de casos legales con IA, se incluye la complejidad, ajuste de precio, servicios adicionales y propuesta profesional, 
# así como el formato JSON requerido, y una recomendación de ajuste de precio en porcentaje (0%, 25% o 50%).
def analizar_con_ia(descripcion, tipo_servicio):
    prompt = f"""
Analiza este caso legal: {descripcion}
Tipo de servicio: {tipo_servicio}

Evalúa:
1. Complejidad (Baja, Media o Alta)
2. Ajuste de precio recomendado (0%, 25% o 50%)
3. Servicios adicionales necesarios
4. Genera propuesta profesional para cliente (2 a 3 párrafos)

Devuelve el resultado en formato JSON válido, con las claves:
- "complejidad"
- "ajuste_precio"
- "servicios_adicionales" (como lista)
- "propuesta_texto"

Ejemplo de estructura (no lo incluyas literalmente, solo sigue el formato):

{{
  "complejidad": "Media",
  "ajuste_precio": (recomendación de ajuste en porcentaje 0.0, 0.25 o 0.5), 
  "servicios_adicionales": ["Revisión de contratos"],
  "propuesta_texto": "Texto profesional generado por IA..."
}}

IMPORTANTE:
- Tu respuesta debe ser solo JSON.
- No escribas explicaciones ni texto antes o después.
- No uses ```json ni comillas triples.
"""

    #Conectamos con la API de OpenAI para obtener la respuesta, en este caso con el modelo gpt-4o-mini, por tema de coste y rapidez.
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        content = response.choices[0].message.content.strip()

        # Convertimos el contenido a JSON
        data = json.loads(content)
        return data

    except Exception as e:
        return {
            "error": "Ocurrió un error al procesar la solicitud con IA.",
            "detalle": str(e)
        }
