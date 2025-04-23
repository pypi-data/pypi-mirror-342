# Nacos Config MCP

A Microservice Client Protocol (MCP) server for managing Nacos configuration servers.

This implementation uses the official [nacos-sdk-python](https://github.com/nacos-group/nacos-sdk-python) library.

## Installation

```bash
pip install nacos-config-mcp
```

## Usage

Run the server:

```bash
nacos-config-mcp
```

## Features

The MCP server provides tools for interacting with Nacos configuration servers:

### Configuration Management
- **get_config**: Retrieve configuration values
- **publish_config**: Create or update configuration (use with caution)
- **remove_config**: Delete configuration (use with extreme caution)

### Namespace Operations
- **list_namespaces**: List all available namespaces

### System
- **just_get_version**: Get the version of the MCP server

## Important Notes

Some operations can potentially disrupt running services:
- Creating, updating, or deleting configurations can impact services that depend on them
- Always use appropriate caution when modifying production configurations

## License

MIT 