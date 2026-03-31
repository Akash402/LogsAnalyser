import os
from google import genai

def analyze_chunk(chunk_text):
    client = genai.Client()

    prompt = f"""
    Analyze this log snippet as a Senior SRE. Provide the below:
    1. SYSTEM HEALTH: 2-sentence summary.
    2. KEY ISSUES: Bulleted list of errors/anomalies.
    3. RECOMMENDED FIXES: Actionable steps ordered by PRIORITY .

    LOG:
    {chunk_text}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"API Error: {e}"

def read_chunks(path, size=50):
    with open(path, 'r') as f:
        chunk = []
        for line in f:
            chunk.append(line)
            if len(chunk) >= size:
                yield "".join(chunk)
                chunk = []
        if chunk:
            yield "".join(chunk)

def run():
    log_file = "app_logs.log"
    if not os.path.exists(log_file):
        print("Log file missing.")
        return

    print(f"--- ANALYSING {log_file} ---\n")
    for i, chunk in enumerate(read_chunks(log_file)):
        print(f"--- SECTION {i + 1} ---")
        print(analyze_chunk(chunk))
        print("-" * 30)

if __name__ == "__main__":
    run()
