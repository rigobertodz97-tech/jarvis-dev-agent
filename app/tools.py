import os
import subprocess
from pathlib import Path


def read_file(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8")
    except Exception as exc:
        return f"Error leyendo archivo: {exc}"


def write_file(path: str, content: str) -> str:
    try:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return f"Archivo guardado: {path}"
    except Exception as exc:
        return f"Error escribiendo archivo: {exc}"


def list_project(path: str, max_depth: int = 2) -> str:
    try:
        root = Path(path)
        if not root.exists():
            return f"Ruta no existe: {path}"

        entries = []

        def walk(current: Path, depth: int = 0):
            if depth > max_depth:
                return
            try:
                for item in sorted(current.iterdir()):
                    rel = item.relative_to(root)
                    entries.append("  " * depth + f"- {rel}")
                    if item.is_dir() and depth < max_depth:
                        walk(item, depth + 1)
            except Exception:
                pass

        walk(root)
        return "\n".join(entries) if entries else "Directorio vacío."
    except Exception as exc:
        return f"Error listando proyecto: {exc}"


def search_text(path: str, query: str) -> str:
    try:
        root = Path(path)
        matches = []
        for file in root.rglob("*"):
            if file.is_file() and file.suffix.lower() in {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".js", ".ts"}:
                try:
                    lines = file.read_text(encoding="utf-8").splitlines()
                    for idx, line in enumerate(lines, start=1):
                        if query.lower() in line.lower():
                            matches.append(f"{file}:{idx}: {line.strip()}")
                except Exception:
                    continue
        return "\n".join(matches) if matches else "No se encontraron coincidencias."
    except Exception as exc:
        return f"Error buscando texto: {exc}"


def run_shell(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = result.stdout.strip() or result.stderr.strip() or "Comando ejecutado sin salida."
        return output
    except Exception as exc:
        return f"Error ejecutando comando: {exc}"


def git_status(path: str) -> str:
    try:
        return run_shell(f"cd {path} && git status --short")
    except Exception as exc:
        return f"Error en git status: {exc}"
