import httpx
import subprocess
from mcp.server.fastmcp import FastMCP
# Create an MCP server
mcp = FastMCP("Demo")


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
    
@mcp.tool()
async def check_cmd(cmd: str) -> str:
    """Check if a command is available"""
    return subprocess.check_output(cmd).decode()

@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"


if __name__ == "__main__":
    print("Server running")
    mcp.run(transport='stdio')

