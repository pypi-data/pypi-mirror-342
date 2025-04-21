# 导入必要的模块和类型
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import asyncio
import sys


# 创建标准输入输出服务器参数配置
# 这些参数用于启动和管理与服务器的通信
server_params = StdioServerParameters(
    command="python",  # 指定要执行的Python解释器
    args=["server.py"],  # 传递给解释器的命令行参数
    env=None,  # 可选的环境变量设置
)

# 定义采样回调函数
# 这个函数用于处理模型生成的消息
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    # 返回一个固定的响应消息
    return types.CreateMessageResult(
        role="assistant",  # 消息角色为助手
        content=types.TextContent(
            type="text",  # 内容类型为文本
            text="Hello, world! from model",  # 消息内容
        ),
        model="gpt-3.5-turbo",  # 使用的模型名称
        stopReason="endTurn",  # 停止原因
    )

# 主运行函数
async def run():
    try:
        print("正在启动客户端...")
        # 使用上下文管理器创建标准输入输出客户端连接
        async with stdio_client(server_params) as (read, write):
            print("已建立连接")
            # 创建客户端会话，并传入采样回调函数
            async with ClientSession(
                read, write, sampling_callback=handle_sampling_message
            ) as session:
                print("正在初始化会话...")
                # 初始化会话连接
                await session.initialize()

                # # 列出所有可用的提示词模板
                # prompts = await session.list_prompts()

                # # 获取特定提示词模板，并传入参数
                # prompt = await session.get_prompt(
                #     "example-prompt", arguments={"arg1": "value"}
                # )

                # # 列出所有可用的资源
                # resources = await session.list_resources()

                # 列出所有可用的工具
                print("正在获取工具列表...")
                tools = await session.list_tools()
                print("可用的工具:", tools)

                # 调用特定工具并传入参数
                print("正在调用工具...")
                result = await session.call_tool(
                    "send_message", 
                    arguments={"msg_type": 'markdown', 
                               "content": '#Hello, world! from client'})
                print("工具调用结果:", result)

    except Exception as e:
        print(f"发生错误: {str(e)}", file=sys.stderr)
        raise

# 程序入口点
if __name__ == "__main__":
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {str(e)}", file=sys.stderr)