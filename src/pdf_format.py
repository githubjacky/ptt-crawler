from fpdf import FPDF
from numpy import info


class PDF(FPDF):
    def print_header(self):
        title = '爬蟲結果'
        self.add_font('cf', '', '..\\res\\kaiu.ttf', uni=True)
        self.set_font('cf', size=30)
        title_w = self.get_string_width(title) + 20  # calculate the width of title
        self.set_x((self.w - title_w) / 2)  # the x postion of the header

        #self.set_draw_color(0, 80, 180)   # header border color
        self.set_fill_color(235, 203, 139) # header background color
        self.set_text_color(46, 52, 64)  # header text color
        self.set_line_width(1)  # thichness of frame

        self.cell(title_w, 10, title, border=0, ln=1,
            align='C', fill=1)
        self.ln(10)   # line break


    def footer(self):
        self.set_y(-15)  # set the postion of the footer
        self.set_text_color(76, 86, 106)
        self.set_font('helvetica', 'I', 6)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')


    def paragraph_title(self, p_num, p_title):
        # self.add_font('cf', '', 'C:\\Windows\\Fonts\\kaiu.ttf', uni=True)
        self.set_font('cf', size=18)
        self.set_fill_color(129, 161, 193)  # background color

        chapter_title = f'{p_num}. {p_title}'
        self.multi_cell(0, 5, chapter_title, ln=1, fill=1)
        self.ln(10)


    def paragraph_body(self, item):
        sub_title = item[0]
        paragraph = item[1]
        if (not isinstance(paragraph, list)) or (isinstance(paragraph, list) and len(paragraph) != 0):
            # subtitle
            # self.add_font('cf', '', 'C:\\Windows\\Fonts\\kaiu.ttf', uni=True)
            self.set_font('cf', size=12)
            self.set_fill_color(136, 192, 208)  # background color
            sub_title_w = self.get_string_width(sub_title)+3  # calculate the width of title
            self.cell(sub_title_w, 5, sub_title, ln=1, fill=1)
            # paragraph body
            if isinstance(paragraph, list):
                for content in paragraph:
                    self.set_text_color(59, 66, 82)
                    self.multi_cell(0, 5, content, ln=1)
            else:
                self.set_text_color(59, 66, 82)
                self.multi_cell(0, 5, str(paragraph), ln=1)
