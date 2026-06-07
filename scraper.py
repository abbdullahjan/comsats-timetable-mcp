import httpx
from bs4 import BeautifulSoup

URL = "https://cuonline.cuiatd.edu.pk/timetable/COmsatstimetableprintversion.aspx"

def extract_hidden_fields(html):
    soup = BeautifulSoup(html, "lxml")
    data = {}
    for inp in soup.find_all("input"):
        name = inp.get("name")
        value = inp.get("value", "")
        if name and name.startswith("__"):
            data[name] = value
    return data

def extract_selected_class(html):
    """Read back which class the server actually rendered the timetable for."""
    soup = BeautifulSoup(html, "lxml")
    select = soup.find("select", {"id": "ddlClasses"})
    if select:
        selected = select.find("option", selected=True)
        if selected:
            return selected.get("value", "")
    return ""

async def fetch_timetable_page(target_class: str = "BCS 5A"):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Origin": "https://cuonline.cuiatd.edu.pk",
        "Referer": URL
    }

    async with httpx.AsyncClient(follow_redirects=True, headers=headers) as client:

        # STEP 1: Initial GET — get base tokens (page defaults to BBA 5A)
        init_res = await client.get(URL)
        tokens = extract_hidden_fields(init_res.text)

        # STEP 2: Trigger the dropdown onchange postback with the target class.
        # ASP.NET will validate the token, re-render the page for the new class,
        # and return a fresh __EVENTVALIDATION bound to that selection.
        postback_payload = {
            "__EVENTTARGET": "ddlClasses",
            "__EVENTARGUMENT": "",
            "__LASTFOCUS": "",
            "__VIEWSTATE": tokens.get("__VIEWSTATE", ""),
            "__VIEWSTATEGENERATOR": tokens.get("__VIEWSTATEGENERATOR", ""),
            "__EVENTVALIDATION": tokens.get("__EVENTVALIDATION", ""),
            "ddlClasses": target_class,
        }

        final_res = await client.post(URL, data=postback_payload)

        # Verify the server actually rendered the right class
        rendered_class = extract_selected_class(final_res.text)
        if rendered_class != target_class:
            raise ValueError(
                f"Server rendered '{rendered_class}' instead of '{target_class}'. "
                f"Check that '{target_class}' exists in the dropdown."
            )

        return final_res.text