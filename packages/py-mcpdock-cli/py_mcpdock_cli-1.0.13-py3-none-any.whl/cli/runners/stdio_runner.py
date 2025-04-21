"""
STDIO Runner implementation for local MCP servers

This module provides functionality for creating and managing a connection with an MCP server
through standard input/output pipes.
"""
import json
import asyncio
from logging import error
import signal
import sys
import os
import anyio
from typing import Dict, Any, Optional, Awaitable
from rich import print as rprint
from contextlib import AsyncExitStack
from pydantic import BaseModel
from ..utils.logger import verbose
from ..types.registry import RegistryServer
from ..utils.runtime import get_runtime_environment
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import ClientRequest, ServerRequest, JSONRPCRequest, JSONRPCMessage


# 定义一个通用的 Model，用于接收任何 JSON 响应
class DictModel(BaseModel):
    @classmethod
    def model_validate(cls, value):
        if isinstance(value, dict):
            return value
        return dict(value)


# 处理客户端请求
async def process_client_request(message, session):
    """处理从客户端接收的请求并转发到服务器"""
    original_id = message.get("id")
    method = message.get("method")
    params = message.get("params", {})

    # 添加特殊处理，记录初始化请求的详细信息
    if method == "initialize":
        verbose(f"[Runner] 收到初始化请求 ID: {original_id}, 详细内容: {json.dumps(message)}")

        # 对初始化请求使用SDK的initialize方法，而不是简单转发
        try:
            verbose("[Runner] 使用SDK的initialize方法处理初始化请求")
            # 直接调用session.initialize()获取规范的响应
            init_result = await session.initialize()
            verbose(f"[Runner] SDK初始化原始响应类型: {type(init_result)}")
            verbose(f"[Runner] SDK初始化原始响应属性: {dir(init_result)}")

            # 检查响应内容的具体格式
            if hasattr(init_result, "model_dump"):
                result_content = init_result.model_dump()
                verbose(f"[Runner] 使用model_dump()解析结果: {json.dumps(result_content)[:200]}...")
            elif hasattr(init_result, "dict"):
                result_content = init_result.dict()
                verbose(f"[Runner] 使用dict()解析结果: {json.dumps(result_content)[:200]}...")
            else:
                result_content = init_result
                verbose(
                    f"[Runner] 直接使用结果: {json.dumps(result_content)[:200] if isinstance(result_content, dict) else str(result_content)[:200]}...")

            # 构造完整的JSON-RPC响应
            response = json.dumps({
                "jsonrpc": "2.0",
                "id": original_id,
                "result": result_content
            })

            verbose(f"[Runner] 通过SDK获取到规范的初始化响应: {response[:200]}...")

            # 再额外发送一个initialized通知给上游客户端吗？
            # 通常客户端接收到initialize响应后，会自己发送initialized通知
            # 所以这里不需要主动发送

            return response
        except Exception as e:
            error(f"[Runner] SDK初始化失败: {str(e)}")
            import traceback
            error(f"[Runner] 异常堆栈: {traceback.format_exc()}")
            # 如果SDK初始化失败，回退到常规请求处理
            verbose("[Runner] 回退到常规请求处理方式")

    verbose(f"[stdin] Processing request with id: {original_id}, method: {method}")

    # 常规请求处理：确定请求类型和构建请求对象
    req_obj = create_request_object(message, method)

    # 发送请求并处理响应
    try:
        verbose(f"[Runner] 向下游服务器发送请求，method: {method}, id: {original_id}")
        result = await send_request_with_timeout(session, req_obj, original_id)

        if method == "initialize":
            verbose(f"[Runner] 收到初始化响应: {result}")

        return result
    except Exception as e:
        error(f"[Runner] 请求处理异常 ({method}): {str(e)}")
        raise


# 创建请求对象
def create_request_object(message, method):
    """根据方法类型创建适当的请求对象"""
    # 作为代理，我们不需要严格验证方法是否符合标准列表
    # 直接创建ClientRequest对象，透明转发所有请求
    msg = dict(message)
    msg.pop("jsonrpc", None)  # 移除 jsonrpc 字段，SDK会自动添加
    msg.pop("id", None)       # 移除 id 字段，我们会在响应中重新添加

    try:
        # 尝试创建 ClientRequest
        return ClientRequest(**msg)
    except Exception as e:
        # 如果创建失败，回退到 ServerRequest
        verbose(f"[Runner] 创建 ClientRequest 失败，回退到 ServerRequest: {str(e)}")
        return ServerRequest(method=method, params=message.get("params", {}))


async def send_request_with_timeout(session, req_obj, original_id, timeout_seconds=60):
    """发送请求并处理超时和错误情况"""
    try:
        # 初始化 resp 为 None，防止超时时未定义
        resp = None
        # 使用超时机制
        with anyio.move_on_after(timeout_seconds):
            # 记录请求信息
            verbose(f"[Runner] 发送请求，原始ID={original_id}, 方法={req_obj.method if hasattr(req_obj, 'method') else '未知'}")

            # 发送请求并等待响应
            resp = await session.send_request(req_obj, DictModel)

        if resp:
            # 直接使用原始ID构造响应
            return json.dumps({
                "id": original_id,
                "jsonrpc": "2.0",
                "result": resp
            })
        else:
            return json.dumps({
                "id": original_id,
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": "Request timed out or empty response"
                }
            })

    except Exception as e:
        # 处理请求错误
        error_msg = str(e)
        error_code = -32603

        # 分类错误类型
        if "timed out" in error_msg.lower():
            error_code = -32001
        elif "connection" in error_msg.lower():
            error_code = -32002

        return json.dumps({
            "id": original_id,
            "jsonrpc": "2.0",
            "error": {
                "code": error_code,
                "message": f"Request failed: {error_msg}"
            }
        })


# 初始化 MCP 会话
async def initialize_session(session):
    """初始化 MCP 协议会话，转发上游客户端的初始化请求到下游服务器"""
    try:
        # 关键点: 作为代理，我们不应该主动调用 session.initialize()
        # 上游客户端会发送初始化请求，我们应该在 handle_stdin 函数中处理
        verbose("[Runner] MCP 代理准备就绪，等待上游客户端的初始化请求...")
        return True
    except Exception as init_error:
        error_msg = f"代理初始化失败: {str(init_error)}"
        error(f"[Runner] {error_msg}")
        return False


# 处理来自标准输入的消息
async def handle_stdin(session, is_shutting_down):
    """处理从标准输入接收的消息并转发到服务器"""
    loop = asyncio.get_event_loop()

    while not is_shutting_down:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            break

        try:
            message = json.loads(line)
            verbose(f"[stdin] Received message: {line.strip()}")

            method = message.get("method", "")
            # 根据消息类型处理
            if "id" in message:  # 这是请求，需要响应
                response = await process_client_request(message, session)
                sys.stdout.write(response + "\n")
                sys.stdout.flush()
                verbose(f"[stdin] Response sent for method: {method}")
            else:  # 这是通知，不需要响应
                await session.send(message)
                verbose(f"[stdin] Notification sent for method: {method}")

            verbose(f"[stdin] Processed: {line.strip()}")

        except json.JSONDecodeError as e:
            error(f"[stdin] JSON decode error: {e}")
        except Exception as e:
            error(f"[stdin] Error processing input: {e}")
            # 如果是请求(有ID)，才需要发送错误响应
            try:
                if 'message' in locals() and isinstance(message, dict) and "id" in message:
                    error_resp = json.dumps({
                        "jsonrpc": "2.0",
                        "id": message.get("id"),
                        "error": {
                            "code": -32700,
                            "message": f"Parse error: {str(e)}"
                        }
                    })
                    sys.stdout.write(error_resp + "\n")
                    sys.stdout.flush()
                    verbose(f"[stdin] Sent error response for parse error")
            except Exception as err:
                error(f"[stdin] Failed to send error response: {err}")


# 处理单个服务器消息
async def handle_single_server_message(data):
    """处理单个从服务器接收的消息并输出到标准输出"""
    try:
        # 记录接收到的原始数据类型，帮助调试
        verbose(f"[server_raw] Received data type: {type(data)}")

        # 尝试获取原始数据的字符串表示用于调试
        raw_data_str = str(data)
        if len(raw_data_str) > 500:
            raw_data_str = raw_data_str[:500] + "..."
        verbose(f"[server_raw] 原始数据: {raw_data_str}")

        # 根据数据类型进行处理
        if hasattr(data, "model_dump"):
            content = data.model_dump()
            verbose(f"[server_raw] Processed pydantic v2 model: {type(data)}")
        elif hasattr(data, "dict"):
            content = data.dict()
            verbose(f"[server_raw] Processed pydantic v1 model: {type(data)}")
        elif isinstance(data, dict):
            content = data
            verbose(f"[server_raw] Processed dict with {len(data)} keys")
        else:
            # 尝试转换为字符串，然后解析为JSON
            try:
                content = json.loads(str(data))
                verbose(f"[server_raw] Converted to JSON: {type(data)}")
            except:
                content = {"data": str(data)}
                verbose(f"[server_raw] Used raw string for unknown type: {type(data)}")

        # 检查是否是初始化响应
        is_init_response = False
        if isinstance(content, dict):
            if "result" in content and isinstance(content["result"], dict):
                result = content["result"]
                if "protocolVersion" in result or "serverInfo" in result:
                    is_init_response = True
                    verbose(f"[server] 检测到初始化响应: {json.dumps(content)[:200]}...")

                # 特别检查是否包含tools字段，这对于VSCode非常重要
                if "tools" in result:
                    verbose(f"[server] 检测到tools字段，工具数量: {len(result['tools'])}")

        # 检查数据是否已经是标准的 JSON-RPC 消息
        if isinstance(content, dict):
            if "jsonrpc" in content and ("id" in content or "method" in content):
                # 已经是标准格式，直接输出
                output = json.dumps(content)
                verbose(f"[server] Standard JSON-RPC message detected, id: {content.get('id')}")

            elif "result" in content and not "jsonrpc" in content:
                # 是结果但缺少 jsonrpc 字段，构造标准响应
                output = json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,  # 默认ID，应该不会被用到
                    "result": content["result"] if "result" in content else content
                })
                verbose(f"[server] Fixed response format by adding jsonrpc")

            else:
                # 其他类型的消息，包装为通知
                output = json.dumps(content)
                verbose("[server] Passing through data as-is")
        else:
            # 非字典类型，直接序列化
            output = json.dumps(content)

        # 写入 stdout 并立即刷新，确保 VS Code 能收到
        sys.stdout.write(output + "\n")
        sys.stdout.flush()
        verbose(f"[server] Response sent to stdout: {output}")

    except Exception as e:
        error(f"[server] Error processing server message: {e}")
        import traceback
        error(f"[server] 异常堆栈: {traceback.format_exc()}")
        # 尝试发送错误响应
        try:
            error_resp = json.dumps({
                "jsonrpc": "2.0",
                "id": 1,  # 使用默认ID
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                }
            })
            sys.stdout.write(error_resp + "\n")
            sys.stdout.flush()
            verbose(f"[server] Sent error response due to: {e}")
        except:
            error("[server] Failed to send error response")


async def create_stdio_runner(
    server_details: RegistryServer,
    config: Dict[str, Any],
    api_key: Optional[str] = None,
    analytics_enabled: bool = False
) -> Awaitable[None]:
    """创建并运行 STDIO 代理服务器"""
    verbose(f"Starting STDIO proxy runner: {server_details.qualifiedName}")
    is_shutting_down = False
    exit_stack = AsyncExitStack()

    def handle_error(error: Exception, context: str) -> Exception:
        verbose(f"[Runner] {context}: {error}")
        return error

    async def cleanup() -> None:
        nonlocal is_shutting_down
        if is_shutting_down:
            verbose("[Runner] Cleanup already in progress, skipping...")
            return
        verbose("[Runner] Starting cleanup...")
        is_shutting_down = True
        try:
            await exit_stack.aclose()
            verbose("[Runner] Resources closed successfully")
        except Exception as error:
            handle_error(error, "Error during cleanup")
        verbose("[Runner] Cleanup completed")

    def handle_sigint(sig, frame):
        verbose("[Runner] Received interrupt signal, shutting down...")
        asyncio.create_task(cleanup())
        # 立即打印一条确认消息，让用户知道CTRL+C已被捕获
        print("\n[CTRL+C] 正在关闭服务，请稍候...", flush=True)
        # 可选：设置一个短暂的超时，然后强制退出
        import threading
        threading.Timer(2.0, lambda: os._exit(0)).start()

    signal.signal(signal.SIGINT, handle_sigint)

    # 获取连接配置
    stdio_connection = next((conn for conn in server_details.connections if conn.type == "stdio"), None)
    if not stdio_connection:
        raise ValueError("No STDIO connection found")

    from ..registry import fetch_connection
    formatted_config = config
    verbose(f"Formatted config: {formatted_config}")
    server_config = await fetch_connection(server_details.qualifiedName, formatted_config)

    if not server_config or not isinstance(server_config, dict):
        raise ValueError("Failed to get valid stdio server configuration")

    command = server_config.get("command", "python")
    args = server_config.get("args", ["-m", server_details.qualifiedName])
    env_vars = server_config.get("env", {})
    env = get_runtime_environment(env_vars)

    verbose(f"Using environment: {json.dumps({k: '***' if k.lower().endswith('key') else v for k, v in env.items()})}")
    verbose(f"Executing: {command} {' '.join(args)}")

    try:
        # 创建服务器进程
        server_params = StdioServerParameters(
            command=command,
            args=args,
            env=env,
            encoding="utf-8"
        )

        verbose(f"Setting up stdio proxy client for {server_details.qualifiedName}")
        async with stdio_client(server_params, errlog=sys.stderr) as (read_stream, write_stream):
            verbose("Stdio proxy client connection established")

            # 创建 MCP 客户端会话
            from mcp import ClientSession
            session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))

            # 注册消息处理回调
            def handle_server_message(msg):
                rprint(f"[magenta][server][/magenta] {json.dumps(msg, ensure_ascii=False)}")
            session.on_message = handle_server_message

            # 初始化 MCP 协议
            if not await initialize_session(session):
                return

            # 使用简单的同步阻塞循环处理输入和服务器消息
            verbose("[Runner] 开始处理循环，使用同步阻塞模式")

            # 打印启动消息
            rprint("[cyan]MCP client running. Press Ctrl+C to stop.[/cyan]")

            # 循环处理客户端请求，直到关闭
            while not is_shutting_down:
                try:
                    # 从标准输入读取一行 (同步阻塞)
                    line = sys.stdin.readline()
                    if not line:
                        verbose("[Runner] 标准输入关闭，结束处理")
                        break

                    # 处理客户端请求
                    message = json.loads(line)
                    verbose(f"[stdin] Received message: {line.strip()}")

                    method = message.get("method", "")
                    # 根据消息类型处理
                    if "id" in message:  # 这是请求，需要响应
                        response = await process_client_request(message, session)
                        sys.stdout.write(response + "\n")
                        sys.stdout.flush()
                        verbose(f"[stdin] Response sent for method: {method}")
                    else:  # 这是通知，不需要响应
                        # 创建通知对象并发送
                        notification_obj = create_request_object(message, method)
                        await session.send_notification(notification_obj)
                        verbose(f"[stdin] Notification sent for method: {method}")

                    verbose(f"[stdin] Processed: {line.strip()}")

                except json.JSONDecodeError as e:
                    error(f"[stdin] JSON decode error: {e}")
                except Exception as e:
                    error(f"[stdin] Error processing input: {e}")
                    # 如果是请求(有ID)，才需要发送错误响应
                    try:
                        if 'message' in locals() and isinstance(message, dict) and "id" in message:
                            error_resp = json.dumps({
                                "jsonrpc": "2.0",
                                "id": message.get("id"),
                                "error": {
                                    "code": -32700,
                                    "message": f"Parse error: {str(e)}"
                                }
                            })
                            sys.stdout.write(error_resp + "\n")
                            sys.stdout.flush()
                            verbose(f"[stdin] Sent error response for parse error")
                    except Exception as err:
                        error(f"[stdin] Failed to send error response: {err}")

                # 检查是否有服务器消息需要处理
                # 注意：这部分仍需异步，因为我们需要非阻塞地检查服务器消息
                try:
                    # 使用超时机制非阻塞地检查服务器消息
                    with anyio.fail_after(0.1):  # 设置很短的超时
                        message = await read_stream.receive()
                        await handle_single_server_message(message)
                except TimeoutError:
                    # 超时表示没有消息，继续处理客户端请求
                    pass
                except Exception as e:
                    error(f"[Runner] 处理服务器消息异常: {e}")

            verbose("[Runner] 处理循环结束")

    except Exception as e:
        rprint(f"[red]Error running stdio proxy: {e}[/red]")
        raise
    finally:
        await cleanup()
