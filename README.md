# Markdown to PDF (Streamlit)

Simple web app to edit Markdown, preview it, and download a PDF.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. In Streamlit Community Cloud, create a new app from the repo.
3. Set the app file to `app.py` (default).

The app uses `runtime.txt` to pin Python and `requirements.txt` for dependencies.
