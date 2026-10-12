import json
import httpx

from app.config import MODEL_NAME, OLLAMA_URL


def ask_model(prompt: str, system_prompt: str | None = None) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }
    if system_prompt:
        payload["system"] = system_prompt

    response = httpx.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
    response.raise_for_status()
    result = response.json()
    return result.get("response", "Sin respuesta del modelo.")


def build_project_summary(project_path: str) -> str:
    from app.tools import list_project, git_status, search_text, read_file

    try:
        structure = list_project(project_path, max_depth=2)
        git_state = git_status(project_path)
        readme = ""
        readme_path = f"{project_path}/README.md"
        if __import__("pathlib").Path(readme_path).exists():
            readme = read_file(readme_path)[:2500]

        summary = f"""
Proyecto: {project_path}

Estructura:
{structure}

Git status:
{git_state}

README (resumen):
{readme}
"""
        return summary
    except Exception as exc:
        return f"Error generando resumen del proyecto: {exc}"


def generate_mode_system_prompt(mode: str) -> str:
    prompts = {
        "architect": "Eres un arquitecto senior de software. Analiza el proyecto, propone mejoras y recomendaciones de diseño con enfoque en escalabilidad, mantenibilidad y calidad.",
        "debugger": "Eres un ingeniero de debugging senior. Identifica errores, fallos de lógica, problemas de configuración, y da un plan de corrección paso a paso.",
        "devops": "Eres un ingeniero DevOps. Revisa entorno, despliegues, infraestructura, automatización y recomendaciones operativas.",
        "qa": "Eres un especialista en QA. Evalúa robustez, cobertura de pruebas, calidad del software y riesgos funcionales.",
        "reviewer": "Eres un reviewer senior. Haz una revisión técnica objetiva del código, riesgos y oportunidades de mejora.",
    }
    return prompts.get(mode, "Eres un asistente de ingeniería de software altamente útil y práctico.")


def build_task_prompt(task: str, project_path: str, mode: str) -> str:
    project_summary = build_project_summary(project_path)
    return f"""
Eres un agente tipo JARVIS para acompañar proyectos de ingeniería.
Modo: {mode}

Solicitud del usuario:
{task}

Contexto del proyecto:
{project_summary}

Instrucciones:
1. Haz un análisis técnico conciso pero útil.
2. Si falta contexto, pide lo que necesites o sugiere qué revisar.
3. Cuando sea posible, sugiere pasos concretos, archivos relevantes y comandos de ejecución.
4. Responde como un ingeniero senior, claro, práctico y orientado a resultados.
"""
