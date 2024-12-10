from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, Border, Side, PatternFill

def create_xl_sample(): 
    # Criar um novo Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "test"

    # Estilos gerais
    bold_font = Font(bold=True, size=12)
    header_font = Font(bold=True, size=14)
    center_alignment = Alignment(horizontal="center", vertical="center")
    border = Border(left=Side(style="thin"), right=Side(style="thin"), top=Side(style="thin"), bottom=Side(style="thin"))
    gray_fill = PatternFill(start_color="D9D9D9", end_color="D9D9D9", fill_type="solid")

    # Cabeçalho principal
    ws.merge_cells("A1:F1")
    ws["A1"].value = "ORDER"
    ws["A1"].alignment = center_alignment
    ws["A1"].font = header_font

    # Informações do documento
    info_data = [
        ("NUMBER DOC.:", "00001", "CLIENT:", "CLIENT NAME", "RESPONSABILITY OF:", "NAME"),
        ("PART NUMBER:", "1 123 456 789", "CLIENT VERSION:", "V01", "APROVED BY:", "ENGINEER"),
        ("DESCRIPTION:", "DESCRIPTION PART NUMBER", "INTERNAL VERSION:", "V02", "DATE:", "05/12/2024"),
    ]

    # Column styles
    for row_idx, row_data in enumerate(info_data, start=2):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.border = border
            cell.alignment = center_alignment
            if col_idx % 2 != 0: 
                cell.fill = gray_fill
                cell.font = bold_font

    # Titles
    column_headers = ["Column1", "Column2", "Column3", "Column4", "Column5", "Column6"]
    for col_idx, col_name in enumerate(column_headers, start=1):
        cell = ws.cell(row=5, column=col_idx, value=col_name)
        cell.font = bold_font
        cell.alignment = center_alignment
        cell.fill = gray_fill
        cell.border = border

    # Datatable
    data_rows = [
        [f"data_column{i}.{j}" for i in range(1, 7)] for j in range(1, 13)
    ]

    for row_idx, row_data in enumerate(data_rows, start=6):
        for col_idx, value in enumerate(row_data, start=1):
            cell = ws.cell(row=row_idx, column=col_idx, value=value)
            cell.alignment = center_alignment
            cell.border = border

    # Width adjustments
    for col_letter in "ABCDEF":
        ws.column_dimensions[col_letter].width = 20

    wb.save("example/default_search/test.xlsx")

def create_env_file():
    with open(".env", "w") as file:
        file.write("DEFAULT_SAVEPATH=example/default_savepath\n")
        file.write("SEARCH_PATH=example/default_search\n")
        file.write("SECRET_KEY=''\n")
        file.write("DEBUG=True\n")


def start_app():
    create_env_file()
    create_xl_sample()


start_app()