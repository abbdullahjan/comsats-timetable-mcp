def analyze_timetable(data):
    analysis = {
        "total_rows_found": len(data),
        "early_morning_classes": 0,
        "warnings": [],
        "summary": ""
    }
    
    if not data:
        analysis["warnings"].append("No usable timetable rows found.")
        analysis["summary"] = "Analysis failed due to missing schedule metrics."
        return analysis

    # Simple text heuristic checks on parsed table rows
    for row in data:
        row_string = " ".join(row).lower()
        if "08:30" in row_string or "8:30" in row_string:
            analysis["early_morning_classes"] += 1

    if analysis["early_morning_classes"] > 2:
        analysis["warnings"].append(f"Heavy schedule: You have {analysis['early_morning_classes']} early morning classes.")
        
    analysis["summary"] = f"Successfully parsed {len(data)} scheduling layout positions."
    return analysis