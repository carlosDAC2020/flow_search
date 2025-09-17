import asyncio
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

# --- Tu configuración se mantiene igual ---
print("✅ Modelo y componentes inicializados.")
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key=settings.GEMINI_API_KEY,
    temperature=0
)

prompt = ChatPromptTemplate.from_template("tell me a joke about {topic}")
parser = StrOutputParser()
chain = prompt | model | parser

async def main():
    """
    Función asíncrona principal para ejecutar la cadena y mostrar los eventos de forma legible.
    """
    print("\n▶️  INICIANDO EJECUCIÓN DE LA CADENA...\n")
    
    try:
        # Usamos un bucle para iterar sobre cada evento de la transmisión
        async for event in chain.astream_events({"topic": "parrot"}, version="v1"):
            kind = event["event"]
            name = event.get("name", "unnamed") # Obtenemos el nombre del componente

            # Filtramos y formateamos la salida según el tipo de evento
            if kind == "on_prompt_end":
                # Mostramos el prompt ya formateado que se le enviará al modelo
                formatted_prompt = event['data']['output'].to_string()
                print("📝 [Paso 1: Prompt] Plantilla procesada.")
                print(f'   Texto enviado al modelo: "{formatted_prompt}"\n')

            elif kind == "on_chat_model_start":
                print(f"🧠 [Paso 2: Modelo] Esperando respuesta de '{name}'...")
                print("   Respuesta en streaming:")

            elif kind == "on_chat_model_stream":
                # Imprimimos cada trozo de texto a medida que llega
                chunk_content = event['data']['chunk'].content
                if chunk_content:
                    print(chunk_content, end="", flush=True)
            
            elif kind == "on_parser_end":
                # El parser ha terminado de convertir la respuesta a texto
                print(f"\n\n✂️  [Paso 3: Parser] '{name}' ha convertido la salida a texto.\n")

            elif kind == "on_chain_end":
                # La cadena completa ha finalizado
                final_output = event['data']['output']
                print("🏁 FIN DE LA EJECUCIÓN.")
                print(f'   Resultado final: "{final_output.strip()}"')

    except Exception as e:
        print(f"\nHa ocurrido un error: {e}")

# --- Ejecución del código ---
if __name__ == "__main__":
    asyncio.run(main())