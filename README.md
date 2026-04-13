# AI-Powered Log Analyzer

A lightweight Python tool that uses the **Gemini 2.5 Flash API** to transform messy, cryptic log files into actionable, plain-English executive summaries.

## Features
- **Smart Summarization:** Goes beyond simple keyword matching to understand context.
- **Root Cause Analysis:** Explains Python tracebacks and database errors in simple terms.
- **Security Insights:** Automatically flags suspicious patterns like brute-force login attempts.
- **Prioritized Fixes:** Suggests specific steps to resolve issues, ranked by urgency (High/Medium/Low).
- **Efficient Chunking:** Processes large log files in configurable chunks to avoid high memory overhead.
- **Chunk Overlap:** Overlaps lines between chunks so errors spanning boundaries aren't missed.
- **Retry with Backoff:** Automatically retries failed API calls up to 3 times with exponential backoff.
- **Multiple Files & Glob Support:** Analyze one file, many files, or a wildcard pattern in a single run.
- **Aggregate Summary:** After all chunks are processed, generates a single consolidated report per file.
- **Save Output:** Optionally write all results to a file with `--output`.

## Tech Stack
- **Language:** Python 3.10+
- **AI Model:** Gemini 2.5 Flash (via Google AI Studio)
- **SDK:** `google-genai`

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/log-analyzer.git
cd log-analyzer
```

### 2. Setup and Run
Follow these steps to get the analyzer running on your local machine.

1. Create a Python Virtual Environment
```bash
# Create the environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
.\venv\Scripts\activate
```

2. Install Dependencies
```bash
pip install -r requirements.txt
```

3. Obtain a Gemini API Key from [Google AI Studio](https://aistudio.google.com/app/apikey).

4. Set the API Key as an environment variable:
```bash
# macOS/Linux
export GEMINI_API_KEY=your_actual_api_key_here

# Windows
set GEMINI_API_KEY=your_actual_api_key_here
```

   **PyCharm users:** Go to Run > Edit Configurations, select your script, and add `GEMINI_API_KEY` under Environment Variables.

5. Run the analyzer:
```bash
# Analyze a single file
python log_analyser.py app_logs.log

# Analyze multiple files
python log_analyser.py app_logs.log server.log worker.log

# Analyze using a glob pattern
python log_analyser.py logs/*.log

# Save results to a file
python log_analyser.py app_logs.log --output report.txt
```

## CLI Options

| Option | Default | Description |
|---|---|---|
| `logs` | `app_logs.log` | One or more log file paths or glob patterns |
| `--chunk-size` | `50` | Number of lines per analysis chunk |
| `--overlap` | `5` | Number of lines to overlap between chunks |
| `--output` | _(none)_ | File path to save the full analysis output |

## Example

```bash
python log_analyser.py logs/*.log --chunk-size 100 --overlap 10 --output report.txt
```

This will analyze all `.log` files in the `logs/` directory, process them in 100-line chunks with 10-line overlaps, and save the full report to `report.txt`.
