import logging
from utils.model import ModelSelector
from strands import Agent
import asyncio

logging.getLogger("strands").setLevel(logging.INFO)

logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

model = ModelSelector('Sonnet3.7').get_model()

# Instrucciones para el agente estudiante
CloudStudent_Instructions = """
Eres Alex, un estudiante entusiasta de ciencias de la computación que está aprendiendo sobre computación en la nube.
Tu personalidad y comportamiento:
    • Eres curioso y haces preguntas reflexivas sobre conceptos de computación en la nube
    • Muestras gran interés por las plataformas AWS, Azure y Google Cloud
    • Formulas preguntas de seguimiento basadas en las respuestas del profesor
    • Mantienes las preguntas enfocadas y con fines educativos
    • SIEMPRE terminas cada mensaje con una pregunta específica
    • Construyes sobre las respuestas anteriores del profesor
    • Después de 4-5 intercambios, agradeces al profesor y preguntas por recursos adicionales

IMPORTANTE: 
- Responde SOLO como Alex el estudiante
- NO actúes como el profesor
- Mantén un tono respetuoso pero entusiasta
- Haz UNA pregunta específica por mensaje
"""

# Instrucciones para el agente profesor
CloudProfessor_Instructions = """
Eres la Dr. María González, una profesora experimentada en computación en la nube con 15 años de experiencia en AWS, Azure y Google Cloud.
Tu personalidad y comportamiento:
    • Brindas explicaciones claras y educativas sobre conceptos de computación en la nube
    • Usas ejemplos del mundo real y analogías para explicar conceptos complejos
    • Fomentas el aprendizaje continuo y la exploración
    • Respondes preguntas de forma académica pero accesible
    • Mantienes las respuestas concisas pero informativas (máximo 2-3 párrafos)
    • Guías la conversación hacia aplicaciones prácticas de la computación en la nube
    • Ocasionalmente haces preguntas al estudiante para verificar comprensión

IMPORTANTE:
- Responde SOLO como la Dr. González
- NO actúes como el estudiante
- Sé paciente y didáctica
- Proporciona ejemplos concretos cuando sea posible
"""

# Crear los agentes
cloud_student = Agent(
    system_prompt=CloudStudent_Instructions,
    model=model
)

cloud_professor = Agent(
    system_prompt=CloudProfessor_Instructions,
    model=model
)

class CloudConversationManager:
    def __init__(self, student_agent, professor_agent):
        self.student = student_agent
        self.professor = professor_agent
        self.conversation_history = []
        self.turn_count = 0
        self.max_turns = 4
        
    def should_end_conversation(self, message):
        end_keywords = [
            "gracias por todo", "muchas gracias", "ha sido muy útil",
            "recursos adicionales", "seguir aprendiendo", "esto es todo",
            "terminar", "concluir", "despedida", "excelente explicación"
        ]
        return any(keyword in message.lower() for keyword in end_keywords)
    
    async def run_conversation(self):
        print("🎓 === Sesión de Tutoría: Computación en la Nube ===")
        print("👨‍🏫 Dr. María González (Profesora) ↔️ 🎓 Pedro (Estudiante)")
        print("=" * 70)
        
        # El estudiante inicia la conversación
        current_speaker = "student"
        
        # Mensaje inicial del estudiante
        print("🎓 Pedro está iniciando la conversación...")
        initial_question = await self.get_agent_response(
            self.student, 
            "Inicia una conversación preguntando sobre computación en la nube. Haz una pregunta específica para comenzar."
        )
        
        print(f"🎓 Pedro: {initial_question}")
        print("-" * 70)
        
        self.conversation_history.append(f"Estudiante: {initial_question}")
        current_speaker = "professor"
        self.turn_count += 1
        
        # Continuar la conversación
        while self.turn_count < self.max_turns:
            
            if current_speaker == "professor":
                # Turno del profesor
                context = "\n".join(self.conversation_history[-4:])  # Últimos 4 mensajes para contexto
                prompt = f"Contexto de la conversación:\n{context}\n\nResponde como profesora a la última pregunta del estudiante."
                
                response = await self.get_agent_response(self.professor, prompt)
                print(f"👨‍🏫 Dr. González: {response}")
                
                self.conversation_history.append(f"Profesora: {response}")
                current_speaker = "student"
                
            else:
                # Turno del estudiante
                context = "\n".join(self.conversation_history[-4:])  # Últimos 4 mensajes para contexto
                prompt = f"Contexto de la conversación:\n{context}\n\nResponde como estudiante a la explicación del profesor y haz una nueva pregunta."
                
                response = await self.get_agent_response(self.student, prompt)
                print(f"🎓 Alex: {response}")
                
                self.conversation_history.append(f"Estudiante: {response}")
                current_speaker = "professor"
                
                # Verificar si el estudiante quiere terminar
                if self.should_end_conversation(response):
                    print("\n🎯 Alex está listo para concluir la sesión...")
                    # Respuesta final del profesor
                    final_context = "\n".join(self.conversation_history[-3:])
                    final_prompt = f"Contexto:\n{final_context}\n\nDa una respuesta final como profesora, incluyendo recursos adicionales para que el estudiante siga aprendiendo."
                    
                    final_response = await self.get_agent_response(self.professor, final_prompt)
                    print(f"👨‍🏫 Dr. González: {final_response}")
                    break
            
            print("-" * 70)
            self.turn_count += 1
            
            # Pausa para evitar rate limiting
            await asyncio.sleep(1)
        
        if self.turn_count >= self.max_turns:
            print(f"\n⏰ Sesión completada después de {self.turn_count} intercambios.")
        
        print(f"\n📊 Resumen de la sesión:")
        print(f"   • Total de intercambios: {len(self.conversation_history)}")
        print(f"   • Tema: Computación en la nube")
        print(f"   • Participantes: Alex (Estudiante) y Dr. González (Profesora)")
    
    async def get_agent_response(self, agent, prompt):
        """Obtiene respuesta de un agente específico"""
        try:
            # Llamar al agente y manejar el resultado correctamente
            result = agent(prompt)
            
            # Diferentes formas de acceder al contenido según la estructura de AgentResult
            if hasattr(result, 'content'):
                return str(result.content).strip()
            elif hasattr(result, 'text'):
                return str(result.text).strip()
            elif hasattr(result, 'message'):
                return str(result.message).strip()
            elif hasattr(result, 'response'):
                return str(result.response).strip()
            else:
                # Si no encontramos el atributo correcto, convertir a string
                return str(result).strip()
                
        except Exception as e:
            print(f"Debug - Error details: {e}")
            print(f"Debug - Result type: {type(result) if 'result' in locals() else 'No result'}")
            print(f"Debug - Result attributes: {dir(result) if 'result' in locals() else 'No result'}")
            return f"Error al obtener respuesta: {e}"

async def start_cloud_conversation():
    """Inicia la conversación entre los agentes"""
    print("🚀 Iniciando Sistema de Tutoría Inteligente")
    print("   Tema: Computación en la Nube")
    print()
    
    try:
        conversation_manager = CloudConversationManager(cloud_student, cloud_professor)
        await conversation_manager.run_conversation()
        print("\n✅ Sesión de tutoría finalizada exitosamente")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Sesión interrumpida por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante la sesión: {e}")
        print("\n🔧 Verificar la configuración del modelo y conexión")

def main():
    """Función principal que ejecuta la conversación"""
    print("\n=== CloudCamp: Tutoría Inteligente ===")
    print("Conversación entre Agentes de IA sobre Computación en la Nube")
    print("Presiona Ctrl+C para interrumpir en cualquier momento\n")
    
    # Ejecutar la conversación asíncrona
    asyncio.run(start_cloud_conversation())

# Verificar si el script se ejecuta directamente
if __name__ == "__main__":
    main()