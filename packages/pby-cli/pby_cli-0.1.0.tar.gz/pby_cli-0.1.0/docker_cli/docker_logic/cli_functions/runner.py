# File to run a container

from pathlib import Path
from typing import Optional
import typer
import subprocess
import os
import sys


def add_user_to_docker_group():
    try:
        # Vérifie si l'utilisateur est déjà dans le groupe docker
        user_groups = subprocess.check_output("groups", shell=True).decode().strip()
        if "docker" not in user_groups:
            print("L'utilisateur n'est pas dans le groupe 'docker'. Tentative d'ajout...")
            subprocess.check_call(["sudo", "usermod", "-aG", "docker", os.getlogin()])
            print("L'utilisateur a été ajouté au groupe 'docker'. Application immédiate des changements.")
            
            # Appliquer immédiatement les changements de groupe avec newgrp
            subprocess.check_call("newgrp docker", shell=True)
            print("Les modifications ont été appliquées avec succès.")
            print("Relancer la commande pour créer le container")
        else:
            print("L'utilisateur fait déjà partie du groupe 'docker'.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'ajout au groupe Docker : {e}")
        sys.exit(1)

def run_container(
    image_name: str,
    container_name: str,
    cpus: int,
    gpu: bool,
    ssh_port: int,
    workspace: Path,
    data_project: Optional[Path] = None,
    data_device: Optional[Path] = None,
    model_dir: Optional[Path] = None,):
     

    add_user_to_docker_group()
    command = [
        "docker", "run", "-it", "-d", #"--rm",,
        "--name", container_name,
        "--cpus", str(cpus),
        "-v", f"{workspace}:/workspace",
        "-p", f"{ssh_port}:22",
        "-w", "/workspace",
        "--shm-size=256g"
    ]

    venv_path = workspace / ".venv"
    if venv_path.exists():
        command.extend(["-v", f"{venv_path.resolve()}:{venv_path}"])
        
    if gpu:
        command += ["--runtime=nvidia"]

    if data_project:
        command += ["-v", f"{data_project}:/data_project"]

    if data_device:
        command += ["-v", f"{data_device}:/data_device"]

    if model_dir:
        command += ["-v", f"{model_dir}:/models"]

    command.append(f"{image_name}:latest")

    typer.echo(f"Lancement du conteneur : {' '.join(command)}")
    # Capture the output and error
    subprocess.run(command) 
    print(f"Container généré avec succès")
    print(" ")
    print("Tu peux maintenant utiliser le container avec:")
    print(f"docker exec -it {container_name} bash")
