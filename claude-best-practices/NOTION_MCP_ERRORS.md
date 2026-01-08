# Notion MCP 最佳实践与常见错误

> **使用指南**：本文档记录 Notion MCP 的常见错误模式和解决方案，用于设计自动化工作流时参考。

---

## 📋 快速参考

### Block 类型映射

| 概念 | Notion 类型 | type 值 |
|------|-------------|---------|
| 一级标题 | heading_1 | `heading_1` |
| 二级标题 | heading_2 | `heading_2` |
| 三级标题 | heading_3 | `heading_3` |
| 段落 | paragraph | `paragraph` |
| 无序列表 | bulleted_list_item | `bulleted_list_item` |
| 有序列表 | numbered_list_item | `numbered_list_item` |
| 折叠 | toggle | `toggle` |

### 常见错误与解决方案

#### ❌ 错误 1: 链接格式错误

**错误代码**:
```json
{
  "text": {"content": "Oxen.ai", "link": "https://..."}
}
```

**错误信息**:
```
body.children[1].bulleted_list_item.rich_text[1].text.link should be an object
```

**✅ 正确格式**:
```json
{
  "text": {
    "content": "Oxen.ai",
    "link": {"url": "https://..."}
  }
}
```

---

#### ❌ 错误 2: `after` 参数引用已删除的 block

**错误代码**:
```python
mcp__notion__API-patch-block-children(
    after="2da68312-fbf9-81f8...",  # 此 block 已被删除
    block_id="page_id",
    children=[...]
)
```

**错误信息**:
```
Block ID to append children after is not parented by page_id
```

**✅ 解决方案**:
1. 先调用 `get-block-children` 获取当前状态
2. 使用有效的 block ID
3. 避免使用已删除的 block 作为锚点

---

#### ❌ 错误 3: `child_page` 不支持

**错误代码**:
```json
{
  "child_page": {"title": "Week 3: MCP Server 开发"},
  "type": "child_page"
}
```

**错误信息**:
```
body.children[1].embed should be defined, instead was `undefined`.
```

**✅ 解决方案**:
使用 `post-page` 创建子页面，而不是 `patch-block-children`

---

## 🎯 最佳实践

### 1. 创建可折叠标题

```json
{
  "heading_2": {
    "is_toggleable": true,
    "rich_text": [
      {"text": {"content": "🔧 工具参考"}, "type": "text"}
    ]
  },
  "type": "heading_2"
}
```

### 2. 创建带链接的文本

```json
{
  "paragraph": {
    "rich_text": [
      {
        "text": {"content": "前缀文本"},
        "type": "text"
      },
      {
        "text": {
          "content": "链接文本",
          "link": {"url": "https://example.com"}
        },
        "annotations": {"underline": true},
        "type": "text"
      }
    ]
  },
  "type": "paragraph"
}
```

### 3. 推荐工作流

```
1. get-block-children(page_id) → 获取当前结构
2. delete-a-block(block_id) → 删除不需要的
3. patch-block-children(block_id, children) → 批量添加新内容
4. 如果需要更新：delete + create（不是 update）
```

### 4. 权限确认

**重要**: VSCode 扩展有独立的安全层，`.claude/settings.local.json` 无法绕过用户确认。

**建议**:
- 接受现状，每次操作手动确认
- 或者设计 Skill/Subagent 批量处理，减少确认次数

---

## 🚀 Subagent/Skill 设计建议

### 方案 A: 批量操作 Skill

**输入**: 操作列表
```yaml
operations:
  - delete: ["block_id_1", "block_id_2"]
  - create:
      - type: "heading_2"
        content: "🔧 工具参考"
        toggleable: true
```

**输出**: 执行结果

**优点**: 减少确认次数到 1-2 次
**缺点**: 需要提前规划好所有操作

---

### 方案 B: 模板渲染

**输入**: 模板定义
```yaml
structure:
  - heading: "🏃 进行中项目"
    toggleable: true
    children:
      - paragraph: "Week 3: MCP Server 开发"
      - bulleted_list: "📖 理论: xxx"
```

**输出**: Notion API 调用序列

**优点**: 声明式，易维护
**缺点**: 需要设计模板语法

---

## 📁 关键文件

| 文件 | 用途 |
|------|------|
| `.claude/settings.local.json` | 权限配置 |
| `~/.cursor/mcp.json` | MCP 服务器配置 |
| `/Users/David/.claude/plans/*.md` | 计划文件 |

---

## ⚠️ 已知限制

1. **权限确认绕过**: 暂无解决方案，需手动确认
2. **子页面创建**: `patch-block-children` 不支持，需用 `post-page`
3. **block 更新**: `update-a-block` 格式复杂，建议删除重建

---

**最后更新**: 2026-01-08
**状态**: 活跃维护
