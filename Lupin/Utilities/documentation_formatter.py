# Imports
from docx import Document
from Utilities.data_manager import load_data
from Utilities.module_handler import get_modules, call_module_function
from Utilities.data_manager import get_data_files, get_saves_directory



# Create heading
def heading(document: Document, title : str) -> None:
    document.add_heading(title, level=1)



# Create subheading
def subheading(document: Document, title : str) -> None:
    document.add_heading(title, level=2)



# Create paragraph
def paragraph(document: Document, text : str) -> None:
    document.add_paragraph(text)



# Create unordered list
def unordered_list(document: Document, items : list) -> None:
    for item in items:
        document.add_paragraph(item, style='ListBullet')



# Create ordered list
def ordered_list(document: Document, items : list) -> None:
    for item in items:
        document.add_paragraph(item, style='ListNumber')



# Create table
def table(document: Document, header_row_data : list, data : list) -> None:
    table = document.add_table(rows=1, cols=len(header_row_data))
    table.style = 'Table Grid'
    hdr_cells = table.rows[0].cells
    for i, header in enumerate(header_row_data):
        hdr_cells[i].text = header
    for row in data:
        row_cells = table.add_row().cells
        for i, cell in enumerate(row):
            row_cells[i].text = cell



# Create documentation
def generate_documentation(CURRENT_SESSION):
    document = Document()
    document.add_heading('Documentation', level=1)
    data_files = [get_saves_directory().replace("\\", "/") + "/" + data for data in get_data_files(CURRENT_SESSION)]
    for i in get_modules():
        for j in data_files:
            if j.endswith(i[0] + ".json"):
                call_module_function(i[0], 'documentation', document, load_data(CURRENT_SESSION, i[0]))

    document.save(get_saves_directory().replace("\\", "/") + "/" + CURRENT_SESSION + "/documentation.docx")

    