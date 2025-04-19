# File that gather all function to check on the dockers

import json
import os
import typer
import importlib.resources as resources
from pathlib import Path
import shutil

def parse_packages(value: str) -> list[str]:
    """
    Deal with the parsing of the extra packages given in the command line to build the dockerfile
    """
    try:
        packages = json.loads(value)
        if not isinstance(packages, list) or not all(isinstance(p, str) for p in packages):
            raise typer.BadParameter("extra-packages must be a JSON list of strings.")
        return packages
    except json.JSONDecodeError:
        raise typer.BadParameter("extra-packages must be a valid JSON array (e.g. '[\"vim\", \"htop\"]').")
    

def copy_files_from_package(package_name, subdir_name, destination_dir):
    """
    Copie les fichiers depuis un répertoire spécifique dans un package vers un répertoire local.

    :param package_name: Nom du package Python (ex: 'docker_cli.docker_logic.conf_files')
    :param subdir_name: Nom du sous-dossier à partir duquel les fichiers seront copiés.
    :param destination_dir: Répertoire local de destination où les fichiers seront copiés.
    """
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Accéder au sous-dossier de ressources dans le package
    with resources.path(package_name, subdir_name) as resource_path:
        for file_name in os.listdir(resource_path):
            full_src = os.path.join(resource_path, file_name)
            full_dst = os.path.join(destination_dir, file_name)
            if os.path.isfile(full_src):
                shutil.copy(full_src, full_dst)
                print(f"Copié {full_src} → {full_dst}")

