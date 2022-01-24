from fpdf import FPDF


pdf = FPDF()
pdf.add_page()
font_path = '../res/chinese_font/cwTex_rttf.ttf'

pdf.add_font('cwTex_r', '', font_path, uni=True)
pdf.set_font('cwTex_r', size=15)
pdf.set_left_margin(10)
pdf.set_right_margin(10)
str1 = '嘿嘿達瑞斯開剁aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
str1 += 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
str1 += 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
#pdf.cell(h=100, w=10, txt=str1, ln=1, align='L')
pdf.cell(h=10, w=10, txt='葉秀軒好辦aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', ln=1, align='L')
pdf.ln()
pdf.cell(h=10, w=10, txt='葉秀軒好辦', ln=1, align='L')
pdf.cell(h=0, w=10, txt='葉秀軒好辦', ln=1, align='L')
pdf.cell(h=0, w=10, txt='葉秀軒好辦', ln=1, align='L')

pdf.output('test.pdf')
