# Feedmob MCP Server for Adjust

Feedmob MCP Server for Adjust - MMP MCP server

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>

```
{
  "mcpServers": {
    "feedmob-mcp-adjust": {
      "command": "uvx",
      "args": [
        "feedmob-mcp-adjust"
      ],
      "env": {
        "INTERNAL_API_KEY": "xxx"
      }
    }
  }
}

```

</details>

### Debugging

```shell
npx @modelcontextprotocol/inspector uv --directory ./ run feedmob-mcp-adjust -e INTERNAL_API_KEY=xxx
```