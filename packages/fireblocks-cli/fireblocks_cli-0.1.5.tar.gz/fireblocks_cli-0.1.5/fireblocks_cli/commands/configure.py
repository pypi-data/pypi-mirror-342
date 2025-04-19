# SPDX-FileCopyrightText: 2025 Ethersecurity Inc.
#
# SPDX-License-Identifier: MPL-2.0

# Author: Shohei KAMON <cameong@stir.network>

import typer
from pathlib import Path
from fireblocks_cli.crypto import generate_key_and_csr
from fireblocks_cli.config import (
    get_config_dir,
    get_config_file,
    get_api_key_dir,
    get_credentials_file,
    DEFAULT_CONFIG,
)
from fireblocks_cli.utils.toml import save_toml

configure_app = typer.Typer()


@configure_app.command("init")
def init():
    """Initialize configuration files and key directories."""
    typer.secho("🛠 Starting Fireblocks CLI initialization...", fg=typer.colors.CYAN)

    # Create the config directory if it doesn't exist
    config_dir = get_config_dir()
    config_dir.mkdir(parents=True, exist_ok=True)
    typer.secho(f"✅ Config directory ensured: {config_dir}", fg=typer.colors.GREEN)

    # Create config.toml if it does not exist
    config_file = get_config_file()
    if not config_file.exists():
        config = DEFAULT_CONFIG.copy()

        # If credentials file exists, use its values to populate config
        credentials_file = get_credentials_file()
        if credentials_file.exists():
            lines = credentials_file.read_text().splitlines()
            for line in lines:
                if "api_id" in line:
                    config["default"]["api_id"] = line.split("=")[-1].strip()
                elif "api_secret_key" in line:
                    config["default"]["api_secret_key"] = line.split("=")[-1].strip()
            typer.secho(
                f"✅ Loaded credentials from: {credentials_file}",
                fg=typer.colors.YELLOW,
            )

        # Save the populated config to file
        save_toml(config, config_file)
        typer.secho(f"✅ Created config.toml: {config_file}", fg=typer.colors.GREEN)
    else:
        typer.secho(
            f"⚠ config.toml already exists: {config_file}", fg=typer.colors.YELLOW
        )

    # Ensure ~/.config/fireblocks-cli/keys directory exists
    api_key_dir = get_api_key_dir()
    api_key_dir.mkdir(parents=True, exist_ok=True)
    typer.secho(f"✅ Keys directory ensured: {api_key_dir}", fg=typer.colors.GREEN)

    typer.secho("🎉 Initialization complete!", fg=typer.colors.CYAN)


@configure_app.command("gen-keys")
def gen_keys():
    """秘密鍵とCSRを api_key_dir に生成します"""
    org = typer.prompt("🔐 組織名を入力してください（例: MyCompany）").strip()
    if not org:
        typer.secho("❌ 組織名は必須です。処理を中止します。", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    key_path, csr_path = generate_key_and_csr(org)
    typer.secho(f"✅ 秘密鍵: {key_path}", fg=typer.colors.GREEN)
    typer.secho(f"✅ CSR   : {csr_path}", fg=typer.colors.GREEN)
