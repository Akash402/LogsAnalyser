# AI-Powered Log Analyzer

A lightweight Python tool that uses the **Gemini 2.5 Flash API** to transform messy, cryptic log files into actionable, plain-English executive summaries.

## Features
- **Smart Summarization:** Goes beyond simple keyword matching to understand context.
- **Root Cause Analysis:** Explains Python tracebacks and database errors in simple terms.
- **Security Insights:** Automatically flags suspicious patterns like brute-force login attempts.
- **Prioritized Fixes:** Suggests specific steps to resolve issues, ranked by urgency (High/Medium/Low).
- **Efficient Chunking:** Uses Python generators to process large log files without high memory overhead.

## Tech Stack
- **Language:** Python 3.10+
- **AI Model:** Gemini 2.5 Flash (via Google AI Studio)
- **SDK:** `google-genai`

## Getting Started

### 1. Clone the repo
```bash
git clone [https://github.com/yourusername/log-analyzer.git](https://github.com/yourusername/log-analyzer.git)
cd log-analyzer
```

### 2. Setup and Run
Follow these steps to get the analyzer running on your local machine.

1. Create a Python Virtual Environment - Using a virtual environment keeps your global Python installation clean.
```bash
# Create the environment
python -m venv venv

# Activate it (macOS/Linux)
source venv/bin/activate

# Activate it (Windows)
.\venv\Scripts\activate
```
2. Install Dependencies - With your virtual environment active, install the required SDK:
```bash
pip install -r requirements.txt
```

3. Obtain a  Gemini API Key
4. Configure PyCharm Environment Variables
   1. To run and debug securely within PyCharm:
   Click the Run Configuration dropdown (top right, next to the Play button) and select Edit Configurations.... 
   2. Select your log_analyzer.py script from the list. 
   3. Find the Environment variables field and click the browse icon (folder/three dots). 
   4. Click the + icon and add:
    ```shell
        Name: GEMINI_API_KEY
    
        Value: your_actual_api_key_here
    
        Click OK, then Apply.
    ```
5. Run the analyser - Ensure your log file (e.g., app_logs.log) is in the project root, then run the script via PyCharm's "Run" button or the terminal:
```bash
python log_analyzer.py
```
