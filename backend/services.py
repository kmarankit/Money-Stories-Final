# services
import os
import json
from dotenv import load_dotenv
from llama_parse import LlamaParse
from google import genai

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print(f"[INIT] LLAMA_API_KEY present: {bool(LLAMA_API_KEY)}")
print(f"[INIT] GEMINI_API_KEY present: {bool(GEMINI_API_KEY)}")


def _get_gemini_client():
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY missing in backend/.env")

    try:
        return genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        raise ValueError(f"Failed to initialize Gemini client: {e}")


def extract_raw_markdown(file_path: str) -> str:
    if not LLAMA_API_KEY:
        raise ValueError("LLAMA_CLOUD_API_KEY missing in backend/.env")

    parser = LlamaParse(
        api_key=LLAMA_API_KEY,
        result_type="markdown",
        premium_mode=True
    )
    documents = parser.load_data(file_path)
    return "\n".join(doc.text for doc in documents)


# =====================================================
# UPDATED STEP 2 - Yearly Extraction Logic
# =====================================================
def transform_to_yearly_report(raw_markdown: str):
    """
    Extract all available years from the P&L statement.
    """
    prompt = f"""
    You are a financial analyst. Extract the P&L (Profit and Loss) table from this report.

    TASK:
    1. Find the 'Consolidated Statement of Profit and Loss' or similar P&L table.
    2. Extract ALL available financial data columns (all years/periods available).
    3. Include headers like: "FY2024", "FY2025", "FY2026", or "Year Ended March 31, 2024" etc.
    4. Preserve the Particulars/Line items with ALL their corresponding yearly values.
    5. Return as a JSON list where each object has "Particulars" and columns for each year.

    Example output format (with 3 years):
    [
        {{
            "Particulars": "Revenue from operations",
            "FY26": 123456,
            "FY25": 120000,
            "FY24": 100000
        }},
        {{
            "Particulars": "Total Income",
            "FY26": 125000,
            "FY25": 122000,
            "FY24": 102000
        }}
    ]

    IMPORTANT RULES:
    - Extract ALL years found in the report (not just one).
    - Column names should be clean: FY24, FY25, FY26, or Year_Ended_2024, etc.
    - Convert all numeric values to numbers (not strings).
    - Remove index numbers from Particulars (e.g., '1. Revenue' -> 'Revenue').
    - Handle negative numbers: (1,234) becomes -1234.
    - Keep ALL line items from the P&L statement.

    RAW TEXT:
    {raw_markdown}

    Return ONLY valid JSON. If you cannot find P&L data, return empty list [].
    """

    client = _get_gemini_client()

    try:
        print("[DEBUG] Sending request to Gemini...")
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config={"response_mime_type": "application/json"}
        )

        parsed = json.loads(response.text)
        print(f"[DEBUG] Parsed JSON successfully: {type(parsed)}, length: {len(parsed) if isinstance(parsed, list) else 'N/A'}")
        return parsed

    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse Gemini JSON response: {e}")
        print(f"[ERROR] Raw response: {response.text if 'response' in locals() else 'No response'}")
        return []
    except Exception as e:
        print(f"[ERROR] Gemini extraction failed: {e}")
        return []


# =====================================================
# MASTER FUNCTION
# =====================================================
def extract_financials(file_path: str):
    print(f"\n[SERVICE] Processing Yearly Data: {file_path}")

    markdown = extract_raw_markdown(file_path)
    print("[INFO] Markdown extraction complete.")

    yearly_data = transform_to_yearly_report(markdown)
    print(f"[INFO] Gemini returned {len(yearly_data)} rows")

    if not yearly_data:
        print("[WARNING] No yearly data extracted")
        return []

    # Frontend expects: [ { headers: [...], rows: [...], table_number: 1 }, ... ]
    if isinstance(yearly_data, list) and yearly_data:
        headers = list(yearly_data[0].keys()) if isinstance(yearly_data[0], dict) else []

        table_obj = {
            "table_number": 1,
            "headers": headers,
            "rows": yearly_data
        }

        print(f"[SUCCESS] Returning {len(yearly_data)} rows in table format")
        return [table_obj]

    return []
