import fitz  # PyMuPDF
import sys

def extract_text_from_pdf(pdf_path):
    """
    Estrae il testo da un file PDF usando PyMuPDF.
    """
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"Errore durante l'estrazione del testo dal PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python ingest_paper.py <path_to_pdf>")
        sys.exit(1)
        
    pdf_file = sys.argv[1]
    
    print(f"Estrazione del testo dal file: {pdf_file}")
    text_content = extract_text_from_pdf(pdf_file)
    
    print("\n--- Contenuto Estratto ---\n")
    print(text_content)