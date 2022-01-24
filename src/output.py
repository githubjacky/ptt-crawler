import xlwings as xw
import json
from pdf_format import PDF


def output_excel(dataList, path):
    wb = xw.Book()
    sheet = wb.sheets[0]

    cols = list(dataList[0].keys())
    last_col = chr(65+(len(cols)-1))

    # set the format for the cell
    sheet.range(f'A1:{last_col}1').api.Font.Bold = True
    sheet.range(f'A1:{last_col}1').api.Font.Name = 'Microsoft YaHei'
    sheet.range(f'A1:{last_col}1').api.HorizontalAlignment = -4108
    sheet.range(f'A1:{last_col}1').api.VerticalAlignment = -4107
    sheet.range(f'A1:{last_col}1').row_height = 17.4

    # set the columns name
    ars = 65
    for item in cols:
        colName = chr(ars)
        sheet.range(f'{colName}1').value = item
        ars += 1
    sheet.autofit(axis='columns')
    # insert the value
    for i in range(len(dataList)):
        write = list(dataList[i].values())
        ars = 65
        for element in write:
            colName = chr(ars)
            if isinstance(element, list):
                total_comment = ''
                for index, comment in enumerate(element):
                    index = f'{index+1}.'
                    total_comment = total_comment + index + comment + ' '
                sheet.range(f'{colName}{i+2}').value = total_comment
            else:
                sheet.range(f'{colName}{i+2}').value = element
            ars += 1

    wb.save(path)


def output_json(dataList, path):
    file = open(path, 'w', encoding="utf-8")
    for data in dataList:
        jsonString = json.dumps(data, ensure_ascii=False)
        file.write(jsonString + '\n')
    file.close()


def output_pdf(dataList, path):
    pdf = PDF()
    pdf.set_margins(left=20, right=20, top=15)

    pdf.set_auto_page_break(auto = True, margin = 15)  # Set auto page break
    pdf.add_page()
    pdf.print_header()
    for index, dataDict in enumerate(dataList):
        items = list(dataDict.items())
        for item in items:
            if item[0] == 'title':
                pdf.paragraph_title(f'{index+1}', item[1])
            else:
                pdf.paragraph_body(item)
        pdf.ln(10)
        pdf.add_page()

    pdf.output(path)
