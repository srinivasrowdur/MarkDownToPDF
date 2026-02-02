import io
from datetime import datetime

import streamlit as st
from markdown import markdown
from xhtml2pdf import pisa

DEFAULT_MD = """# Markdown to PDF\n\nType your **Markdown** on the left.\n\n- Headings\n- Lists\n- *Emphasis*\n\n> Blockquotes are supported too.\n\n```python\nprint(\"Hello, PDF!\")\n```\n"""


@st.cache_data(show_spinner=False)
def markdown_to_pdf_bytes(md_text: str) -> bytes:
    html_body = markdown(
        md_text,
        extensions=["fenced_code", "tables", "sane_lists"],
    )
    html = f"""<!doctype html>
<html>
  <head>
    <meta charset=\"utf-8\" />
    <style>
      body {{
        font-family: Arial, Helvetica, sans-serif;
        line-height: 1.5;
        padding: 24px;
      }}
      ul, ol {{
        margin: 0 0 12px 20px;
        padding: 0;
      }}
      li {{
        margin: 4px 0;
      }}
      code, pre {{
        font-family: \"Courier New\", Courier, monospace;
        background: #f6f6f6;
      }}
      pre {{
        padding: 12px;
        overflow-x: auto;
      }}
      table {{
        border-collapse: collapse;
      }}
      th, td {{
        border: 1px solid #ddd;
        padding: 6px 10px;
      }}
      blockquote {{
        border-left: 4px solid #ddd;
        padding-left: 12px;
        color: #555;
      }}
    </style>
  </head>
  <body>
    {html_body}
  </body>
</html>
"""
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(src=html, dest=result)
    if pisa_status.err:
        raise RuntimeError("PDF generation failed")
    return result.getvalue()


st.set_page_config(page_title="Markdown to PDF", layout="wide")

st.title("Markdown to PDF")
st.caption("Convert Markdown to a clean, downloadable PDF.")

left, right = st.columns(2, gap="large")

with left:
    st.subheader("Editor")
    md_text = st.text_area(
        "Markdown",
        value=DEFAULT_MD,
        height=500,
        label_visibility="collapsed",
    )

with st.sidebar:
    st.subheader("Export")
    default_name = f"document-{datetime.now().strftime('%Y%m%d')}.pdf"
    file_name = st.text_input("PDF file name", value=default_name)
    file_name = file_name.strip() or default_name
    if not file_name.lower().endswith(".pdf"):
        file_name = f"{file_name}.pdf"

try:
    pdf_bytes = markdown_to_pdf_bytes(md_text)
    pdf_error = None
except Exception as exc:
    pdf_bytes = None
    pdf_error = exc

with right:
    header_left, header_right = st.columns([1, 0.35], vertical_alignment="center")
    with header_left:
        st.subheader("Preview")
    with header_right:
        if pdf_bytes:
            st.download_button(
                "Download PDF",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf",
                use_container_width=True,
            )
    if pdf_error:
        st.error(f"Could not generate PDF: {pdf_error}")
    st.markdown(md_text)
