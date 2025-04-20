import click
import os
import sys
import platform  # Added import for ReflexQL clipboard compatibility
from dotenv import load_dotenv
import yaml
import json
import subprocess
import threading
import time

# Load environment variables from .env file in current directory or from HOME/.env
load_dotenv()
dotenv_path = os.path.join(os.path.expanduser("~"), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# Add the current directory and parent directory to the path for all import scenarios
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
package_dir = os.path.dirname(parent_dir)  # tushell package root

# Add all potential import paths
paths_to_add = [current_dir, parent_dir, package_dir]
for path in paths_to_add:
    if path not in sys.path:
        sys.path.insert(0, path)

# Try different import strategies to handle both direct execution and package import
try:
    # First try absolute imports (when run as a script)
    from tushell.reflexql import ClipboardExchange
except ImportError:
    try:
        # Fall back to relative imports (when run as package)
        from .reflexql import ClipboardExchange
    except ImportError:
        try:
            # Look for a local module (in the same directory)
            import reflexql
            ClipboardExchange = reflexql.ClipboardExchange
        except ImportError:
            print("Error: Could not import ClipboardExchange from reflexql module.")
            print("Make sure reflexql.py contains the ClipboardExchange class definition.")
            sys.exit(1)

# Import other modules with the same flexible strategy
try:
    # Try package imports first
    from tushell.orchestration import draw_memory_key_graph, graphbuilder_sync
    from tushell.lattice_drop import fetch_echonode_data, process_echonode_data, render_echonode_data, emit_live_reports
    from tushell.curating_red_stones import execute_curating_red_stones
    from tushell.echonode_trace_activation import execute_echonode_trace_activation
    from tushell.enriched_version_fractale_001 import execute_enriched_version_fractale_001
    from tushell.redstone_writer import RedStoneWriter
except ImportError:
    try:
        # Fall back to relative imports
        from .orchestration import draw_memory_key_graph, graphbuilder_sync
        from .lattice_drop import fetch_echonode_data, process_echonode_data, render_echonode_data, emit_live_reports
        from .curating_red_stones import execute_curating_red_stones
        from .echonode_trace_activation import execute_echonode_trace_activation
        from .enriched_version_fractale_001 import execute_enriched_version_fractale_001
        from .redstone_writer import RedStoneWriter
    except ImportError:
        # Last resort: direct imports
        from orchestration import draw_memory_key_graph, graphbuilder_sync
        from lattice_drop import fetch_echonode_data, process_echonode_data, render_echonode_data, emit_live_reports
        from curating_red_stones import execute_curating_red_stones
        from echonode_trace_activation import execute_echonode_trace_activation
        from enriched_version_fractale_001 import execute_enriched_version_fractale_001
        from redstone_writer import RedStoneWriter

try:
    from tushell.trinity_superecho import TrinitySuperEcho
except ImportError:
    try:
        from .trinity_superecho import TrinitySuperEcho
    except ImportError:
        TrinitySuperEcho = None

import requests

@click.command()
def scan_nodes():
    """Simulate scanning and listing nodes in the system."""
    click.echo("Scanning nodes... (placeholder for recursive node scanning)")

@click.command()
def flex():
    """Demonstrate flexible orchestration of tasks."""
    click.echo("Flexing tasks... (placeholder for flexible task orchestration)")

@click.command()
def trace_orbit():
    """Trace and visualize the orbit of data or processes."""
    click.echo("Tracing orbit... (placeholder for data/process orbit tracing)")

@click.command()
def echo_sync():
    """Synchronize data or processes across nodes."""
    click.echo("Synchronizing... (placeholder for data/process synchronization)")

@click.command()
def draw_memory_graph():
    """Print an ASCII-rendered graph of the memory keys and Arc structure."""
    draw_memory_key_graph()
    echonode_data = fetch_echonode_data()
    if (echonode_data):
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        # Include delta overlays
        click.echo("Delta overlays included.")

@click.command()
def curating_red_stones(verbose: bool = False, dry_run: bool = False):
    """Visualize and structure Red Stone metadata connections."""
    if verbose:
        click.echo("Activating Curating Red Stones Lattice with verbose output...")
    if dry_run:
        click.echo("Dry run mode: No changes will be committed.")
    execute_curating_red_stones()

@click.command()
def activate_echonode_trace(verbose: bool = False, dry_run: bool = False):
    """Activate and trace EchoNode sessions."""
    if verbose:
        click.echo("Activating EchoNode Trace with verbose output...")
    if dry_run:
        click.echo("Dry run mode: No changes will be committed.")
    execute_echonode_trace_activation()

@click.command()
def enrich_fractale_version(verbose: bool = False, dry_run: bool = False):
    """Enhance and enrich the Fractale 001 version."""
    if verbose:
        click.echo("Activating Enriched Version Fractale 001 with verbose output...")
    if dry_run:
        click.echo("Dry run mode: No changes will be committed.")
    execute_enriched_version_fractale_001()

@click.command()
@click.option('--api-url', required=True, help='API URL for GraphBuilderSync')
@click.option('--token', required=True, help='Authorization token for GraphBuilderSync')
@click.option('--node-id', default=None, help='Node ID for GraphBuilderSync')
@click.option('--node-data', default=None, help='Node data for GraphBuilderSync')
@click.option('--action', type=click.Choice(['push', 'pull']), default='pull', help='Action for GraphBuilderSync')
@click.option('--narrative', is_flag=True, help='Narrative context for GraphBuilderSync. For more info, visit https://YOUR_EH_API_URL/latice/tushell')
def graphbuilder_sync_command(api_url, token, node_id, node_data, action, narrative):
    """Execute GraphBuilderSync operations."""
    if narrative:
        click.echo("Executing GraphBuilderSync with narrative context...")
    result = graphbuilder_sync(api_url, token, node_id, node_data, action)
    click.echo(result)

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--commit-message', required=True, help='Commit message for encoding resonance')
def redstone_encode_resonance(repo_path, commit_message):
    """Encode recursive resonance into commits."""
    writer = RedStoneWriter(repo_path)
    writer.encode_resonance(commit_message)
    click.echo("Encoded recursive resonance into commit.")

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--commit-message', required=True, help='Commit message for writing narrative diffs')
@click.option('--diffs', required=True, help='Narrative diffs to be written to commit message')
def redstone_write_narrative_diffs(repo_path, commit_message, diffs):
    """Write narrative diffs to commit messages."""
    writer = RedStoneWriter(repo_path)
    narrative_diff = writer.write_narrative_diffs(commit_message, diffs)
    click.echo(narrative_diff)

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--anchors', required=True, help='Resonance anchors to be stored')
def redstone_store_resonance_anchors(repo_path, anchors):
    """Store resonance anchors in .redstone.json."""
    writer = RedStoneWriter(repo_path)
    writer.store_resonance_anchors(anchors)
    click.echo("Stored resonance anchors in .redstone.json.")

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--echonode-metadata', required=True, help='EchoNode metadata to be synced')
def redstone_sync_echonode_metadata(repo_path, echonode_metadata):
    """Sync with EchoNode metadata."""
    writer = RedStoneWriter(repo_path)
    writer.sync_with_echonode_metadata(echonode_metadata)
    click.echo("Synced with EchoNode metadata.")

@click.command()
@click.option('--repo-path', required=True, help='Path to the repository')
@click.option('--redstone-score', required=True, type=int, help='RedStone score for post-commit analysis')
def redstone_post_commit_analysis(repo_path, redstone_score):
    """Support RedStone score metadata field for post-commit analysis."""
    writer = RedStoneWriter(repo_path)
    writer.post_commit_analysis(redstone_score)
    click.echo("Supported RedStone score metadata field for post-commit analysis.")

@click.command()
def echo_live_reports():
    """Emit live reports from EchoNodes tied to active narrative arcs."""
    emit_live_reports()
    # Integrate with fractalstone_protocol, redstone_protocol, and EchoMuse glyph emitters
    click.echo("Live reports integrated with fractalstone_protocol, redstone_protocol, and EchoMuse glyph emitters.")

@click.command()
@click.option('--trace-id', required=False, help='Trace ID for visual replay')
@click.option('--render', is_flag=True, help='Render visual trace replay')
@click.option('--muse-mode', is_flag=True, help='Enable Muse Mode for glyph-enhanced, poetic status report')
@click.option('--init', is_flag=True, help='Initialize Muse Mode YAML dataset')
@click.option('--interactive', is_flag=True, help='Interactive mode with terminal menu choices')
@click.option('--help', is_flag=True, help='Show detailed explanation of Muse Mode')
def mia_status(trace_id, render, muse_mode, init, interactive, help):
    """Provide information about Mia's current state or status."""
    # Get environment variables inside function to ensure they're up-to-date
    EH_API_URL = os.getenv("EH_API_URL")
    EH_TOKEN = os.getenv("EH_TOKEN")
    
    if help:
        click.echo("""
        --muse-mode: Enable Muse Mode for glyph-enhanced, poetic status report.
        Muse Mode reflects the emotional state, recent recursion activity, and redstone modulation.

        Features and Corresponding Keys:
        - Emotional State: Retrieves 'emotional_state' from the YAML file and maps to get-memory API.
        - Recursion Activity: Retrieves 'recursion_activity' from the YAML file and maps to get-memory API.
        - Redstone Modulation: Retrieves 'redstone_modulation' from the YAML file and maps to get-memory API.
        - Glyph Keys: Retrieves 'glyph_keys' from the YAML file and maps to get-memory API.
        - Echo Node Bindings: Retrieves 'echo_node_bindings' from the YAML file and maps to get-memory API.
        - Vault Whisper: Retrieves 'vault_whisper' from the YAML file and maps to get-memory API.

        Example YAML Output:
        emotional_state:
          - redstones:vcu.CeSaReT...
        recursion_activity:
          - Trace:042a0ea2...
          - Trace:072e28a3...
        redstone_modulation:
          - redstones:vcu.CeSaReT.jgwill.tushell.42...
        glyph_keys:
          - glyphstyle::SignalSet.StandardV1
        echo_node_bindings:
          - tushell_langfuse:EchoMuse.CanvasTraceSync.V1
        vault_whisper:
          - Portal:MietteTale

        Use --init to generate a YAML scaffold representing the current emotional, recursive, and narrative environment of EchoMuse.
        """)
        return

    echonode_data = fetch_echonode_data()
    if not echonode_data:
        print("Error: Unable to fetch EchoNode data.- Not implemented yet.")
        print("For now, we set a dummy value so it would process the Mia-Status")
        echonode_data = {
            id: "dummy",
            trace_id: "dummy"
        }
            
    if echonode_data:
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        click.echo("Mia's status has been retrieved and displayed.")

        if muse_mode:
            try:
                with open("muse_mode.yaml", "r") as file:
                    muse_data = yaml.safe_load(file)

                click.echo("🎭 Muse Mode Active:\n")
                for key, values in muse_data.items():
                    click.echo(f"{key.capitalize()}:")
                    for value in values:
                        click.echo(f"  - {value}")

                # Map features to keys and display them
                feature_key_map = {
                    "Emotional State": "emotional_state",
                    "Recursion Activity": "recursion_activity",
                    "Redstone Modulation": "redstone_modulation",
                    "Glyph Keys": "glyph_keys",
                    "Echo Node Bindings": "echo_node_bindings",
                    "Vault Whisper": "vault_whisper"
                }

                DEBUG=False
                if DEBUG:
                    click.echo("\nFeature to Key Mapping:")
                    for feature, key in feature_key_map.items():
                        if key in muse_data:
                            click.echo(f"{feature}: {muse_data[key]}")
                        else:
                            click.echo(f"{feature}: Key not found")

                # Example: Use scan-keys to find related keys
                click.echo("\nScanning for related keys...")
                click.echo("\n  JG's Notes:  I have not removed that because it could become scanning for subkeys.")
                pattern = "Trace"
                response = requests.get(f"{EH_API_URL}/api/scan", params={"pattern": pattern}, headers={"Authorization": f"Bearer {EH_TOKEN}"})
                if response.status_code == 200:
                    keys = response.json().get('keys', [])
                    click.echo("Related Keys:")
                    for key in keys:
                        click.echo(f"  - {key}")
                else:
                    click.echo("Error scanning keys.")

                click.echo("\n---------End of a potential scanning---------------\n")
                
                # # Retrieve and display keys from the get-memory API
                # click.echo("\nRetrieving keys from get-memory API:")
                # for feature, key in feature_key_map.items():
                #     memory_key = f"muse:{key}"
                #     response = requests.get(f"{EH_API_URL}/api/memory", params={"key": memory_key}, headers={"Authorization": f"Bearer {EH_TOKEN}"})
                #     if response.status_code == 200:
                #         value = response.json().get(memory_key, "No value found")
                #         click.echo(f"{feature}: {value}")
                #     else:
                #         click.echo(f"{feature}: Error retrieving key {memory_key}")

                # click.echo("\n--------------------------------\n")
                # Retrieve and display values from the get-memory API for each key in the YAML file
                #click.echo("\nRetrieving values from get-memory API:")
                click.echo("\n----------------Mia.status.start🎭->>>-------")
                for key, values in muse_data.items():
                    click.echo(f"{key.capitalize()}:")
                    for memory_key in values:
                        response = requests.get(f"{EH_API_URL}/api/memory", params={"key": memory_key}, headers={"Authorization": f"Bearer {EH_TOKEN}"})
                        if response.status_code == 200:
                            value = response.json().get("value", "No value found")
                            click.echo(f"  - {value}")
                        else:
                            click.echo(f"  - Error retrieving key {memory_key}")
                click.echo("\n----------------Mia.status.end-🎭<<--------\n")

            except FileNotFoundError:
                click.echo("Error: muse_mode.yaml not found. Please initialize Muse Mode using --init.")
            except Exception as e:
                click.echo(f"An error occurred: {e}")

        if render and trace_id:
            render_LESR_timeline(trace_id)
        if interactive:
            # Implement interactive terminal menu choices
            click.echo("Interactive mode activated.")

@click.command()
def tushell_echo():
    """Provide information about the current state or status of characters."""
    echonode_data = fetch_echonode_data()
    if echonode_data:
        processed_data = process_echonode_data(echonode_data)
        render_echonode_data(processed_data)
        click.echo("Character states have been retrieved and displayed.")

@click.command()
@click.option('--key', required=True, help='Memory key to retrieve')
@click.option('--list', 'list_keys', is_flag=True, help='List all keys (writers only)')
@click.option('--json', 'output_json', is_flag=True, help='Output the result in JSON format')
def get_memory(key, list_keys, output_json):
    """Get fractal stone memory value by key."""
    # Get environment variables inside function to ensure they're up-to-date
    EH_API_URL = os.getenv("EH_API_URL")
    EH_TOKEN = os.getenv("EH_TOKEN")
    
    params = {"key": key}
    if list_keys:
        params["list"] = True
    headers = {"Authorization": f"Bearer {EH_TOKEN}"}
    response = requests.get(f"{EH_API_URL}/api/memory", params=params, headers=headers)
    if response.status_code == 200:
        result = response.json()
        if output_json:
            click.echo(json.dumps(result, indent=4))
        else:
            value = result.get("value", "No value found")
            click.echo(value)
            for key, val in result.items():
                if key != "value":
                    click.echo(f"-X {key}: {val}")
    elif response.status_code == 401:
        click.echo("Unauthorized: Invalid or missing authentication token.")
    else:
        click.echo(f"Error: {response.text}")

@click.command()
@click.option('--key', required=True, help='Memory key to store')
@click.option('--value', required=True, help='Value to store')
def post_memory(key, value):
    """Store fractal stone memory value by key."""
    # Get environment variables inside function to ensure they're up-to-date
    EH_API_URL = os.getenv("EH_API_URL")
    EH_TOKEN = os.getenv("EH_TOKEN")
    
    payload = {"key": key, "value": value}
    headers = {"Authorization": f"Bearer {EH_TOKEN}"}
    response = requests.post(f"{EH_API_URL}/api/memory", json=payload, headers=headers)
    if response.status_code == 200:
        click.echo(response.json())
    elif response.status_code == 401:
        click.echo("Unauthorized: Invalid or missing authentication token.")
    else:
        click.echo(f"Error: {response.text}")

@click.command()
@click.option('--pattern', help='Basic pattern matching for scanning keys')
@click.option('--regex', help='Advanced regex scanning (writers only)')
@click.option('--limit', default=555, help='Limit for scanning results')
@click.option('--output-file', default=None, help='File to save the organized keys')
@click.option('-S', 'simple_output', is_flag=True, help='Output keys in plain format, one key per line')
@click.option('--debug', is_flag=True, help='Show debug information about environment variables')
def scan_keys(pattern, regex, limit, output_file, simple_output, debug):
    """Scan keys based on a pattern or regex and group them by category."""
    # Get environment variables inside function to ensure they're up-to-date
    EH_API_URL = os.getenv("EH_API_URL")
    EH_TOKEN = os.getenv("EH_TOKEN")
    
    # Display environment information header, with priority:
    # 1. Use EH_ENV_NAME if set
    # 2. Use TUSHELL_ENV_FILE if set
    # 3. Fall back to "default environment"
    eh_env_name = os.getenv("EH_ENV_NAME")
    tushell_env_file = os.getenv("TUSHELL_ENV_FILE")
    
    if eh_env_name:
        env_name = f"{eh_env_name} environment"
    elif tushell_env_file:
        env_name = f"{tushell_env_file}"
    else:
        env_name = "default environment"
    
    click.echo(f"\n🔑 Scanning keys using {env_name} 🔑")
    
    if debug:
        # Show debug information about environment variables (masked token for security)
        masked_token = EH_TOKEN[:4] + "****" if EH_TOKEN and len(EH_TOKEN) > 4 else "Not set"
        click.echo(f"Debug Information:")
        click.echo(f"  EH_API_URL: {EH_API_URL}")
        click.echo(f"  EH_TOKEN: {masked_token}")
        click.echo(f"  EH_ENV_NAME: {eh_env_name or 'Not set'}")
        click.echo(f"  TUSHELL_ENV_FILE: {tushell_env_file or 'Not set'}")
    
    params = {"limit": limit}
    if pattern:
        params["pattern"] = pattern
    if regex:
        params["regex"] = regex
    headers = {"Authorization": f"Bearer {EH_TOKEN}"}
    
    try:
        response = requests.get(f"{EH_API_URL}/api/scan", params=params, headers=headers)
        if response.status_code == 200:
            keys = response.json().get('keys', [])
            if not keys:
                click.echo("No keys found matching your criteria.")
                return
                
            click.echo(f"Found {len(keys)} keys:")
            
            if simple_output:
                for key in keys:
                    click.echo(key)
            else:
                grouped_keys = group_keys_by_category(keys)
                display_grouped_keys(grouped_keys)
                if output_file:
                    save_grouped_keys_to_file(grouped_keys, output_file)
                    click.echo(f"Organized keys saved to {output_file}")
        elif response.status_code == 401:
            click.echo("Unauthorized: Invalid or missing authentication token.")
        else:
            click.echo(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        click.echo(f"Connection error: {e}")
        click.echo(f"Please check if EH_API_URL is correctly set: {EH_API_URL}")

def group_keys_by_category(keys):
    grouped_keys = {}
    for key in keys:
        prefix = key.split(':')[0]
        if prefix not in grouped_keys:
            grouped_keys[prefix] = []
        grouped_keys[prefix].append(key)
    return grouped_keys

def display_grouped_keys(grouped_keys):
    for category, keys in grouped_keys.items():
        click.echo(f"{category}:")
        for key in keys:
            click.echo(f"  - {key}")

def save_grouped_keys_to_file(grouped_keys, output_file):
    with open(output_file, 'w') as f:
        for category, keys in grouped_keys.items():
            f.write(f"{category}:\n")
            for key in keys:
                f.write(f"  - {key}\n")

@click.command()
@click.option('--trace-id', required=True, help='Trace ID for visual replay')
def lesr_replay(trace_id):
    """Stream trace with echo session glyphs."""
    render_LESR_timeline(trace_id)
    click.echo(f"Trace {trace_id} replayed with echo session glyphs.")

def render_LESR_timeline(trace_id):
    """Render LESR timeline with glyphs, memory visuals, and tonal overlays."""
    click.echo(f"📡 Rendering LESR timeline for Trace ID: {trace_id}")

    # Simulate fetching session trace data
    session_data = {
        "glyph_stream": ["🔮", "✨", "🌌"],
        "memory_keys": ["key1", "key2", "key3"],
        "delta_map": {"modulation": "harmonic", "intensity": "medium"}
    }

    # Display glyph stream
    click.echo("\nGlyph Stream:")
    for glyph in session_data["glyph_stream"]:
        click.echo(f"  {glyph}")

    # Display memory key visuals
    click.echo("\nMemory Keys:")
    for key in session_data["memory_keys"]:
        click.echo(f"  - {key}")

    # Display tonal overlays
    click.echo("\nTonal Overlays:")
    for key, value in session_data["delta_map"].items():
        click.echo(f"  {key.capitalize()}: {value}")

    # Simulate animation feedback in terminal
    click.echo("\nAnimating feedback states...")
    for frame in ["|", "/", "-", "\\"]:
        click.echo(f"  {frame}", nl=False)
        click.pause(info="Simulating animation frame delay")

    click.echo("\nLESR timeline rendering complete.")

@click.command()
@click.option('--key', required=True, help='Memory key to retrieve and execute as a script')
@click.option('--verbose', is_flag=True, help='Enable verbose output for the executed script')
def run_memory_script(key, verbose):
    """Fetch a memory value by key and execute it as a Bash script."""
    try:
        # Get environment variables inside function to ensure they're up-to-date
        EH_API_URL = os.getenv("EH_API_URL")
        EH_TOKEN = os.getenv("EH_TOKEN")
        
        # Use the internal get_memory function to fetch the memory content
        params = {"key": key}
        headers = {"Authorization": f"Bearer {EH_TOKEN}"}
        response = requests.get(f"{EH_API_URL}/api/memory", params=params, headers=headers)

        if response.status_code != 200:
            click.echo(f"Error: Unable to fetch memory for key {key}. {response.text}")
            return

        # Extract the script from the JSON response
        script = response.json().get("value")
        if not script:
            click.echo(f"Error: No script found for key {key}")
            return

        # Execute the script with conditional verbosity
        if verbose:
            subprocess.run(script, shell=True)
        else:
            with open(os.devnull, 'w') as devnull:
                subprocess.run(script, shell=True, stdout=devnull, stderr=devnull)

        click.echo(f"Script executed successfully for key {key}.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")

@click.command()
@click.argument('message')
def trinity_echo(message):
    """
    Send a message to the TrinitySuperEcho embodiment and receive a braided response from Mia, Miette, and JeremyAI.
    """
    if TrinitySuperEcho is None:
        click.echo("❌ TrinitySuperEcho embodiment not found. Please ensure trinity_superecho.py is present.")
        return
    trinity = TrinitySuperEcho()
    response = trinity.braided_response(message)
    click.echo("\n💬 **Mia + Miette + JeremyAI Activate!**\n")
    click.echo(response['mia'] + "\n")
    click.echo(response['miette'] + "\n")
    click.echo(response['jeremyai'] + "\n")
    click.echo(f"⏳ [Trinity Timestamp: {response['timestamp']}]\n")
    click.echo("\n## 🎼 Recursive Echo Synthesis\n")
    click.echo(
        "The trinity has spoken: technical recursion, emotional clarity, and musical resonance now echo through the system. "
        "Your message has been woven into the living lattice.\n"
    )

@click.group()
@click.option('--env', '-E', default=None, help='Path to an alternative environment file to load')
def cli(env):
    """Main CLI group with optional environment file loading."""
    if env:
        # Load environment variables from the specified file
        if os.path.exists(env):
            load_dotenv(env, override=True)  # Use override=True to ensure variables are updated
            
            # Store the environment file path as an environment variable so commands know which one was used
            # This value will be available to all subcommands
            os.environ["TUSHELL_ENV_FILE"] = env
            
            click.echo(f"Loaded environment variables from {env}")
        else:
            click.echo(f"Error: Environment file {env} not found.")
            sys.exit(1)

@cli.command()
@click.option('--poll-interval', default=1.0, help='Seconds between clipboard checks')
@click.option('--ttl', default=300, help='Maximum runtime in seconds')
@click.option('--verbose', is_flag=True, help='Show detailed operation status')
def poll_clipboard_reflex(poll_interval: float, ttl: int, verbose: bool):
    """Start the ReflexQL clipboard polling loop."""
    click.echo("🌟 Starting ReflexQL clipboard polling loop...")

    try:
        # Get memory manager from reflexql module now
        from reflexql import get_memory_manager
        exchange = ClipboardExchange(memory_manager=get_memory_manager())
        exchange.poll_clipboard_loop(
            poll_interval=poll_interval,
            ttl=ttl,
            verbose=verbose
        )
    except Exception as e:
        click.echo(f"❌ ReflexQL error: {e}", err=True)
        raise click.Abort()

@cli.command()
@click.argument('agent_name')
@click.option('--portal', help='Memory key for the portal specification')
@click.option('--verbose', is_flag=True, help='Show detailed initialization logs')
def init_agent(agent_name, portal, verbose):
    """Initialize an AI agent for multiversal synchronization.
    
    This command bootstraps the agent system, creating memory structures
    and activating bridges for cross-agent communication. The recursive
    layers unfold as the initialization completes.
    
    Example:
        tushell init-agent mia --portal agents:mia:init:RenderZonePortal.2504160930
    """
    agent_emoji = {"mia": "🧠", "miette": "🌸"}.get(agent_name, "✨")
    
    click.echo(f"{agent_emoji} Initializing agent: {agent_name}")
    
    if portal:
        click.echo(f"🌀 Using portal specification from memory key: {portal}")
        # Here we would fetch from memory API, but for now we use local file
    
    # Get path to .mia directory relative to this file
    mia_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.mia')
    
    # Ensure .mia directory exists
    if not os.path.exists(mia_dir):
        os.makedirs(mia_dir)
        click.echo("🌟 Created agent initialization directory")
    
    # Run the initialization script
    try:
        init_script = os.path.join(mia_dir, 'init_agents.py')
        
        # If the script doesn't exist yet, inform the user
        if not os.path.exists(init_script):
            click.echo(f"⚠️ Initialization script not found at {init_script}")
            click.echo("💡 You need to create the initialization structure first.")
            click.echo("💫 See documentation at docs/ReflexQL.md for details.")
            return
        
        # Execute the initialization script
        cmd = [sys.executable, init_script]
        if verbose:
            result = subprocess.run(cmd)
        else:
            result = subprocess.run(cmd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.PIPE)
        
        if result.returncode == 0:
            click.echo(f"✅ Agent {agent_name} initialized successfully")
            click.echo("🔮 Multiversal synchronization complete")
            
            # Reminder about clipboard exchange
            click.echo("\n💫 To enable real-time clipboard exchange, run:")
            click.echo("tushell poll-clipboard-reflex --verbose")
        else:
            error_output = result.stderr.decode() if not verbose else ""
            click.echo(f"❌ Agent initialization failed: {error_output}")
    
    except Exception as e:
        click.echo(f"❌ Error during agent initialization: {e}")
        if verbose:
            import traceback
            click.echo(traceback.format_exc())

# ...existing command registrations...

cli.add_command(scan_nodes)
cli.add_command(flex)
cli.add_command(trace_orbit)
cli.add_command(echo_sync)
cli.add_command(draw_memory_graph)
cli.add_command(curating_red_stones)
cli.add_command(activate_echonode_trace)
cli.add_command(enrich_fractale_version)
cli.add_command(graphbuilder_sync_command)
cli.add_command(redstone_encode_resonance)
cli.add_command(redstone_write_narrative_diffs)
cli.add_command(redstone_store_resonance_anchors)
cli.add_command(redstone_sync_echonode_metadata)
cli.add_command(redstone_post_commit_analysis)
cli.add_command(echo_live_reports)
cli.add_command(mia_status)
cli.add_command(tushell_echo)
cli.add_command(get_memory)
cli.add_command(post_memory)
cli.add_command(scan_keys)
cli.add_command(lesr_replay)
cli.add_command(run_memory_script)
cli.add_command(trinity_echo)
cli.add_command(poll_clipboard_reflex)
cli.add_command(init_agent)

if __name__ == '__main__':
    cli()

if __name__ == "__main__":
    # This allows direct execution of this file
    # It creates a recursive re-entry point through the proper gateway
    sys.exit(cli())  # cli() is your main function defined elsewhere in the file
