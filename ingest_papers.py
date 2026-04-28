import os
import pathlib
from google import genai  # 使用 2026 全新 SDK
from pypdf import PdfReader

# 1. 配置路径
SOURCE_DIR = pathlib.Path("research_papers") # 统一存放原始文件
KB_DIR = pathlib.Path("knowledge_base")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. 初始化最新客户端
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-3-flash-preview" # 2026 最强 Flash 模型

def extract_text(file_path):
    """根据文件后缀选择不同的读取方式"""
    suffix = file_path.suffix.lower()
    
    if suffix == ".pdf":
        try:
            reader = PdfReader(file_path)
            # 提取前 15 页以保持效率 [cite: 469]
            return "".join([page.extract_text() for page in reader.pages[:15]])
        except Exception as e:
            return f"PDF Error: {str(e)}"
            
    elif suffix == ".md":
        try:
            # Markdown 直接作为文本读取
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Markdown Error: {str(e)}"
    
    return ""

def summarize_content(text, file_name):
    """调用 Gemini 生成策略摘要"""
    if not text.strip():
        return "Error: No text extracted."
        
    prompt = f"""
    System: You are an expert Quantitative Trading Researcher.
    Task: Extract strategy logic from the following document named '{file_name}'.
    Focus on: Entry/Exit signals, VIX correlation, and Mathematical formulas in LaTeX.
    
    Content:
    {text[:30000]} # 限制长度以防溢出
    """
    
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {str(e)}"

def main():
    SOURCE_DIR.mkdir(exist_ok=True)
    KB_DIR.mkdir(exist_ok=True)
    
    # 3. 同时检索 PDF 和 MD 文件
    extensions = ("*.pdf", "*.md")
    files_to_process = []
    for ext in extensions:
        files_to_process.extend(list(SOURCE_DIR.glob(ext)))
        
    processed_count = 0

    for file_path in files_to_process:
        summary_path = KB_DIR / f"{file_path.stem}.md"
        
        # 增量更新逻辑：跳过已存在的文件以节省额度 
        if summary_path.exists():
            print(f"Skipping: {file_path.name}")
            continue
            
        print(f"Processing: {file_path.name}...")
        text = extract_text(file_path)
        summary = summarize_content(text, file_path.name)
        
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write(summary)
        processed_count += 1

    print(f"Workflow Complete. Processed {processed_count} new files.")

if __name__ == "__main__":
    main()
