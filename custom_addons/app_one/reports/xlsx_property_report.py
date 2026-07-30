from ast import literal_eval

from odoo import http
from odoo.http import request

import io
import xlsxwriter


class XlsxPropertyReport(http.Controller):

    @http.route('/property/excel/report/<string:property_ids>', type='http', auth="user")
    def download_property_excel_report(self,property_ids):

        property_ids = request.env['property'].browse(literal_eval(property_ids))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output,{'in_memory': True})
        worksheet = workbook.add_worksheet('Properties')
        header_format = workbook.add_format({'bold':True,'bg_color':'#D3D3D3','border':1,'align':'center'})
        body_format = workbook.add_format({'border':1,'align':'center'})
        price_format = workbook.add_format({'num_format':'$##,###00.00','border':1,'align':'center'})
        headers = ['name','postcode','date_availability','selling_price','garden']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        row_num = 1
        for row in property_ids:
            worksheet.write(row_num,0,row.name,body_format)
            worksheet.write(row_num,1,row.postcode,body_format)
            worksheet.write(row_num,2,row.date_availability,body_format)
            worksheet.write(row_num,3,row.selling_price,price_format)
            worksheet.write(row_num,4,'Yes' if row.garden else 'No')
            row_num += 1

        workbook.close()
        output.seek(0)
        file_name = 'Properties Report.xlsx'
        return request.make_response(
            output.getvalue(),
            headers =[
                ('Content-Type','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition',f'attachment;filename={file_name}'),
                ])