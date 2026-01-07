# Claude Code 系统状态

## 版本信息
- **Claude Code**: v2.0.71
- **安装方式**: VSCode Extension / CLI

## MCP 服务器 (5个已连接 ✅)

| 服务器 | 状态 | 命令 |
|--------|------|------|
| `context7` | ✓ Connected | `npx -y @upstash/context7-mcp` |
| `serena` | ✓ Connected | `uvx serena start-mcp-server` |
| `chrome-devtools` | ✓ Connected | `npx -y chrome-devtools-mcp@latest` |
| `playwright` | ✓ Connected | `npx -y @playwright/mcp@latest` |
| `sequential-thinking` | ✓ Connected | `npx -y @modelcontextprotocol/server-sequential-thinking` |

## SuperClaude Framework (v4.1.7)

位置: `~/.claude/commands/sc/`

### 27个 `/sc:` 命令

**核心开发**:
- `/sc:implement` - 功能实现
- `/sc:test` - 测试执行
- `/sc:analyze` - 代码分析
- `/sc:build` - 构建项目
- `/sc:refactor` - 代码重构
- `/sc:design` - 架构设计

**研究与文档**:
- `/sc:research` - 深度网络研究
- `/sc:document` - 文档生成
- `/sc:index-repo` - 仓库索引
- `/sc:explain` - 代码解释

**任务管理**:
- `/sc:task` - 复杂任务执行
- `/sc:pm` - 项目管理
- `/sc:workflow` - 生成工作流
- `/sc:agent` - 启动专用AI代理

**其他**:
- `/sc:git` - Git操作
- `/sc:cleanup` - 代码清理
- `/sc:brainstorm` - 需求发现
- `/sc:troubleshoot` - 问题诊断
- `/sc:estimate` - 开发评估
- `/sc:reflect` - 任务反思
- `/sc:improve` - 代码改进
- `/sc:load` - 会话加载
- `/sc:save` - 会话保存
- `/sc:learn-path` - 学习路径
- `/sc:spec-panel` - 规格评审
- `/sc:business-panel` - 业务分析
- `/sc:select-tool` - 工具选择
- `/sc:recommend` - 命令推荐
- `/sc:index` - 知识库生成
- `/sc:help` - 显示帮助

## VSCode 设置

```json
{
  "claudeCode.preferredLocation": "panel",
  "claudeCode.disableLoginPrompt": true,
  "claudeCodeChat.thinking.intensity": "ultrathink"
}
```

## 项目权限配置

位置: `.claude/settings.local.json`

```json
{
  "permissions": {
    "allow": [
      "Skill(sc:*)",
      "Task:*",
      "Bash(python, git, curl, poetry, conda, npm, ...)",
      "mcp__notion__*",
      "mcp__4_5v_mcp__*",
      "mcp__web_reader__*"
    ]
  },
  "enableAllProjectMcpServers": true
}
```

## 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                    VSCode Extension                         │
│                  Claude Code v2.0.71                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Layer                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐   │
│  │ serena      │ │ playwright  │ │ chrome-devtools     │   │
│  │ (semantic)  │ │ (browser)   │ │ (browser testing)   │   │
│  └─────────────┘ └─────────────┘ └─────────────────────┘   │
│  ┌─────────────┐ ┌─────────────┐                           │
│  │ context7    │ │ sequential  │                           │
│  │ (docs)      │ │ -thinking   │                           │
│  └─────────────┘ └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  SuperClaude Framework                      │
│                     v4.1.7                                  │
│                   (27 /sc: commands)                        │
└─────────────────────────────────────────────────────────────┘
```

## 快速命令

```bash
# 查看MCP服务器状态
claude mcp list

# 使用SuperClaude命令
/sc:help

# 继续之前的会话
claude --continue

# 非交互式输出
claude -p "your prompt"
```

## 配置文件位置

| 配置 | 位置 |
|------|------|
| Claude Code设置 | `~/Library/Application Support/Code/User/settings.json` |
| SuperClaude命令 | `~/.claude/commands/sc/` |
| 项目权限 | `.claude/settings.local.json` |
| MCP配置 | 通过Trae CN管理 |

---
*生成日期: 2025-01-05*
