import pymupdf.layout
import pymupdf4llm
from pathlib import Path


def pdf_to_md(pdf_path: str, dir: str):
    out_dir = Path(dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / (Path(pdf_path).stem + ".md")

    if md_path.exists() and md_path.stat().st_size > 0:
        print(f"Markdown already exists for {pdf_path}, skipping conversion.")
        return str(md_path)

    print(f"Converting {pdf_path} to markdown...")

    doc = pymupdf.open(pdf_path)
    md_text = pymupdf4llm.to_markdown(doc)
    md_path.write_bytes(md_text.encode())
    print(f"Saved markdown to {md_path}")
    return str(md_path)


if __name__ == "__main__":
    pdf_path = "data/raw/dsm5_eng.pdf"
    output_dir = "data/raw"
    pdf_to_md(pdf_path, output_dir)
