import asyncio
from src.mcp_server_time.server import TimeServer

async def main():
    server = TimeServer("Asia/Shanghai")
    await server.mcp.run_stdio_async()

if __name__ == "__main__":
    asyncio.run(main()) 