import requests
import json
import os 

api_key = os.environ.get("ai_api_key")
prompt = """

You are a data extraction assistant. Extract all product names and their prices from the raw text below.

RULES:
- Output format: one row per product, as: PRODUCT,PRICE
- If a product has no price, use: PRODUCT,NULL
- Include the currency symbol in the price (e.g. £30.00)
- Include sizes if given or quantity ('48x' , '18oz')
- Only extract real product names — not codes alone, categories, or metadata (e.g. ignore "Case: 1000")
- Product codes (e.g. D22013) may be included as part of the name if accompanied by a descriptive name
- Do NOT output any explanation, heading, commentary, or blank lines — only the CSV rows
- If there are no valid products in the data, output only: NA
- Do not invent or assume prices that are not clearly associated with a product

EXAMPLE:
" + example_text + "

"""

url = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {ai}",
    "Content-Type": "application/json",
}

model = "openrouter/owl-alpha"


def call_api(data):
    response = requests.post(url, data=json.dumps({
        "model": model,
        "messages": [
            {
              "role": "user",
              "content": (prompt + data)
            }
          ],
        "reasoning": {"enabled": True}
    }), headers=headers)
    return response.json()
    
def split_data(unsplit_data, chunk_size=1000):
    lines = unsplit_data.split('\n')
    chunks = []
    current_chunk = []
    current_length = 0

    for line in lines:
        if current_length + len(line) + 1 > chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(line)
        current_length += len(line) + 1  # +1 for the \n

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

def analyse(unsplit_data):
    chunks = split_data(unsplit_data)
    for count, chunk in enumerate(chunks, 1):
        data = call_api(chunk)

        successful = False
        while not successful:
    
            try:
                content = data['choices'][0]['message']['content']
                successful = True
            except:
                pass
            
            
        return (content)

