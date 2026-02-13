# main.py

import os
import uuid
import base64
import sys
import asyncio
import logging
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.concurrency import run_in_threadpool

from services import extract_financials
from utils import generate_excel


# ---------------------------
# Windows Event Loop Fix
# ---------------------------
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


# ---------------------------
# Logging Setup
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ---------------------------
# App Initialization
# ---------------------------
app = FastAPI(title="Financial Report Extraction API")


# ---------------------------
# CORS Configuration
# ---------------------------
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_origin, "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE_MB = 20


@app.get("/api/health")
def health_check():
    return {"status": "ok", "service": "backend"}


# ---------------------------
# Upload Endpoint
# ---------------------------
@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):

    logger.info(f"Received file: {file.filename}")

    # Validate extension
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed."
        )

    # Read file
    content = await file.read()

    # Validate size
    if len(content) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"File exceeds {MAX_FILE_SIZE_MB}MB limit."
        )

    # Unique filename
    unique_filename = f"{uuid.uuid4().hex}{extension}"
    file_path = UPLOAD_DIR / unique_filename

    try:
        # Save file
        with open(file_path, "wb") as f:
            f.write(content)

        logger.info(f"File saved at {file_path}")

        # Extract financial rows (LlamaParse only stage)
        data = await run_in_threadpool(
            extract_financials,
            str(file_path)
        )

        if not data:
            logger.warning("No financial data extracted.")
            return {
                "success": False,
                "financialData": {"pnl": [], "balanceSheet": [], "cashFlow": [], "others": []},
                "excelBuffer": None,
                "message": "No financial data found in PDF. Ensure it contains a Profit & Loss statement."
            }

        logger.info(f"Extraction successful. Tables: {len(data)}")

        # Flatten table objects for Excel generation
        # data is now: [ { headers: [...], rows: [...], table_number: 1 }, ... ]
        flat_data_for_excel = []
        if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict) and "rows" in data[0]:
            flat_data_for_excel = data[0]["rows"] if data[0]["rows"] else []
        else:
            flat_data_for_excel = data if data else []

        # Generate Excel
        excel_bytes = await run_in_threadpool(
            generate_excel,
            flat_data_for_excel
        )

        excel_base64 = base64.b64encode(excel_bytes).decode("utf-8")
        logger.info(f"Excel generated: {len(excel_base64)} bytes (base64)")

        # Reshape data to match frontend structure: { pnl: [...], balanceSheet: [], cashFlow: [], others: [] }
        structured_data = {
            "pnl": data,
            "balanceSheet": [],
            "cashFlow": [],
            "others": []
        }

        return {
            "success": True,
            "financialData": structured_data,
            "excelBuffer": excel_base64
        }

    except ValueError as e:
        logger.exception("Configuration error during processing.")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        logger.exception("Critical failure during processing.")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )

    finally:
        # Cleanup
        if file_path.exists():
            file_path.unlink()
            logger.info("Temporary file deleted.")
