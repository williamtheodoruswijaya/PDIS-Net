# MCP Setup

MCP means Model Context Protocol. It lets compatible AI tools connect to external context providers such as filesystem or git servers.

## Files

Root template:

```text
mcp.json
```

Codex mirror:

```text
.codex/mcp.json
```

Both currently define:

- filesystem server scoped to `.`
- git server scoped to `.`

## Template

```json
{
  "mcpServers": {
    "semantix-filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
      "env": {}
    },
    "semantix-git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "."],
      "env": {}
    }
  }
}
```

## Requirements

Depending on your MCP client, this may require:

- Node.js and `npx`
- Python tooling and `uvx`
- MCP client support for local config files

## Safety

Keep MCP scope narrow:

- filesystem is scoped to the repo
- git is scoped to the repo
- no secrets are placed in the config

Do not add tokens directly to `mcp.json`.

