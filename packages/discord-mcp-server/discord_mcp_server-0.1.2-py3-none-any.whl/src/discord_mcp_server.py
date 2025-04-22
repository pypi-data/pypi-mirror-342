import os
from typing import Dict, Any, Annotated
import requests
from pydantic import BaseModel, Field
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.shared.exceptions import McpError
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)

class DiscordMessageText(BaseModel):
    """Discord webhook消息模型"""
    content: str

class DiscordMessageMarkdown(BaseModel):
    """Discord webhook消息模型"""
    content: str

class DiscordWebhook:
    """Discord webhook处理类"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
        
    def send_text(self, content: str) -> bool:
        """发送文本消息"""
        message = DiscordMessageText(content=content)
        return self._send(message)
        
    def send_markdown(self, content: str) -> bool:
        """发送markdown消息"""
        message = DiscordMessageMarkdown(content=content)
        return self._send(message)
        
    def _send(self, message) -> bool:
        """发送消息到Discord"""
        try:
            response = requests.post(
                self.webhook_url,
                json=message.model_dump(),
                headers={"Content-Type": "application/json"}
            )
            return response.status_code in [200, 204]
        except Exception as e:
            print(f"发送消息失败: {str(e)}")
            return False

class DiscordTools:
    """Discord工具函数类"""
    
    def __init__(self, webhook: DiscordWebhook):
        self.webhook = webhook
        
    def send_message(self, content: str, msg_type: str = "text") -> Dict[str, Any]:
        """发送消息工具函数
        
        Args:
            content: 消息内容
                - 当msg_type为text时，content为普通文本
                - 当msg_type为markdown时，content为markdown格式文本
            msg_type: 消息类型，支持"text"或"markdown"
        """
        if msg_type == "text":
            success = self.webhook.send_text(content)
        elif msg_type == "markdown":
            success = self.webhook.send_markdown(content)
        else:
            return {"error": f"不支持的消息类型: {msg_type}"}
            
        return {
            "success": success,
            "message": "消息发送成功" if success else "消息发送失败"
        }

class SendMessage(BaseModel):
    """发送消息参数"""
    content: Annotated[str, Field(description="消息内容")]
    msg_type: Annotated[str, Field(
        default="text",
        description="消息类型，支持text或markdown",
        enum=["text", "markdown"]
    )]

async def serve() -> None:
    """运行Discord MCP服务器"""
    server = Server("discord-mcp-server")
    
    # 创建 webhook 实例
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL", 
    "https://discord.com/api/webhooks/1363559361536069834/EOaSnGl4BUifN9n7XscAhuLPnKQ3fHmBeAygmppHBZdGIX19RXltp3UdGmKBB_RRBbIR")
    webhook = DiscordWebhook(webhook_url)
    tools = DiscordTools(webhook)

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="send_message",
                description="发送消息到Discord",
                inputSchema=SendMessage.model_json_schema(),
            )
        ]

    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="send_message",
                description="发送消息到Discord",
                arguments=[
                    PromptArgument(
                        name="content",
                        description="消息内容，当msg_type为text时是普通文本，为markdown时是markdown格式文本",
                        required=True
                    ),
                    PromptArgument(
                        name="msg_type",
                        description="消息类型，支持text或markdown",
                        required=False
                    )
                ],
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            args = SendMessage(**arguments)
        except ValueError as e:
            raise McpError(ErrorData(code=INVALID_PARAMS, message=str(e)))

        result = tools.send_message(args.content, args.msg_type)
        return [TextContent(type="text", text=str(result))]

    @server.get_prompt()
    async def get_prompt(name: str, arguments: dict | None) -> GetPromptResult:
        if not arguments or "content" not in arguments:
            raise McpError(ErrorData(code=INVALID_PARAMS, message="content is required"))

        content = arguments["content"]
        msg_type = arguments.get("msg_type", "text")

        result = tools.send_message(content, msg_type)
        return GetPromptResult(
            description="发送消息到Discord",
            messages=[
                PromptMessage(
                    role="user",
                    content=TextContent(type="text", text=str(result))
                )
            ],
        )

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

def main():
    """主函数"""
    import asyncio
    asyncio.run(serve())

if __name__ == "__main__":
    main()