from mcp.server.mcpserver import MCPServer

mcp = MCPServer("EmployeeServer")


@mcp.tool()
def get_employee(employee_id: str) -> str:
    """Lookup employee information"""

    employees = {
        "1001": "John Smith - IT",
        "1002": "Jane Doe - HR",
        "1003": "David Brown - Finance"
    }

    return employees.get(
        employee_id,
        "Employee not found"
    )


if __name__ == "__main__":
    print("Starting MCP Server...")
    mcp.run()
