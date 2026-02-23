

# 📊 Money Stories Finserv Dashboard

### **Built by Ankit Kumar**

> **The Problem:** Financial reports like the "Tata Motors Quarterly Statement" are messy, multi-page PDFs. Extracting specific yearly data manually takes hours and is prone to human error.
> **The Solution:** An AI-powered dashboard that "reads" these complex PDFs like a human expert, extracts the exact 14 financial lines needed, and generates a professional Excel report in seconds.

---

## 🚀 How it Works (The Workflow)

I built this project to be as simple as possible for the end-user. Here is the path your data takes:

1. **Upload** ➔ You drop a complex financial PDF into the dashboard.
2. **AI Scan (LlamaParse)** ➔ The system uses **AI Vision** to scan the pages. It doesn't just look for text; it understands the "layout" of the tables.
3. **Data Structuring (Gemini 2.5 Flash)** ➔ This is the "brain" of the operation. I used **Gemini 2.5 Flash** to analyze the raw data, clean up numerical inconsistencies, and map everything to a standardized financial schema.
4. **Smart Filter** ➔ Instead of giving you everything, the system specifically looks for **Year-Wise** data (like FY 2025 and 2024), ignoring the quarterly clutter.
5. **Verification** ➔ The extracted data (Revenue, Tax, EPS, etc.) is displayed in a clean, scrollable table for you to review.
6. **Export** ➔ With one click, you download a perfectly formatted **Excel file** ready for your financial analysis.

---

## 🛠️ The "Engine" Under the Hood

To achieve 100% accuracy, I used a modern "Tech Stack":

* **Frontend:** React.js (For a fast, smooth user experience).
* **Backend:** Python & FastAPI (The "brain" that processes the files).
* **AI Intelligence:** **Gemini 2.5 Flash** (For high-speed data cleaning and structuring).
* **AI Vision:** **LlamaParse Premium** (For high-fidelity table extraction).
* **Hosting:** Live on **Netlify** (Frontend) and **Render** (Backend).

---

## 📈 Key Features I Focused On

* **Progress Tracking:** Since AI vision and Gemini processing take time, I added a progress bar with live logs so the user knows exactly what the AI is doing.
* **Precision:** Targeted extraction of 14 specific line items required for financial modeling.
* **Reliability:** Built to handle multi-page documents without losing data between pages.

---

### **How to Run This Locally**

1. Clone the repo.
2. Add your `LLAMA_CLOUD_API_KEY` and `GEMINI_API_KEY` to the `.env` file.
3. Run the backend: `uvicorn main:app --reload`.
4. Run the frontend: `npm start`.

---


