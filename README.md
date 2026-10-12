# JARVIS Dev Agent

Un agente local de desarrollo para acompañarte en la creación, revisión y mejora de proyectos de ingeniería.

## Qué incluye

- Asistente tipo JARVIS con contexto del proyecto
- Lectura y análisis de archivos
- Listado de estructura del repositorio
- Ejecución segura de comandos del sistema
- Integración con Ollama
- Endpoints REST para uso local o desde una UI
- Soporte para modos: architect, debugger, devops, qa, reviewer

## Estructura

```text
.
├── app/
│   ├── __init__.py
│   ├── agent.py
│   ├── config.py
│   ├── main.py
│   └── tools.py
├── .env.example
├── README.md
├── requirements.txt
├── start.sh
└── tests/
    └── test_smoke.py
```

## Requisitos

- Python 3.11+
- Ollama instalado y corriendo localmente
- Un modelo descargado en Ollama, por ejemplo: `llama3.1`, `qwen2.5`, `mistral`

## Instalación

```bash
git clone https://github.com/rigobertodz97-tech/jarvis-dev-agent.git
cd jarvis-dev-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Ejecutar Ollama

```bash
ollama run llama3.1
```

## Arranque

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O usando el script:

```bash
bash start.sh
```

## Uso de la API

### Health check

```bash
curl http://localhost:8000/
```

### Enviar tarea

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Revisa este proyecto y dime cómo mejorar la arquitectura backend y la calidad del código.",
    "project_path": ".",
    "mode": "architect"
  }'
```

## Modos disponibles

- `architect`: diseño y arquitectura
- `debugger`: resolución de errores
- `devops`: despliegue, CI/CD y entorno
- `qa`: revisión de calidad y pruebas
- `reviewer`: análisis de código y recomendaciones

## Variables de entorno

```env
MODEL_NAME=llama3.1
OLLAMA_URL=http://localhost:11434
APP_PORT=8000
ALLOW_COMMANDS=true
```

## Seguridad

Este agente ejecuta comandos del sistema. Solo actívalo en proyectos de confianza y con permisos adecuados.

## Siguiente paso recomendado

Puedes conectarlo a una interfaz web, a GitHub, o a un agente de análisis de repo con memoria persistente.

---

Proyecto base para un JARVIS de ingeniería de software funcionando localmente en tu máquina.
