import os
import sys
import glob
import argparse
import time
from google import genai


def analyze_chunk(client, chunk_text):
    prompt = f"""
    Analyze this log snippet as a Senior SRE. Provide the below:
    1. SYSTEM HEALTH: 2-sentence summary.
    2. KEY ISSUES: Bulleted list of errors/anomalies.
    3. RECOMMENDED FIXES: Actionable steps ordered by PRIORITY.

    LOG:
    {chunk_text}
    """

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < 2:
                wait = 2 ** attempt
                print(f"  [Retry {attempt + 1}/2] API error: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                return f"[API Error after 3 attempts: {e}]"


def read_chunks(path, size=50, overlap=5):
    with open(path, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        chunk = lines[i:i + size]
        yield "".join(chunk)
        i += size
        if overlap and i < len(lines):
            i -= overlap


def aggregate_summary(client, summaries):
    combined = "\n\n---\n\n".join(
        f"Section {i + 1}:\n{s}" for i, s in enumerate(summaries)
    )
    prompt = f"""
    You are a Senior SRE. Below are per-section analyses of a log file.
    Produce a single consolidated report with:
    1. OVERALL SYSTEM HEALTH: 3-sentence summary.
    2. TOP ISSUES: The most critical problems across all sections, deduplicated.
    3. PRIORITIZED ACTION PLAN: Ordered list of fixes (High/Medium/Low priority).

    SECTION ANALYSES:
    {combined}
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"[Aggregate summary error: {e}]"


def process_file(client, path, chunk_size, overlap, output_lines):
    print(f"\n{'='*50}")
    print(f"ANALYSING: {path}")
    print(f"{'='*50}\n")

    summaries = []
    for i, chunk in enumerate(read_chunks(path, size=chunk_size, overlap=overlap)):
        print(f"--- SECTION {i + 1} ---")
        result = analyze_chunk(client, chunk)
        print(result)
        print("-" * 30)
        summaries.append(result)
        output_lines.append(f"=== {path} — Section {i + 1} ===\n{result}\n")

    if len(summaries) > 1:
        print("\n--- AGGREGATE SUMMARY ---")
        summary = aggregate_summary(client, summaries)
        print(summary)
        print("-" * 30)
        output_lines.append(f"=== {path} — Aggregate Summary ===\n{summary}\n")


def run():
    parser = argparse.ArgumentParser(description="AI-powered log analyser using Gemini.")
    parser.add_argument(
        "logs",
        nargs="*",
        default=["app_logs.log"],
        help="Log file path(s) or glob pattern(s). Defaults to app_logs.log."
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=50,
        help="Number of lines per analysis chunk (default: 50)."
    )
    parser.add_argument(
        "--overlap",
        type=int,
        default=5,
        help="Number of lines to overlap between chunks (default: 5)."
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Optional file path to save analysis results."
    )
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    # Expand globs
    paths = []
    for pattern in args.logs:
        matched = glob.glob(pattern)
        if matched:
            paths.extend(matched)
        else:
            paths.append(pattern)

    output_lines = []
    found_any = False

    for path in paths:
        if not os.path.exists(path):
            print(f"Warning: '{path}' not found, skipping.")
            continue
        found_any = True
        process_file(client, path, args.chunk_size, args.overlap, output_lines)

    if not found_any:
        print("Error: No valid log files found.")
        sys.exit(1)

    if args.output:
        with open(args.output, 'w') as f:
            f.write("\n".join(output_lines))
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    run()
