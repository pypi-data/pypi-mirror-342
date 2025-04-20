import typer
import subprocess
from pathlib import Path
from collections import defaultdict, deque
import json
import shutil
import yaml

app = typer.Typer(help="""
    Run a Quantum Machine or Workflow locally using Python.

    Example:
        quantum run machine HelloWorld
        quantum run workflow MyWorkflow
    """
)

REQUIRED_KEYS = {"machine_name", "input_data", "output", "depends_machine"}

@app.command()
def machine(machine_name: str):
    """
    Run a Quantum Machine locally using Python.

    Example:
        quantum run machine HelloWorld
    """
    # ✅ Check for Machine Folder is exist
    machine_path = Path(machine_name).resolve()
    input_json_path =  machine_path
    if not input_json_path.exists():
        typer.secho(f"❌ '{machine_name}' Machine Folder not found.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    # ✅ Check for core engine only when running the machine
    try:
        from quantum.CoreEngine import CoreEngine  # Only needed when actually running the machine
    except ImportError:
        typer.secho("❌ Missing dependency: 'quantum-core-engine' is required. Please install it separately.", fg=typer.colors.RED)
        raise typer.Exit(1)
    
    typer.echo(f"🚀 Starting Quantum Machine: {machine_name}")

    main_script = machine_path / "main.py"
    if not main_script.exists():
        typer.secho("❌ main.py not found in machine directory.", fg=typer.colors.RED)
        raise typer.Exit(1)

    input_json_path = machine_path / "input.json"
    if not input_json_path.exists():
        typer.secho("❌ input.json file not found in the machine directory.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # ✅ Load and validate input.json structure
    try:
        with open(input_json_path) as f:
            input_data = json.load(f)
    except json.JSONDecodeError:
        typer.secho("❌ input.json is not valid JSON.", fg=typer.colors.RED)
        raise typer.Exit(1)

    # ✅ Check for all required keys
    missing_keys = REQUIRED_KEYS - input_data.keys()
    if missing_keys:
        typer.secho(f"❌ input.json is missing required keys: {', '.join(missing_keys)}", fg=typer.colors.RED)
        raise typer.Exit(1)

    # Determine the Python executable to use
    python_executable = shutil.which("python") or shutil.which("python3")
    if not python_executable:
        typer.secho("❌ Neither 'python3' nor 'python' is available in the environment.", fg=typer.colors.RED)
        raise typer.Exit(1)

    command = [
        python_executable,
        str(Path().joinpath(machine_name, "main.py")),
        #f"./{machine_name}/main.py",
        json.dumps(input_data)
    ]

    typer.echo(f"Running machine '{machine_name}' with env='dev'")
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    
    # Stream logs line by line
    for line in process.stdout:
        print(line, end='')

    process.wait()

    if process.returncode == 0:
        typer.echo("✅ Machine executed successfully")
        typer.echo(process.stdout)
    else:
        typer.echo("❌ Machine execution failed", err=True)
        typer.echo(process.stderr, err=True)


@app.command("workflow")
def run_workflow(
    workflow_name: str = typer.Argument(..., help="Name of the workflow to run (folder containing workflow.yaml)")
):
    """
    Run a Quantum Workflow locally.

    Example:
        quantum run workflow HelloWorld
    """
    workflow_file = Path.joinpath(Path(workflow_name), "workflow.yaml")

    if not workflow_file.exists():
        typer.secho(f"❌ Workflow file '{workflow_file}' does not exist.", fg=typer.colors.RED)
        raise typer.Exit(1)

    with open(workflow_file, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            typer.secho(f"❌ Error reading workflow.yaml: {e}", fg=typer.colors.RED)
            raise typer.Exit(1)

    machines = data.get("machines", {})
    print(f"Machines: {machines}")
    
    # Build DAG and in-degree map
    dag = defaultdict(list)
    in_degree = defaultdict(int)
    for child, parents in machines.items():
        if isinstance(parents, list):
            for parent in parents:
                dag[parent].append(child)
                in_degree[child] += 1
        else:
            machines[child] = []

    # Queue machines with 0 in-degree (no dependencies)
    execution_queue = deque([m for m in machines if in_degree[m] == 0])
    execution_order = []

    while execution_queue:
        current = execution_queue.popleft()
        execution_order.append(current)
        for dependent in dag.get(current, []):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                execution_queue.append(dependent)

    if len(execution_order) != len(machines):
        typer.secho("❌ Cycle detected or invalid dependencies in workflow graph.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"\n📋 Execution Order: {execution_order}\n", fg=typer.colors.BLUE)

    success = set()
    failed = set()

    for machine in execution_order:
        parents = machines[machine]
        if any(p not in success for p in parents):
            typer.secho(f"⏭️ Skipping '{machine}' because one or more parent(s) failed.", fg=typer.colors.YELLOW)
            failed.add(machine)
            continue

        typer.secho(f"\n🚀 Starting Quantum Machine: {machine}", fg=typer.colors.CYAN)

        machine_path = Path(machine).resolve()
        if not machine_path.exists():
            typer.secho(f"❌ '{machine}' Machine Folder not found.", fg=typer.colors.RED)
            failed.add(machine)
            continue

        input_json_path = machine_path / "input.json"
        if not input_json_path.exists():
            typer.secho(f"❌ input.json file not found in {machine}.", fg=typer.colors.RED)
            failed.add(machine)
            continue

        try:
            from quantum.CoreEngine import CoreEngine
        except ImportError:
            typer.secho("❌ Missing dependency: 'quantum-core-engine' is required. Please install it.", fg=typer.colors.RED)
            raise typer.Exit(1)

        try:
            with input_json_path.open() as f:
                input_data = json.load(f)
                input_data["workflow_name"] = workflow_name
        except json.JSONDecodeError:
            typer.secho("❌ input.json is not valid JSON.", fg=typer.colors.RED)
            failed.add(machine)
            continue

        missing_keys = REQUIRED_KEYS - input_data.keys()
        if missing_keys:
            typer.secho(f"❌ input.json is missing keys: {', '.join(missing_keys)}", fg=typer.colors.RED)
            failed.add(machine)
            continue

        python_exec = shutil.which("python") or shutil.which("python3")
        if not python_exec:
            typer.secho("❌ Python interpreter not found.", fg=typer.colors.RED)
            raise typer.Exit(1)

        command = [python_exec, str(machine_path / "main.py"), json.dumps(input_data)]
        typer.echo(f"Running '{machine}' with env='dev'")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')

        process.wait()
        if process.returncode == 0:
            typer.secho(f"✅ Machine '{machine}' executed successfully\n", fg=typer.colors.GREEN)
            success.add(machine)
        else:
            typer.secho(f"❌ Machine '{machine}' execution failed\n", fg=typer.colors.RED)
            failed.add(machine)

    typer.secho("\n🏁 Workflow Completed!", fg=typer.colors.CYAN)
    typer.secho(f"✅ Successful Machines: {sorted(success)}", fg=typer.colors.GREEN)
    typer.secho(f"❌ Failed Machines: {sorted(failed)}", fg=typer.colors.RED)
