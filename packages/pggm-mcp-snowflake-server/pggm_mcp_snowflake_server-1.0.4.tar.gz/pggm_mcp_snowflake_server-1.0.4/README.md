# PGGM MCP Snowflake Server

A customized Model Context Protocol (MCP) server for Snowflake integration, allowing AI assistants to interact with Snowflake databases securely and efficiently.

## Features

- Connect to Snowflake databases and execute queries
- Support for various SQL operations and schema exploration
- Data insights collection and memoization
- SQL write operation detection for enhanced security
- Customizable database, schema, and table filtering
- Support for authentication through environment variables or command-line arguments

## Installation

### Using pip

Option 1: Install  
Install this in your user site-packages so that it works with all your projects, run a powershell window and:

```bash
C:\Users\User> pip install --user pggm-mcp-snowflake-server
```
This will install the package in: C:\Users\USER\AppData\Roaming\Python\Python311\site-packages
with the .exe in your C:\Users\USER\AppData\Roaming\Python\Python311\Scripts
You might have to add this to your PATH:
1) windows search: Edit the System Environment Variables
2) Navigate: advanced / Environment Variables / select: PATH / Edit.. 
3) New: C:\Users\USER\AppData\Roaming\Python\Python311

Option 2: Install in your project venv

```bash
pip install pggm-mcp-snowflake-server
```

### Inside VS-Code

Add the following to your settings.json in vs-code (F1 + Preferences: Open User Settings(JSON))

```bash
    "workbench.settings.applyToAllProfiles": [
        "chat.agent.enabled"
    ],
    "github.copilot.chat.agent.thinkingTool": true,
    "mcp": {

        "inputs": [],
        "servers": {
           "snowflake_local": {
            "command": "C:\\Users\\SNST\\AppData\\Roaming\\Python\\Python311\\Scripts\\pggm_mcp_snowflake_server.exe",
            # In case you chose to install in your venv, replace above with the following:
            # "command": "{project_source}\\venv\\Scripts\\pggm_mcp_snowflake_server.exe",     
            "args": [
                    "--account",
                    "pggm-vb.privatelink",
                    "--warehouse",
                    "{warehouse}",
                    "--authenticator",
                    "externalbrowser",
                    "--user",
                    "{user_email}",
                    "--role",
                    "PUBLIC",
                    "--database",
                    "SNOWFLAKE",
                    "--schema",
                    "INFORMATION_SCHEMA",
                    # Optionally: "--allow_write"
                ]
            }
        }
    },

```
## Usage

In VS Code you need to have Agent mode enabled.
You can see which tools the AI has access to by navigating towards its chat window, and selecting the Tools icon, or pressing Ctrl+Shift+/ inside its chat window. 

### Tools Available

The pggm_mcp_snowflake_server provides the following tools for copilot:

- `list_databases` - List all available databases in Snowflake
- `list_schemas` - List all schemas in a database
- `list_tables` - List all tables in a specific database and schema
- `describe_table` - Get the schema information for a specific table
- `read_query` - Execute a SELECT query
- `append_insight` - Add a data insight to the memo
- `write_query` - Execute an INSERT, UPDATE, or DELETE query (if --allow_write is enabled)
- `create_table` - Create a new table in the Snowflake database (if --allow_write is enabled)

## Security

By default, the server runs in read-only mode. To enable write operations, you must explicitly pass the `--allow_write` flag.

The server uses SQL parsing to detect and prevent write operations in `read_query` calls, ensuring only approved write operations can be executed.
