import re

def validate_sql(sql: str):
    sql = sql.strip().lower()

    if not sql.startswith("select"):
        raise ValueError("Only SELECT allowed")

    return sql


# ✅ ADD THIS FUNCTION
def extract_sql_from_text(text: str):
    # try to find SQL inside ```sql ``` block
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # fallback: find SELECT query
    match = re.search(r"(SELECT .*?)(;|$)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return None