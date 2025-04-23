# adjust MCP server

Adjust - MMP MCP server

## Quickstart

### Install

#### Claude Desktop

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development/Unpublished Servers Configuration</summary>

```
"mcpServers": {
  "feedmob-mcp-adjust": {
    "command": "uvx",
    "args": [
      "feedmob-mcp-adjust"
    ],
    "env": {
      "INTERNAL_API_KEY": "1da03eb2684d370814db28e456a4f968018bda7a2980f151c499a79b843983e3"
    }
  }
}
```

</details>

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).

You can launch the MCP Inspector via [`bun`](https://bun.sh/docs/cli/install) with this command:

```bash
bun x @modelcontextprotocol/inspector uv --directory ./ run adjust -e INTERNAL_API_KEY=your_token_here
```

Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
