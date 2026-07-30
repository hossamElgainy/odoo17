
from odoo import http

class test_api(http.Controller):

    @http.route("/api/test",methods=["GET"],type="http",auth="none",csrf=False)
    def test_endpoint(self):
        print(" this is a test endpoint ")