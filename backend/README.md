# Money Stories Backend

## Setup

1. Create a virtual environment and install dependencies:

```bash
cd backend
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
```

2. Configure environment variables:

```bash
copy .env.example .env
```

Then fill in `LLAMA_CLOUD_API_KEY` and `GEMINI_API_KEY` in `backend/.env`.

3. Run the API server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API endpoints

- `GET /api/health` - health check
- `POST /api/upload` - upload a PDF and get extracted financial data + Excel file (base64)

## Frontend connection

From frontend, call:

- `http://localhost:8000/api/health`
- `http://localhost:8000/api/upload`
