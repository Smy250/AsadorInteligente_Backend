from google import genai
import os
from dotenv import load_dotenv

# 0. Cargamos la API KEY desde las variables de entorno.
load_dotenv()
G_API_KEY = os.getenv("GEMINI_API_KEY")

# 1. Configuración del Cliente Moderno
client = genai.Client(api_key=G_API_KEY)

# 2. Definición del Modelo y Reglas del Agente
MODEL_ID = "gemini-flash-lite-latest"
sys_instruct = """Eres un agente en fase de pruebas. Primeramente estaremos probando la api 
 hasta especializarte en una tarea."""

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
    mensaje_completo = f"CONTEXTO DB: {datos_db}\n\nUSUARIO: {prompt_usuario}"
    
    try:
        response = ai_chat.send_message(mensaje_completo)
        return response.text
    except Exception as e:
        return f"Error en la nueva API: {e}"

# --- Ejemplo de flujo con memoria ---
# Turno 1: Le pasas datos
#print(consulta_agente_pro("", "Hola, ¿Todo correcto?"))