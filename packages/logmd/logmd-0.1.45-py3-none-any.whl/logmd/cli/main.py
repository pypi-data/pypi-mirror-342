#!/usr/bin/env python
import time
import io
from tqdm import tqdm
from typer import Typer
from pathlib import Path
import ase
import typer
from logmd import LogMD
from logmd.cli.auth import auth_app
import sys 

# Make `logmd file.pdb` work as `logmd upload file.pdb`. 
if len(sys.argv) > 1 and "." in sys.argv[1] and not sys.argv[1].startswith("-"):
    sys.argv.insert(1, "upload")

app = Typer(name="logmd", rich_markup_mode="rich")
app.add_typer(auth_app, name="")

@app.command(name="upload")
def upload_file(
    file_path: Path = typer.Argument(help="The path to the file to upload."),
    project: str = typer.Option(
        default="", help="The project to upload to [requires login]."
    ),
    topology: Path = typer.Option(default=None, help="The path to the topology file to upload."),
):
    """
    Upload a file to LogMD.
    """
    if topology is not None:
        # assume desmond format. 
        try:
            from pymol import cmd 
        except:
            print("Pymol not installed, it's required for Desmond files. ")
            print("Install with `conda install -c schrodinger pymol .")
            exit()

        # Redirect stdout temporarily
        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            # Load the structure and trajectory
            cmd.load(topology, "m")
            cmd.load_traj(file_path, "m")

        n_frames = cmd.count_frames("m")
        print(f"Total number of frames: {n_frames}")
        logmd = LogMD()

        from tqdm import tqdm
        #for frame in tqdm(range(1, n_frames + 1)):
        for frame in tqdm(range(1, n_frames + 1)):
            cmd.frame(frame)
            cmd.save('.tmp.pdb', "m", state=frame, format="pdb")
            pdb = open('.tmp.pdb').read()
            logmd(pdb)
            time.sleep(0.1)
        exit()
        
    logmd_obj = LogMD(project=project)
    content = file_path.read_text()
    model_count = content.count("\nMODEL")

    if model_count <= 1:
        atoms = ase.io.read(file_path)
        logmd_obj(atoms)
    else:
        models = content.split("\nMODEL")
        for model in tqdm(
            models[1:]
        ):  # Skip the first split part as it is before the first MODEL
            buffer = io.StringIO("MODEL" + model)
            # Ensure buffer content is a string
            buffer_content = buffer.getvalue()
            if isinstance(buffer_content, bytes):
                buffer_content = buffer_content.decode(
                    "utf-8"
                )  # Decode bytes to string
            atoms = ase.io.read(
                io.StringIO(buffer_content), format="proteindatabank"
            )  # Specify the correct format if needed
            logmd_obj(atoms)

            time.sleep(0.2)


@app.command(name="watch")
def watch_from_terminal(file_path: Path, topology: Path = None, interval: int = 1):
    """
    Watch a file and upload it to LogMD when it changes.
    """
    import hashlib

    if topology is not None:
        hash = ""
        #logmd_obj = LogMD()
        # assume desmond format. 
        try:
            from pymol import cmd 
        except:
            print("Pymol not installed, it's required for Desmond files. ")
            print("Install with `conda install -c schrodinger pymol .")
            exit()

        import contextlib
        with contextlib.redirect_stdout(io.StringIO()):
            cmd.load(topology, "m")
            cmd.load_traj(file_path, "m")#, start=0, stop=700)
        n_frames = cmd.count_frames("m")
        print(f"Found {n_frames} ready to upload. ")
        print('looking for more frames...')

        logmd = LogMD()
        for frame in tqdm(range(1, n_frames + 1, interval)):
            cmd.frame(frame)
            cmd.save('.tmp.pdb', "m", state=frame, format="pdb")
            pdb = open('.tmp.pdb').read()
            logmd(pdb)
            time.sleep(0.1)

        import os 
        while True:
            '''with open(os.devnull, 'w') as devnull:
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = devnull
                sys.stderr = devnull
                try:
                    # Load the structure and trajectory
                    with contextlib.redirect_stdout(io.StringIO()):
                        cmd.load(topology, "m")
                        cmd.load_traj(file_path, "m", start=n_frames)
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr'''

            cmd.load(topology, "m")
            cmd.load_traj(file_path, "m", start=n_frames)

            new_n_frames = cmd.count_frames("m")
            print(f"Total {n_frames} new {new_n_frames-1} url={logmd.url}")
            if new_n_frames > 1: 
                print(f"Found {new_n_frames-1} new frames to upload. ")
                for frame in tqdm(range(1, new_n_frames + 1, interval)):
                    cmd.frame(frame)
                    cmd.save('.tmp.pdb', "m", state=frame, format="pdb")
                    pdb = open('.tmp.pdb').read()
                    print(len(pdb))
                    logmd(pdb)
                    time.sleep(0.1)
                n_frames += new_n_frames - 1

            time.sleep(2.0)

        exit()

    hash = ""
    logmd_obj = LogMD()
    while True:
        new_hash = hashlib.sha256(open(file_path, "rb").read()).hexdigest()
        if new_hash != hash:
            print(f"found change in {file_path}, uploading...")
            hash = new_hash
            logmd_obj(ase.io.read(file_path))
        time.sleep(0.5)


@app.command(name="demos", rich_help_panel="Resources")
def demos():
    """
    Display demos.
    """
    from rich.table import Table
    import rich

    table = Table(title="Demos")
    table.add_column("What")
    table.add_column("Where")

    table.add_row(
        "[green]Login[/green]",
        "[dim]Learn how to login[/dim]\n[blue]https://github.com/log-md/logmd/blob/main/demos/demo_login.py[/blue]",
    )
    table.add_row(
        "[green]ASE[/green]",
        "[dim]See how to log with ASE[/dim]\n[blue]https://github.com/log-md/logmd/blob/main/demos/demo_ase.py[/blue]",
    )
    table.add_row(
        "[green]OpenMM[/green]",
        "[dim]See how to log with OpenMM[/dim]\n[blue]https://github.com/log-md/logmd/blob/main/demos/demo_openmm.py[/blue]",
    )

    rich.print(table)


@app.command(name="vchat", rich_help_panel="Resources")
def vchat():
    """
    Chat with LogMD.
    """
    from rich.panel import Panel
    import rich

    panel = Panel.fit(
        """
Please book a time with us here:

[blue]https://calendly.com/alexander-mathiasen/vchat[/blue]

Or reach out to us at [blue]alexmath@gmail.com[/blue]
        """,
        title="Get in touch",
        border_style="blue",
        title_align="center",
    )
    rich.print(panel)


if __name__ == "__main__":
    app()
