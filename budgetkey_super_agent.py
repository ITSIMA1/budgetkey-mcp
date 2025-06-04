import requests

class BudgetKeyAPI:
    def __init__(self, base_url="https://next.obudget.org/api/"):
        self.base_url = base_url

    def query_sql(self, sql_query):
        url = f"{self.base_url}query"
        params = {"query": sql_query}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

# ---------------

import openai

def interpret_with_gpt(question, openai_api_key):
    openai.api_key = openai_api_key

    prompt = f"""
You are an assistant that translates Hebrew questions into SQL queries for the BudgetKey dataset.
Use the `supports` table with fields like:
- entity_name (string): name of the organization
- allocated_amount (number): the amount of money allocated
- support_year (integer): the year of the support

Translate the following question to a SQL query that can be used with the BudgetKey API:

שאלה: "{question}"
SQL:
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    return response.choices[0].message.content.strip()


def run_super_question(question, openai_api_key):
    sql_query = interpret_with_gpt(question, openai_api_key)
    print("\n📄 SQL Generated:\n", sql_query)
    api = BudgetKeyAPI()
    results = api.query_sql(sql_query)

    print("\n🔍 Results:")
    for row in results.get("rows", [])[:10]:
        print(" | ".join(str(x) for x in row))

# Example:
# run_super_question("מי קיבל הכי הרבה תמיכה בשנת 2023?", "your-openai-api-key")
