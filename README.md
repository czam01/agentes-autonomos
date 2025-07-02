# 🤖 Agentes Autónomos - CloudCamp

Repositorio de proyectos de agentes conversacionales de IA para educación en computación en la nube, desarrollados por CloudCamp.

## 📋 Descripción General

Este repositorio contiene dos implementaciones diferentes de sistemas de tutoría inteligente que simulan conversaciones entre estudiantes y profesores sobre computación en la nube:

1. **Azure AI Foundry**: Implementación usando Azure AI Foundry y Semantic Kernel
2. **AWS Strand Agents**: Implementación usando Strands AI Framework

Ambos proyectos demuestran cómo crear agentes conversacionales que mantienen contexto y proporcionan experiencias educativas interactivas.


## 🚀 Proyectos

### 1. 🔵 Azure AI Foundry

**Tecnologías**: Azure AI Foundry, Semantic Kernel, Python

Sistema de conversación que utiliza Azure AI Foundry para crear agentes que conversan sobre computación en la nube.

#### Características:
- ✅ Agentes CloudStudent y CloudProfessor
- ✅ Integración con Azure OpenAI
- ✅ Estrategia de terminación automática
- ✅ Gestión de credenciales con DefaultAzureCredential
- ✅ Chat grupal con Semantic Kernel

```mermaid
graph TB
    subgraph "🌐 Azure Cloud"
        subgraph "🤖 Azure AI Foundry"
            AAF[Azure AI Agent Service]
            AOI[Azure OpenAI Service]
            DEP[GPT-4 Deployment]
        end
        
        subgraph "🔐 Azure Identity"
            DAC[DefaultAzureCredential]
            AAD[Azure Active Directory]
        end
    end
    
    subgraph "💻 Local Application"
        subgraph "🎭 Agent Definitions"
            CS_DEF[CloudStudent Definition]
            CP_DEF[CloudProfessor Definition]
        end
        
        subgraph "🎪 Agent Instances"
            CS[🎓 CloudStudent Agent<br/>Alex]
            CP[👨‍🏫 CloudProfessor Agent<br/>Dr. González]
        end
        
        subgraph "🎛️ Orchestration Layer"
            AGC[AgentGroupChat]
            ATS[ApprovalTerminationStrategy]
            SSS[SequentialSelectionStrategy]
        end
        
        subgraph "⚙️ Configuration"
            ENV[.env Variables]
            CREDS[Azure Credentials]
        end
    end
    
    subgraph "🔄 Conversation Flow"
        INIT[Initialize Chat]
        CONV[Conversation Loop]
        TERM[Termination Check]
        END[End Session]
    end
    
    %% Connections
    ENV --> CREDS
    CREDS --> DAC
    DAC --> AAD
    AAD --> AAF
    
    CS_DEF --> AAF
    CP_DEF --> AAF
    AAF --> CS
    AAF --> CP
    
    CS --> AGC
    CP --> AGC
    AGC --> ATS
    AGC --> SSS
    
    AAF --> AOI
    AOI --> DEP
    
    AGC --> INIT
    INIT --> CONV
    CONV --> TERM
    TERM --> CONV
    TERM --> END
    
    %% Styling
    classDef azure fill:#0078d4,stroke:#005a9e,stroke-width:2px,color:#fff
    classDef agent fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    classDef orchestration fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    classDef config fill:#e8f5e8,stroke:#388e3c,stroke-width:2px
    classDef flow fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class AAF,AOI,DEP,DAC,AAD azure
    class CS,CP,CS_DEF,CP_DEF agent
    class AGC,ATS,SSS orchestration
    class ENV,CREDS config
    class INIT,CONV,TERM,END flow
```

### 2. 🟠 AWS Strand Agents

**Tecnologías**: Strands AI Framework, Python, ModelSelector

Sistema avanzado de tutoría con múltiples agentes especializados y herramientas.

#### Características:
- ✅ Sistema de orquestación con múltiples herramientas
- ✅ Agentes especializados (Support, DevOps, SAA Simulator, Laboratory)
- ✅ Conversación entre CloudStudent y CloudProfessor
- ✅ Manejo robusto de errores con SafeAgent
- ✅ Cleanup automático de recursos
- ✅ Interfaz visual mejorada

```mermaid
graph LR
    subgraph "🏗️ Sistema de Tutoría Inteligente"
        subgraph "🎭 Agentes"
            A1[🎓 CloudStudent<br/>Alex]
            A2[👨‍🏫 CloudProfessor<br/>Dr. González]
        end
        
        subgraph "🎛️ Gestión"
            CM[ConversationManager]
            SA1[SafeAgent Wrapper]
            SA2[SafeAgent Wrapper]
        end
        
        subgraph "🧠 Modelo IA"
            MS[ModelSelector<br/>Sonnet3.7]
            API[API Endpoint]
        end
        
        subgraph "💾 Datos"
            CH[Conversation History]
            CTX[Context Buffer]
        end
    end
    
    A1 -.-> SA1
    A2 -.-> SA2
    SA1 --> CM
    SA2 --> CM
    CM --> CH
    CM --> CTX
    SA1 --> MS
    SA2 --> MS
    MS --> API
    
    style A1 fill:#e3f2fd
    style A2 fill:#f3e5f5
    style CM fill:#fff3e0
    style MS fill:#e8f5e8
```
