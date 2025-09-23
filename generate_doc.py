import os
import pypandoc

def convert_md_to_docx(md_file, docx_file):
    output = pypandoc.convert_file(md_file, 'docx', outputfile=docx_file)
    assert output == ""  # pypandoc devuelve "" si todo salió bien
    print(f"✅ DOCX generado: {docx_file}")

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.abspath(__file__))
    md_path = os.path.join(repo_root, "README.md")
    docx_path = os.path.join(repo_root, "README.docx")

    if os.path.exists(md_path):
        convert_md_to_docx(md_path, docx_path)
    else:
        print("❌ No se encontró README.md en la rama actual")