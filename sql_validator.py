import re

def validate_sql(sql: str):
    if not sql:
        raise ValueError("Empty SQL")

    sql_clean = sql.strip().lower()

    #  allow only SELECT
    if not sql_clean.startswith("select"):
        raise ValueError("Only SELECT queries are allowed")

    return sql.strip()


#  Improved extractor (more powerful)
def extract_sql_from_text(text: str):
    if not text:
        return None

    #  Case 1: ```sql block
    match = re.search(r"```sql\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    #  Case 2: normal SELECT query
    match = re.search(r"(SELECT .*?)(;|$)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    #  Case 3: fallback (any SELECT till end)
    match = re.search(r"(select .*)", text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()

    return None
