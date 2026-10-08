import asyncio
from mcp import Client


async def get_employee_from_mcp(employee_id: str):

    async with Client(
        "http://localhost:8000/mcp"
    ) as client:

        result = await client.call_tool(
            "get_employee",
            {
                "employee_id": employee_id
            }
        )

        return str(result.structured_content)