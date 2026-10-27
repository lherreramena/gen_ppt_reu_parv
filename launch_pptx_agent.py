import os
from dotenv import load_dotenv

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Verificar que la clave exista antes de arrancar
if not os.getenv("OPENAI_API_KEY"):
    print("❌ Error: No se encontró la variable OPENAI_API_KEY en el archivo .env")
    exit(1)

print("✅ OPENAI_API_KEY cargada correctamente desde el archivo .env\n")

# 3. Importar y ejecutar el script principal de especificaciones
if __name__ == "__main__":
    import pptx_agent
    # Llamar a pptx_agent.main con argumentos
