import os
import pathlib
import google.generativeai as genai
from pypdf import PdfReader

# 1. Configuration & Paths
PDF_DIR = pathlib.Path("research_papers")
KB_DIR = pathlib.Path("knowledge_base")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')

def summarize_paper(pdf_path):
    """
    Extracts text from PDF and uses Gemini to generate a structured strategy summary.
    """
    try:
        reader = PdfReader(pdf_path)
        text = ""
        # Extract first 15 pages to keep context window efficient
        for i, page in enumerate(reader.pages[:15]):
            text += page.extract_text()
        
        # English Strategic Prompt [cite: 17, 18, 19, 20, 21, 22]
        prompt = f"""
        System: You are an expert Quantitative Trading Researcher specializing in Volatility and VIX strategies.
        Task: Extract the core mathematical and logical DNA from the provided research paper.
        
        Requirements:
        1. Entry Signals: Identify specific market conditions or technical indicators.
        2. Exit & Risk Management: Define stop-loss, take-profit, and position-sizing rules.
        3. Volatility Correlation: Explain the interaction with the VIX index or futures.
        4. Mathematical Formulas: Format all calculations using LaTeX (e.g., $E=mc^2$).
        5. Implementation Feasibility: Assess if this can be automated via Moomoo or Alpaca APIs.

        Paper Content:
        {text}
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error processing {pdf_path.name}: {str(e)}"

def main():
    # Ensure directories exist [cite: 164]
    PDF_DIR.mkdir(exist_ok=True)
    KB_DIR.mkdir(exist_ok=True)
    
    # 2. Find all PDFs
    pdf_files = list(PDF_DIR.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in research_papers/ folder.")
        return

    processed_count = 0
    for pdf_path in pdf_files:
        # Check if summary already exists to avoid redundant API calls [cite: 8]
        summary_path = KB_DIR / f"{pdf_path.stem}.md"
        
        if summary_path.exists():
            print(f"Skipping existing summary: {pdf_path.name}")
            continue
            
        print(f"Processing new paper: {pdf_path.name}...")
        summary = summarize_paper(pdf_path)
        
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
            
        print(f"Successfully generated: {summary_path.name}")
        processed_count += 1

    print(f"Workflow Complete. Processed {processed_count} new paper(s).")

if __name__ == "__main__":
    main()
