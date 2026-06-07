from bs4 import BeautifulSoup

def parse_timetable(html):
    soup = BeautifulSoup(html, "lxml")
    
    # Target the timetable directly by its known GridView ID
    target_table = soup.find("table", {"id": "gvTimeTable1"})
    
    if target_table is None:
        # Fallback: find any table containing time slot headers
        for table in soup.find_all("table"):
            if "08:00" in table.get_text() or "09:30" in table.get_text():
                target_table = table
                break

    if target_table is None:
        return [["No timetable table found in the response."]]

    parsed_data = []
    rows = target_table.find_all("tr")
    for row in rows:
        cols = row.find_all(["td", "th"])
        cleaned_cols = [" ".join(cell.get_text().split()) for cell in cols]
        cleaned_cols = [cell for cell in cleaned_cols if cell.strip()]
        if cleaned_cols:
            parsed_data.append(cleaned_cols)

    return parsed_data