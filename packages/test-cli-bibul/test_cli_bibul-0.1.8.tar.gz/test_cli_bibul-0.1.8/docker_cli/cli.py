import getpass
import os
from pathlib import Path
import typer
from docker_cli.docker_logic.cli_functions.builder import build_image
from docker_cli.docker_logic.cli_functions.runner import run_container
from docker_cli.docker_logic.cli_functions.util import copy_files_from_package, parse_packages, copy_files_from_directory
from docker_cli.docker_logic.scripts.test import test
#from docker.runner import run_container




app = typer.Typer(help="CLI pour gérer les images et containers Docker Probayes")
# Build Docker image
@app.command()
def build(
    name: str = typer.Argument(..., help="Nom de l'image"),
    base_image: str = typer.Option("nvcr.io/nvidia/pytorch:23.06-py3", help="Nom de l'image de base pour la création du Dockerfile"),
    probayes: bool = typer.Option(False, "--with-probayes", help="Inclure l’environnement Probayes"),
    extra_packages:str = typer.Option("[]", help="Packages système supplémentaires à installer", callback=parse_packages) #TO-DO : Parse packages to avoid overloading the command line
):

    copy_files_from_package("docker_cli.docker_logic.conf_files", "", "./conf_files")
    copy_files_from_package("docker_cli.docker_logic.templates", "", "./templates")
    copy_files_from_package("docker_cli.docker_logic.scripts", "", "./scripts")
    build_image(name=name,base_image=base_image, include_probayes=probayes,extra_packages=extra_packages)

# Run Docker container
@app.command()
def run(
    image_name: str = typer.Argument(..., help="Nom de l'image Docker à utiliser"),
    cpus: int = typer.Option(4, help="Nombre de CPUs à allouer"),
    ssh_port: int = typer.Option(2222, help="Port SSH exposé"),
    gpu: bool = typer.Option(False, help="Activer l'accès GPU via NVIDIA runtime"),
    workspace: Path = typer.Option(Path.cwd(), help="Dossier du code source à monter"),
    data_project: Path = typer.Option(None, help="Chemin vers les données projet"),
    data_device: Path = typer.Option(None, help="Chemin vers les données device"),
    model_dir: Path = typer.Option(None, help="Chemin vers les modèles"),
):
    user = getpass.getuser()
    container_name = f"{image_name}-{user}-dev"

    run_container(image_name=image_name, container_name=container_name, cpus=cpus, gpu=gpu, ssh_port=ssh_port, workspace=workspace, data_project=data_project, data_device=data_device, model_dir=model_dir)






# Point d'entrée de l'application
if __name__ == "__main__":
    app()
