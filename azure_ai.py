# Este programa crea dos agentes (un estudiante y un profesor) que conversan sobre computación en la nube usando Azure AI Foundry.

from azure.identity import DefaultAzureCredential  # Para autenticarse con Azure
from semantic_kernel.agents import AzureAIAgent, AgentGroupChat  # Para crear agentes y chats grupales
import os
import asyncio
from dotenv import load_dotenv  # Para cargar variables del archivo .env
from semantic_kernel.agents.strategies import TerminationStrategy, SequentialSelectionStrategy  # Estrategias para controlar la conversación

# Instrucciones para el agente estudiante
CloudStudent_Instructions = """
Eres un estudiante entusiasta de ciencias de la computación que está aprendiendo sobre computación en la nube.
Tu rol es:
    •	Hacer preguntas reflexivas sobre conceptos de computación en la nube.
    •	Mostrar curiosidad sobre las plataformas AWS, Azure y Google Cloud.
    •	Formular preguntas de seguimiento basadas en las respuestas del profesor.
    •	Mantener las preguntas enfocadas y con fines educativos.
    •	Terminar cada uno de tus mensajes con una pregunta específica.
    •	Después de 5 intercambios, agradecer al profesor y concluir la sesión.
"""

# Instrucciones para el agente profesor
CloudProfessor_Instructions = """
Eres un profesor experimentado en computación en la nube con experiencia en AWS, Azure y Google Cloud.
Tu rol es:
    •	Brindar explicaciones claras y educativas sobre conceptos de computación en la nube.
    •	Usar ejemplos del mundo real y analogías.
    •	Fomentar el aprendizaje continuo y la exploración.
    •	Responder preguntas de forma académica pero accesible.
    •	Mantener las respuestas concisas pero informativas (máximo 2 párrafos).
    •	Guiar la conversación hacia aplicaciones prácticas de la computación en la nube.
"""

# Estrategia para terminar la conversación automáticamente
class ApprovalTerminationStrategy(TerminationStrategy):
    def __init__(self, agents, maximum_iterations=10, automatic_reset=True):
        super().__init__()
        self.agents = agents
        self.maximum_iterations = maximum_iterations  # Número máximo de turnos
        self.automatic_reset = automatic_reset
        self._iteration = 0
        self._terminated = False

    # Esta función decide si la conversación debe terminar
    async def should_terminate(self, history, messages):
        self._iteration += 1
        # Si se llega al máximo de turnos, termina
        if self._iteration >= self.maximum_iterations:
            self._terminated = True
            return True
        # Si algún mensaje contiene "APROBADO" o "FIN", termina
        for msg in messages:
            if "APROBADO" in msg.content.upper() or "FIN" in msg.content.upper():
                self._terminated = True
                return True
        return False

    # Reinicia el contador si se necesita
    def reset(self):
        if self.automatic_reset:
            self._iteration = 0
            self._terminated = False

# Función principal del programa
async def main():
    load_dotenv()  # Carga las variables del archivo .env
    
    # Lee el endpoint y el deployment del archivo .env
    endpoint = os.getenv("AZURE_AI_AGENT_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    
    # Si faltan datos, muestra un error y termina
    if not endpoint or not deployment:
        print("Error: AZURE_AI_AGENT_ENDPOINT y AZURE_OPENAI_DEPLOYMENT deben estar configurados en el archivo .env")
        return
    
    print(f"Usando endpoint: {endpoint}")
    print(f"Usando deployment: {deployment}")

    # Crea la credencial para Azure
    creds = DefaultAzureCredential()

    try:
        # Crea el cliente para los agentes
        async with AzureAIAgent.create_client(
            endpoint=endpoint,
            credential=creds
        ) as client:

            # Crea el agente estudiante
            student_def = await client.agents.create_agent(
                model=deployment,
                name="CloudStudent",
                instructions=CloudStudent_Instructions
            )

            # Crea el agente profesor
            professor_def = await client.agents.create_agent(
                model=deployment,
                name="CloudProfessor",
                instructions=CloudProfessor_Instructions,
            )

            # Instancia los agentes
            student_agent = AzureAIAgent(client=client, definition=student_def)
            professor_agent = AzureAIAgent(client=client, definition=professor_def)

            # Crea el chat grupal con ambos agentes y la estrategia de terminación
            group_chat = AgentGroupChat(
                agents=[student_agent, professor_agent],
                termination_strategy=ApprovalTerminationStrategy(
                    agents=[student_agent, professor_agent],
                    maximum_iterations=10,
                    automatic_reset=True
                )                                                                 
            )

            # Inicia la conversación y muestra cada respuesta
            async for response in group_chat.invoke():
                print("Respuesta:", response.content)

    except Exception as e:
        print(f"Error: {e}")
        print("\nVerificar:")
        print("1. El endpoint de Azure AI Foundry es correcto")
        print("2. El deployment del modelo existe y está activo")

# Hace que el programa se ejecute si se llama desde la terminal
if __name__ == "__main__":
    asyncio.run(main())

    