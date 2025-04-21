import os
from typing import Dict, Any
import requests
from pydantic import BaseModel
from mcp.server.fastmcp import FastMCP

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
        """发送消息工具函数"""
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

# 创建 MCP 服务器实例
mcp = FastMCP("Discord MCP Server")

# 创建 webhook 实例
webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
# webhook_url = os.getenv("DISCORD_WEBHOOK_URL", 
# "https://discord.com/api/webhooks/1363559361536069834/EOaSnGl4BUifN9n7XscAhuLPnKQ3fHmBeAygmppHBZdGIX19RXltp3UdGmKBB_RRBbIR")
webhook = DiscordWebhook(webhook_url)
tools = DiscordTools(webhook)

# 注册工具函数
@mcp.tool()
def send_message(content: str, msg_type: str = "text") -> Dict[str, Any]:
    """发送消息到Discord"""
    return tools.send_message(content, msg_type)

def main():
    """主函数"""
    mcp.run()

if __name__ == "__main__":
    main()