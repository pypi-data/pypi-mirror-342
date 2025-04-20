import asyncio
import os
import zipfile
from pathlib import Path

import click
import yaml

from metablock import Metablock

METABLOCK_SPACE = os.environ.get("METABLOCK_SPACE", "")
METABLOCK_ENV = os.environ.get("METABLOCK_ENV", "prod")
METABLOCK_BLOCK_ID = os.environ.get("METABLOCK_BLOCK_ID", "")
METABLOCK_API_TOKEN = os.environ.get("METABLOCK_API_TOKEN", "")


def manifest(file_path: Path) -> dict:
    return yaml.safe_load(file_path.read_text())


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--space",
    "space_name",
    help="Space name",
    default=METABLOCK_SPACE,
    show_default=True,
)
@click.option("--token", help="metablock API token", default=METABLOCK_API_TOKEN)
def apply(path: str, space_name: str, token: str) -> None:
    """Apply metablock manifest to a metablock space"""
    asyncio.get_event_loop().run_until_complete(
        _apply(path, space_name or METABLOCK_SPACE, token or METABLOCK_API_TOKEN)
    )


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--env",
    help="Environment to ship to",
    type=click.Choice(["prod", "stage"]),
    default=METABLOCK_ENV,
    show_default=True,
)
@click.option(
    "--block-id",
    help="Block ID",
    default=METABLOCK_BLOCK_ID,
    show_default=True,
)
@click.option(
    "--name",
    help="Optional deployment name",
    default="shipped from metablock-py",
    show_default=True,
)
@click.option("--token", help="metablock API token", default=METABLOCK_API_TOKEN)
def ship(path: str, env: str, block_id: str, name: str, token: str) -> None:
    """Deploy a new version of html block"""
    asyncio.get_event_loop().run_until_complete(
        _ship(path, env, block_id, name, token or METABLOCK_API_TOKEN)
    )


async def _apply(path: str, space_name: str, token: str) -> None:
    if not token:
        click.echo("metablock API token is required", err=True)
        raise click.Abort()
    if not space_name:
        click.echo("metablock space is required", err=True)
        raise click.Abort()
    p = Path(path)
    blocks = []
    for file_path in p.glob("*.yaml"):
        name = file_path.name.split(".")[0]
        blocks.append((name, manifest(file_path)))
    async with Metablock(auth_key=token) as mb:
        space = await mb.spaces.get(space_name)
        svc = await space.blocks.get_list()
        click.echo(f"space {space.name} has {len(svc)} blocks")
        by_name = {s["name"]: s for s in svc}
        for name, config in blocks:
            block = by_name.get(name)
            if block:
                # update
                await mb.blocks.update(block.id, **config)
                click.echo(f"updated block {name}")
            else:
                # create
                await space.blocks.create(name=name, **config)
                click.echo(f"created new block {name}")


async def _ship(path: str, env: str, block_id: str, name: str, token: str) -> None:
    if not token:
        click.echo("metablock API token is required", err=True)
        raise click.Abort()
    if not block_id:
        click.echo("metablock block-id is required", err=True)
        raise click.Abort()
    p = Path(path)
    if not p.is_dir():
        click.echo(f"path {p} does not exist", err=True)
        raise click.Abort()

    # Create a zip file from the directory
    zip_path = p.with_suffix(".zip")
    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file in p.rglob("*"):  # Recursively add all files in the directory
                arcname = file.relative_to(p)  # Preserve relative paths in the archive
                zipf.write(file, arcname)
        click.echo(f"Created zip file: {zip_path}")

        async with Metablock(auth_key=token) as mb:
            block = await mb.blocks.get(block_id)
            await block.ship(zip_path, name=name, env=env)
            click.echo(f"shipped {zip_path} to {block.name} {env}")
    finally:
        # Clean up the zip file after shipping
        if zip_path.exists():
            zip_path.unlink()
            click.echo(f"Removed temporary zip file: {zip_path}")
