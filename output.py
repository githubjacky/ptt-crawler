import xlwings as xw
import json


def output_excel(dataList, path):
    wb = xw.Book()
    sheet = wb.sheets[0]
    # set the format for the cell
    sheet.range('A1:H1').api.Font.Bold = True
    sheet.range('A1:H1').api.Font.Name = 'Microsoft YaHei'
    sheet.range('A1:H1').api.HorizontalAlignment = -4108
    sheet.range('A1:H1').api.VerticalAlignment = -4107
    sheet.range('A1:H1').row_height = 17.4

    # set the title
    sheet.range('A1').value = 'date'
    sheet.range('A1').column_width = 8
    sheet.range('B1').value = 'title'
    sheet.range('B1').column_width = 18
    sheet.range('C1').value = 'article content'
    sheet.range('C1').column_width = 30
    sheet.range('D1').value = 'push'
    sheet.range('D1').column_width = 8
    sheet.range('E1').value = 'boo'
    sheet.range('E1').column_width = 8
    sheet.range('F1').value = 'arrow'
    sheet.range('F1').column_width = 8
    sheet.range('G1').value = 'total_comment'
    sheet.range('G1').column_width = 18
    sheet.range('G1').value = 'not-boo'
    sheet.range('G1').column_width = 10

    for i, data in enumerate(dataList):
        sheet.range(f'A{i+2}').value = list(data.values())

    wb.save(path)


def output_json(dataList, path):
    file = open(path, 'w', encoding="utf-8")
    for data in dataList:
        jsonString = json.dumps(data, ensure_ascii=False)
        file.write(jsonString + '\n')
    file.close()
