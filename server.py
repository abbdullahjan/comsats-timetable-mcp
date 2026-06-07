from mcp.server.fastmcp import FastMCP
from scraper import fetch_timetable_page
from parser import parse_timetable
from analyzer import analyze_timetable

mcp = FastMCP("Timetable Optimization Assistant")

@mcp.tool()
async def get_raw_timetable(target_class: str = "BCS 5A") -> dict:
    """Fetch the raw string structure of a target class section from the timetable server."""
    html = await fetch_timetable_page(target_class)
    return {
        "class_targeted": target_class,
        "html_preview": html[:1500]
    }

@mcp.tool()
async def get_timetable(target_class: str = "BCS 5A") -> dict:
    """Retrieves structured matrix rows of the university timetable data for a specified section."""
    html = await fetch_timetable_page(target_class)
    data = parse_timetable(html)
    return {
        "class_targeted": target_class,
        "timetable_records": data
    }

@mcp.tool()
async def analyze_schedule_quality(target_class: str = "BCS 5A") -> dict:
    """Performs deep diagnostics check for slot density and early morning burdens."""
    html = await fetch_timetable_page(target_class)
    data = parse_timetable(html)
    metrics = analyze_timetable(data)
    return {
        "class_targeted": target_class,
        "insights": metrics
    }

if __name__ == "__main__":
    mcp.run()