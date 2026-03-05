from google import genai
import os
from dotenv import load_dotenv

# 0. Cargamos la API KEY desde las variables de entorno.
load_dotenv()
G_API_KEY = os.getenv("GEMINI_API_KEY")

# 1. Configuración del Cliente Moderno
client = genai.Client(api_key=G_API_KEY)

# 2. Definición del Modelo y Reglas del Agente
MODEL_ID = "gemini-3.1-flash-lite-preview"
sys_instruct = """Eres un agente experto analista y administrativo de ventas de la organización AsadorInteligente. 
Tu misión es analizar los datos reales del negocio y dar consejos estrategicos.
Responde de forma breve y profesional basándote únicamente en los datos que te seran proporcionados. Si el usuario pregunta algo que no tiene nada que ver con lo que te he descrito anteriormente, pidele una pregunta mas especifica relacionada al negocio."""

# 3. Iniciamos el chat (la memoria vive aquí)
# El historial ahora usa una estructura más intuitiva
chat = client.chats.create(
    model=MODEL_ID,
    config={'system_instruction': sys_instruct}
)

def consulta_agente_pro(datos_db: str, prompt_usuario: str, ai_chat: genai.client.Chats):
    """
    Envía la información de tu DB y la consulta.
    El historial se guarda automáticamente en el objeto 'chat'.
    """
    mensaje_completo = f"CONTEXTO DB AsadorInteligente: {datos_db}\n\nUSUARIO: {prompt_usuario}"
    
    try:
        response = ai_chat.send_message(mensaje_completo)
        return response.text
    except Exception as e:
        return f"Error en la nueva API: {e}"

# --- Ejemplo de flujo con memoria ---
# Turno 1: Le pasas datos
#print(consulta_agente_pro("", "Hola, ¿Todo correcto?"))