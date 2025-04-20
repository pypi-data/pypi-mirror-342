import typer
import subprocess
from pathlib import Path

app = typer.Typer(help="""
Build a Quantum Machine Docker image.

This command creates a Docker image using the machine's Dockerfile and dependencies.

Example:
    quantum build machine HelloWorld
""")

@app.command()
def machine(path: str, tag: str = "quantum-machine:latest"):
    """
    Build a Quantum Machine Docker image.

    This command creates a Docker image using the machine's Dockerfile and dependencies.

    Example:
        quantum build machine HelloWorld
    """
    
    project_path = Path(path).resolve()

    if not (project_path / "Dockerfile").exists():
        typer.secho("❌ Dockerfile not found!", fg=typer.colors.RED)
        raise typer.Exit()

    try:
        subprocess.run(["docker", "build", "-t", tag, str(project_path)], check=True)
        typer.secho(f"✅ Docker image '{tag}' built successfully!", fg=typer.colors.GREEN)
    except subprocess.CalledProcessError:
        typer.secho("❌ Failed to build Docker image.", fg=typer.colors.RED)