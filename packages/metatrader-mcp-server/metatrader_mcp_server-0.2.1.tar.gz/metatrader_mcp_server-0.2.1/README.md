# MetaTrader MCP Server

This is a Model Context Protocol (MCP) server built with Python to enable AI LLMs to trade using MetaTrader platform.

![MetaTrader MCP Server](https://yvkbpmmzjmfqjxusmyop.supabase.co/storage/v1/object/public/github//metatrader-mcp-server-1.png)

## Updates

- April 23, 2025: Published to PyPi (0.2.0) ✌🏻✌🏻✌🏻
- April 16, 2025: We have our first minor version release (0.1.0) 🎉🎉🎉

## Installation Guide

Make sure you have Python version 3.10+ and MetaTrader 5 terminal installed in your workspace. Then install the package:

```bash
pip install metatrader-mcp-server
```

## Claude Desktop Integration

To use this package to enable trading operations via Claude Desktop app, please add this into your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "metatrader": {
      "command": "metatrader-mcp-server",
      "args": [
        "--login",    "<YOUR_MT5_LOGIN>",
        "--password", "<YOUR_MT5_PASSWORD>",
        "--server",   "<YOUR_MT5_SERVER>"
      ]
    }
  }
}
```

## Project Roadmap

For full version checklist, see [version-checklist.md](docs/roadmap/version-checklist.md).

| Task | Status | Done | Tested |
|------|--------|------|--------|
| Connect to MetaTrader 5 terminal | Finished | ✅ | ✅ |
| Develop MetaTrader client module | Finished | ✅ | ✅ |
| Develop MCP Server module | Finished | ✅ | ✅ |
| Implement MCP tools | Finished | ✅ | ✅ |
| Publish to PyPi | Finished | ✅ | ✅ |
| Claude Desktop integration | Finished | ✅ | ✅ |
| Open WebUI integration | - | - | - |

## Developer Documentation

For developers, see [Developer's Documentation](docs/README.md).