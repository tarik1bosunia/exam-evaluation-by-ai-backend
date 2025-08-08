import fitz  # PyMuPDF
import os


doc = fitz.open("resume_md_tarik_bosunia.pdf")

# Get full path of the file
full_path = doc.name  # E.g., "E:/django projects/answer_iq/resume_md_tarik_bosunia.pdf"

# Get just the file name (with extension)
file_name = os.path.basename(full_path)  # "resume_md_tarik_bosunia.pdf"

# Get file name without extension
name_without_ext = os.path.splitext(file_name)[0]  # "resume_md_tarik_bosunia"

print("Full path:", full_path)
print("File name:", file_name)
print("Without extension:", name_without_ext)

# Final output directory
output_dir = os.path.join("media", "images", "exampaper", name_without_ext)

# Create nested output directory
os.makedirs(output_dir, exist_ok=True)

for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=300)
    output_path = os.path.join(output_dir, f"page_{i + 1}.png")
    pix.save(output_path)