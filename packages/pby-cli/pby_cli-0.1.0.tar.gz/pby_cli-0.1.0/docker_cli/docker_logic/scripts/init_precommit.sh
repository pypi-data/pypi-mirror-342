#!/bin/bash

CONFIG_FILE="/workspace/.pre-commit-config.yaml"
RUFF_CONFIG_FILE="/etc/skel/ruff_pre_commit.yaml"

# Vérifier si on est bien dans un projet git
if [ -d "/workspace/.git" ]; then
    echo "[INIT] .git directory found"

    # Créer le fichier s'il n'existe pas
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "[INIT] No .pre-commit-config.yaml found, creating one..."
        touch "$CONFIG_FILE"
    fi

    # Ajouter Ruff uniquement s’il n’est pas déjà présent
    if ! grep -q "https://github.com/astral-sh/ruff-pre-commit" "$CONFIG_FILE"; then
        echo "[INIT] Adding Ruff config to .pre-commit-config.yaml"
        cat "$RUFF_CONFIG_FILE" >> "$CONFIG_FILE"
    else
        echo "[INIT] Ruff already configured in .pre-commit-config.yaml"
    fi

    # Installer les hooks
    echo "[INIT] Installing pre-commit hooks..."
    cd /workspace && pre-commit install
else
    echo "[INIT] No Git repo found, skipping pre-commit setup"
fi

# Ensuite, exécuter la commande passée au container
exec "$@"