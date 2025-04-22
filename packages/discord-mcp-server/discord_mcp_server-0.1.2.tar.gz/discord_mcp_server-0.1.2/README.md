# Discord MCP Server

一个基于MCP的Discord webhook服务器。

## 安装

```bash
uv pip install discord-mcp-server
```

## 使用方法

### 1. 环境变量配置

设置Discord webhook URL环境变量：
```bash
# Windows PowerShell
$env:DISCORD_WEBHOOK_URL="your-discord-webhook-url"

# Linux/Mac
export DISCORD_WEBHOOK_URL="your-discord-webhook-url"
```

### 2. 运行服务器

```bash
# 使用uvx
uvx discord-mcp-server

# 使用完整路径
.\.venv\Scripts\discord-mcp-server.exe
```

### 3. Cursor配置

#### 3.1 Webhook配置
1. 打开Cursor设置
2. 搜索"Discord"
3. 在Webhook URL字段中输入你的Discord webhook URL
4. 保存设置

#### 3.2 MCP配置
在Cursor的MCP配置文件中添加：
```json
{
  "name": "discord-mcp-server",
  "type": "uvx",
  "entry_point": "discord_mcp_server:main",
  "config": {
    "webhook_url": "your-discord-webhook-url"
  }
}
```

### 4. CLine配置

#### 4.1 Webhook配置
在CLine配置文件中添加：
```yaml
discord:
  webhook_url: "your-discord-webhook-url"
```

#### 4.2 MCP配置
在CLine的MCP配置文件中添加：
```json
{
  "name": "discord-mcp-server",
  "type": "uvx",
  "entry_point": "discord_mcp_server:main",
  "config": {
    "webhook_url": "your-discord-webhook-url"
  }
}
```

## 环境变量

- `DISCORD_WEBHOOK_URL`: Discord webhook URL（必需）

## 功能

- 支持发送文本消息
- 支持发送Markdown格式消息
- 通过MCP提供API接口
- 支持Cursor和CLine集成
- 支持异步操作
- 支持错误处理

## 注意事项

1. 确保使用Python 3.10或更高版本
2. 确保已安装所有依赖项
3. 确保Discord webhook URL正确配置
4. 如果使用虚拟环境，确保已激活
5. MCP配置中的`webhook_url`优先级高于环境变量
6. 支持的消息类型：
   - text: 普通文本消息
   - markdown: Markdown格式消息
