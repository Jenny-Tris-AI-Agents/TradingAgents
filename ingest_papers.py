import os
import pathlib
from google import genai  # 使用 2026 全新 SDK
from pypdf import PdfReader

PDF_DIR = pathlib.Path("research_papers")
KB_DIR = pathlib.Path("knowledge_base")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-3-flash-preview" # 既然你已经能看到列表，可以使用最先进的 3.0 版本

def summarize_paper(pdf_path):
    try:
        reader = PdfReader(pdf_path)
        text = "".join([page.extract_text() for page in reader.pages[:15]])
        
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=f"Extract strategy logic from this paper: {text}"
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    PDF_DIR.mkdir(exist_ok=True)
    KB_DIR.mkdir(exist_ok=True)
    
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    processed_count = 0

    for pdf_path in pdf_files:
        summary_path = KB_DIR / f"{pdf_path.stem}.md"
        
        # 如果你想强制重新生成，可以暂时注释掉下面这两行
        if summary_path.exists():
            print(f"Skipping: {pdf_path.name}")
            continue
            
        print(f"Processing: {pdf_path.name}...")
        summary = summarize_paper(pdf_path)
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        processed_count += 1

    print(f"Workflow Complete. Processed {processed_count} new papers.")

if __name__ == "__main__":
    main()
