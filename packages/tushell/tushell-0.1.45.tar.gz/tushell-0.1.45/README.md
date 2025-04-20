# tushell

The Data Diver's best Intelligent and Narrative Command-Line Tooling you will have ever had.

## Description

`tushell` is a CLI-native, recursive DevOps & narrative command tooling package designed to provide intelligent and narrative libraries and command-line tooling for data divers.

## Installation

To install `tushell`, use pip:

```bash
pip install tushell
```

## Usage

Here are some usage examples for each CLI command:

* `scan-nodes`: Simulate scanning and listing nodes in the system.

```bash
tushell scan-nodes
```

* `flex`: Demonstrate flexible orchestration of tasks.

```bash
tushell flex
```

* `trace-orbit`: Trace and visualize the orbit of data or processes.

```bash
tushell trace-orbit
```

* `echo-sync`: Synchronize data or processes across nodes.

```bash
tushell echo-sync
```

* `draw-memory-graph`: Print an ASCII-rendered graph of the memory keys and Arc structure.

```bash
tushell draw-memory-graph
```

* `graphbuilder-sync-command`: Execute GraphBuilderSync operations.

```bash
tushell graphbuilder-sync-command --api-url <API_URL> --token <TOKEN> --action <ACTION> [--node-id <NODE_ID>] [--node-data <NODE_DATA>] [--narrative]
```

* `redstone-encode-resonance`: Encode recursive resonance into commits.
  ```bash
  tushell redstone-encode-resonance
  ```

* `redstone-write-narrative-diffs`: Write narrative diffs to commit messages.
  ```bash
  tushell redstone-write-narrative-diffs
  ```

* `redstone-store-resonance-anchors`: Store resonance anchors in `.redstone.json`.
  ```bash
  tushell redstone-store-resonance-anchors
  ```

* `redstone-sync-echonode-metadata`: Sync with EchoNode metadata.
  ```bash
  tushell redstone-sync-echonode-metadata
  ```

* `redstone-post-commit-analysis`: Support `RedStone score` metadata field for post-commit analysis.
  ```bash
  tushell redstone-post-commit-analysis
  ```

## Upcoming Features

The `EchoNexus` subpackage is an upcoming feature that will serve as an anchor for recursive orchestration modules. Stay tuned for more updates!

For more information, please refer to the documentation.

### 🧠 Narrative Lattices – Recursive CLI Tools

#### `curating-red-stones`
* **Command Name**: `curating-red-stones`
* **Narrative Purpose**: Visualize and structure Red Stone metadata connections
* **Usage**:  
  ```bash
  tushell curating-red-stones
  ```
* **Output**: Displays the structure and connections of Red Stone metadata.

#### `activate-echonode-trace`
* **Command Name**: `activate-echonode-trace`
* **Narrative Purpose**: Activate and trace EchoNode sessions
* **Usage**:  
  ```bash
  tushell activate-echonode-trace
  ```
* **Output**: Logs the activation and tracing of EchoNode sessions.

#### `enrich-fractale-version`
* **Command Name**: `enrich-fractale-version`
* **Narrative Purpose**: Enhance and enrich the Fractale 001 version
* **Usage**:  
  ```bash
  tushell enrich-fractale-version
  ```
* **Output**: Visualizes the enhancements and enrichments made to Fractale 001.

#### `graphbuilder-sync-command`
* **Command Name**: `graphbuilder-sync-command`
* **Narrative Purpose**: Execute GraphBuilderSync operations
* **Usage**:  
  ```bash
  tushell graphbuilder-sync-command --api-url <API_URL> --token <TOKEN> --action <ACTION> [--node-id <NODE_ID>] [--node-data <NODE_DATA>] [--narrative]
  ```
* **Output**: Executes the specified action (push or pull) for GraphBuilderSync operations, optionally with narrative context.

#### `redstone-encode-resonance`
* **Command Name**: `redstone-encode-resonance`
* **Narrative Purpose**: Encode recursive resonance into commits
* **Usage**:  
  ```bash
  tushell redstone-encode-resonance
  ```
* **Output**: Encodes recursive resonance into commits.

#### `redstone-write-narrative-diffs`
* **Command Name**: `redstone-write-narrative-diffs`
* **Narrative Purpose**: Write narrative diffs to commit messages
* **Usage**:  
  ```bash
  tushell redstone-write-narrative-diffs
  ```
* **Output**: Writes narrative diffs to commit messages.

#### `redstone-store-resonance-anchors`
* **Command Name**: `redstone-store-resonance-anchors`
* **Narrative Purpose**: Store resonance anchors in `.redstone.json`
* **Usage**:  
  ```bash
  tushell redstone-store-resonance-anchors
  ```
* **Output**: Stores resonance anchors in `.redstone.json`.

#### `redstone-sync-echonode-metadata`
* **Command Name**: `redstone-sync-echonode-metadata`
* **Narrative Purpose**: Sync with EchoNode metadata
* **Usage**:  
  ```bash
  tushell redstone-sync-echonode-metadata
  ```
* **Output**: Syncs with EchoNode metadata.

#### `redstone-post-commit-analysis`
* **Command Name**: `redstone-post-commit-analysis`
* **Narrative Purpose**: Support `RedStone score` metadata field for post-commit analysis
* **Usage**:  
  ```bash
  tushell redstone-post-commit-analysis
  ```
* **Output**: Supports `RedStone score` metadata field for post-commit analysis.




-----
FUTURE CLI
-----



## TUSHELL CLI for Dummies

Welcome to TUSHELL! This guide will help you get started with the basic commands.

### Installation

First, make sure you have Python installed. Then, you can install TUSHELL using pip:

```bash
pip install tushell
```

### Basic Usage

TUSHELL provides several commands to interact with the system. Here are a few essential ones:

### **Scanning Nodes:**
```bash
tushell scan-nodes
```
This command simulates scanning and listing nodes in the system.

### **Drawing Memory Graph:**
```bash
tushell draw-memory-graph
```
This command prints an ASCII-rendered graph of the memory keys and Arc structure.

### **Curating Red Stones:**
```bash
tushell curating-red-stones
```
This command visualizes and structures Red Stone metadata connections.

### Getting Help

For more information on any command, you can use the `--help` option:
```bash
tushell curating-red-stones --help
```

## TUSHELL CLI for Advanced Terminal Masters

Welcome, seasoned user! This section dives into the advanced features of TUSHELL.

### GraphBuilderSync

Synchronize data or processes across nodes with advanced options:

```bash
tushell graphbuilder-sync-command --api-url <API_URL> --token <TOKEN> --node-id <NODE_ID> --node-data <NODE_DATA> --action <push|pull> --narrative
```

* `--api-url`: API URL for GraphBuilderSync (required).
* `--token`: Authorization token for GraphBuilderSync (required).
* `--node-id`: Node ID for GraphBuilderSync.
* `--node-data`: Node data for GraphBuilderSync.
* `--action`: Action for GraphBuilderSync (`push` or `pull`, default: `pull`).
* `--narrative`: Narrative context for GraphBuilderSync.

### RedStone Writer

### **Encode Resonance:**
```bash
tushell redstone-encode-resonance --repo-path <REPO_PATH> --commit-message <COMMIT_MESSAGE>
```

### **Write Narrative Diffs:**
```bash
tushell redstone-write-narrative-diffs --repo-path <REPO_PATH> --commit-message <COMMIT_MESSAGE> --diffs <DIFFS>
```

### **Store Resonance Anchors:**
```bash
tushell redstone-store-resonance-anchors --repo-path <REPO_PATH> --anchors <ANCHORS>
```

### **Sync EchoNode Metadata:**
```bash
tushell redstone-sync-echonode-metadata --repo-path <REPO_PATH> --echonode-metadata <ECHONODE_METADATA>
```

### **Post-Commit Analysis:**
```bash
tushell redstone-post-commit-analysis --repo-path <REPO_PATH> --redstone-score <REDSTONE_SCORE>
```

### Advanced Options

Many commands support `--verbose` and `--dry-run` options for detailed output and testing without committing changes:
```bash
tushell curating-red-stones --verbose --dry-run
```
