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
    
    # Define aquí los argumentos que le pasarías por la línea de comandos
    # Por ejemplo: --template presentacion.pptx --changes instrucciones.txt --output resultado.pptx
    args = [
        "--template", "assets/template/template.pptx",
        "--changes", "assets/sources/instrucciones.txt",
        "--output", "assets/output/runion_pk.pptx"
    ]
    
    # Llamar a pptx_agent.main con los argumentos simulados
    exit_code = pptx_agent.main(args)
    exit(exit_code)