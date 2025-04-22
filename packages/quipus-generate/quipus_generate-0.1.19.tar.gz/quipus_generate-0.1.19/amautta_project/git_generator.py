from pathlib import Path
import subprocess
import sys
import os

def run_command(command, cwd=None):
    subprocess.run(
        command,
        cwd=cwd,
        shell=True,
        check=True,
        stdout=subprocess.DEVNULL,   # No mostrar salida estándar
    )

def create(proccess, name):
    if proccess == "init":
        gitignore = (
            ".env\n"
            ".DS_Store\n"
            ".vscode/\n"
            ".idea/\n"
            "example_entity\n"
            "nginx/sites/example_entity.conf\n"
        )
    elif proccess == "microservice":
        gitignore = (
            "# Entornos virtuales\n"
            "venv/\n"
            ".env/\n"
            "\n"
            "# Archivos de Python compilados\n"
            "__pycache__/\n"
            "*.py[cod]\n"
            "*.pyo\n"
            "\n"
            "# Configuración de IDE\n"
            ".vscode/\n"
            ".idea/\n"
            "\n"
            "# Archivos temporales\n"
            "*.log\n"
            ".DS_Store\n"
            "\n"
            "# Build\n"
            "dist/\n"
            "build/\n"
            "*.egg-info/\n"
            "\n"
            "# Archivos de configuración de Docker\n"
            "Dockerfile\n"
            ".dockerignore\n"
        )

    archivos = {
        ".gitignore": gitignore,
    }

    if os.path.isfile(f"{os.getcwd()}/.gitignore"):
        print("ℹ️ El proyecto git ya se encuentra inicializado.")
        sys.exit()

    # Crear archivos
    for archivo, content in archivos.items():
        ruta_archivo = os.path.join(name, archivo)
        with open(ruta_archivo, "w") as f:
            f.write(content)

    if proccess == "init":
        tipo = "proyecto"
    elif proccess == "microservice":
        tipo = "microservicio"

    print(f"✅ Se creo el archivo .gitignore para el {tipo} '{name}' con éxito.")

    # Ejecutar comandos de git en el directorio del proyecto
    run_command("git init", cwd=name)
    run_command("git add .", cwd=name)
    run_command("git commit -m 'Initial commit'", cwd=name)
    run_command("git branch -M main", cwd=name)

    print(f"✅ Se inicializó el repositorio git para el {tipo} '{name}' con éxito.")

