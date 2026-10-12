from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.agent import ask_model, build_task_prompt, generate_mode_system_prompt
from app.config import ALLOW_COMMANDS
from app.tools import list_project, run_shell

app = FastAPI(title="JARVIS Dev Agent", version="0.1.0")


class TaskRequest(BaseModel):
    task: str
    project_path: str = "."
    mode: str = "architect"


@app.get("/")
def root():
    return {
        "message": "JARVIS Dev Agent online",
        "status": "ok",
        "modes": ["architect", "debugger", "devops", "qa", "reviewer"],
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/task")
def process_task(req: TaskRequest):
    try:
        if req.mode.lower() not in {"architect", "debugger", "devops", "qa", "reviewer"}:
            raise HTTPException(status_code=400, detail="Modo no soportado")

        project_summary = list_project(req.project_path, max_depth=2)
        prompt = build_task_prompt(req.task, req.project_path, req.mode)
        system_prompt = generate_mode_system_prompt(req.mode)

        response = ask_model(prompt, system_prompt=system_prompt)

        extra = {
            "project_structure": project_summary,
            "allows_commands": ALLOW_COMMANDS,
            "mode": req.mode,
        }

        if ALLOW_COMMANDS:
            try:
                extra["git_status"] = run_shell(f"cd {req.project_path} && git status --short")
            except Exception:
                extra["git_status"] = "No disponible"

        return {
            "response": response,
            "context": extra,
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
