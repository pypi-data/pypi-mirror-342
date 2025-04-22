from pathlib import Path
import re
from uuid import uuid4
import typer
from rich import print

from scallop.sea import SeaBinary, SeaBlobFlags


app = typer.Typer(help="Scallop CLI - nodejs SEA unpacker, repacker, and script stomper.")


@app.command(help="Unpack a node SEA.")
def unpack(target_binary: str):
    print(":oyster: scallop started in [bold]UNPACK[/bold] mode :oyster:\n")
    target_binary_p = Path(target_binary)
    if not target_binary_p.is_file():
        raise typer.BadParameter(f"File {target_binary} does not exist, or is not a file.")
    print(f"[bold][yellow]* Unpacking '{target_binary}'...[/yellow][/bold]")
    sb = SeaBinary(target_binary_p)
    sea_blob = sb.unpack_sea_blob()
    extract_dir = target_binary_p.parent / f'{target_binary_p.stem}_unpacked'
    extract_dir.mkdir(exist_ok=True)

    target = (extract_dir / f'raw_sea.blob')
    print(f"[bold]\t* Extracting raw SEA blob to '{target}'...[/bold]")
    with (extract_dir / f'raw_sea.blob').open('wb') as f:
        f.write(sea_blob.blob_raw)

    santized_code_path = re.sub(r'[^a-zA-Z0-9_-]', '_', sea_blob.code_path)
    santized_code_path = re.sub(r'_js$', '.js', santized_code_path)
    target = (extract_dir / f'{santized_code_path}')
    print(f"[bold]\t* Extracting main resource to '{target}'...[/bold]")
    with target.open('wb') as f:
        f.write(sea_blob.sea_resource)

    if sea_blob.code_cache:
        target = (extract_dir / f'code_cache.bin')
        print(f"[bold]\t* Extracting code cache to '{target}'...[/bold]")
        with target.open('wb') as f:
            f.write(sea_blob.code_cache)

    if sea_blob.assets:
        for asset_name, asset_data in sea_blob.assets.items():
            if len(asset_name) == 0 and len(asset_data) == 0:
                continue
            if len(asset_name) == 0:
                asset_name = str(uuid4())
            santized_asset_name = re.sub(r'[^a-zA-Z0-9_-]', '_', asset_name)
            target = (extract_dir / f'{santized_asset_name}')
            print(f"[bold]\t* Extracting asset '{asset_name}' to '{target}'...[/bold]")
            with target.open('wb') as f:
                f.write(asset_data)

    print("[green][bold]+ Unpacked successfully![/bold][/green] :tada:")


@app.command(help="Repack a node SEA with a new script or v8 snap, optionally stomping the script with the SEA's code cache.")
def repack(target_binary: str, script_or_snap: str, stomp: bool = False):
    print(":oyster: scallop started in [bold]REPACK[/bold] mode :oyster:\n")
    target_binary_p = Path(target_binary)
    if not target_binary_p.is_file():
        raise typer.BadParameter(f"File {target_binary} does not exist, or is not a file.")
    print(f"[bold][yellow]* Loading '{target_binary}'...[/yellow][/bold]")
    sb = SeaBinary(target_binary_p)
    sea_blob = sb.unpack_sea_blob()

    target_script_p = Path(script_or_snap)
    if not target_script_p.is_file():
        raise typer.BadParameter(f"File {script_or_snap} does not exist, or is not a file.")
    print(f"[bold][yellow]* Replacing main resource with '{script_or_snap}'...[/yellow][/bold]")
    with target_script_p.open('rb') as f:
        sea_blob.sea_resource = f.read()

    sb.repack_sea_blob(sea_blob, stomp)
    print("[green][bold]+ Repacked successfully![/bold][/green] :tada:")


@app.command(help="Repack a node SEA asset.")
def repack_asset(target_binary: str, target_asset_name: str, target_asset: str):
    print(":oyster: scallop started in [bold]REPACK ASSET[/bold] mode :oyster:\n")
    target_binary_p = Path(target_binary)
    if not target_binary_p.is_file():
        raise typer.BadParameter(f"File {target_binary} does not exist, or is not a file.")
    print(f"[bold][yellow]* Loading '{target_binary}'...[/yellow][/bold]")
    sb = SeaBinary(target_binary_p)
    sea_blob = sb.unpack_sea_blob()

    target_asset_p = Path(target_asset)
    if not target_asset_p.is_file():
        raise typer.BadParameter(f"File {target_asset} does not exist, or is not a file.")
    
    print(f"[bold][yellow]* Adding or replacing asset '{target_asset_name}' with '{target_asset}'...[/yellow][/bold]")
    with target_asset_p.open('rb') as f:
        sea_blob.assets = sea_blob.assets or {}
        sea_blob.assets[target_asset_name] = f.read()
    sea_blob.flags |= SeaBlobFlags.INCLUDE_ASSETS

    sb.repack_sea_blob(sea_blob, False)
    print("[green][bold]+ Repacked asset successfully![/bold][/green] :tada:")


if __name__ == "__main__":
    app()
