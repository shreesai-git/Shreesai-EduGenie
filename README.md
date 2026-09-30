# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project document. It provides Q&A, simplified explanations, quiz generation, summarization, and personalized learning paths through a FastAPI backend and HTML/CSS/JavaScript frontend.

## Project structure

```text
EduGenie/
├── main.py
├── gemini_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## VS Code setup on Windows

1. Install Python 3.10 or newer and make sure `python --version` works.
2. Open this `EduGenie` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv .venv
```

5. Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

6. Upgrade pip and install dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

7. Copy `.env.example` to `.env` and put your Gemini API key in `GEMINI_API_KEY`.

8. Start the server:

```powershell
uvicorn main:app --reload
```

9. Open **http://127.0.0.1:8000** in your browser.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Web application |
| GET | `/health` | Health check |
| POST | `/qa` | Answer a question |
| POST | `/explain` | Explain a concept |
| POST | `/quiz` | Generate MCQs |
| POST | `/summarize` | Summarize text |
| POST | `/learn/recommendations` | Generate a learning path |

FastAPI's automatic API documentation is available at **/docs** while the server is running.

## Testing

Run:

```powershell
pytest
```

The included tests check that the application starts, the home page loads, and the health endpoint responds. They do not call Gemini, so an API key is not required for those basic tests.

## Local explanation model

The supplied project document specifies LaMini-Flan-T5-783M for local concept explanation. This implementation preserves that option but makes it opt-in because downloading and loading a 783M-parameter model is substantially heavier than the cloud-backed path.

To enable it, first install the optional local-model dependencies:

```powershell
pip install -r requirements-local.txt
```

Then set this in `.env`:

```env
USE_LOCAL_EXPLANATION=true
LOCAL_EXPLANATION_MODEL=MBZUAI/LaMini-Flan-T5-783M
```

If the local model fails to load, the explanation module falls back to Gemini instead of crashing the endpoint.

## Notes

- Never commit `.env` or expose your Gemini API key in frontend JavaScript.
- `GEMINI_MODEL` can be changed in `.env` if a different model is available to your account.
- The quiz endpoint validates the returned JSON before sending it to the browser.
- The frontend uses `textContent`/HTML escaping for generated text to reduce the risk of injecting model output as HTML.
