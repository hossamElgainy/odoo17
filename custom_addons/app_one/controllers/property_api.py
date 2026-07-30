import json
from urllib.parse import parse_qs

from Demos.mmapfile_demo import offset

from odoo import http
from odoo.http import request
from ..utils.api_response import ApiResponse



class PropertyApi(http.Controller):
    @http.route('/api/v1/property',methods=["POST"], type='http', auth='none',csrf=False)
    def create_property(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        errors = {}
        if not vals.get('name'):
            errors['name'] = 'The Name Is Required'

        if not vals.get('postcode'):
            errors['postcode'] = 'postcode Is Required'

        if errors:
            return ApiResponse.error('', 400, errors)

        try:
            res = request.env['property'].sudo().create(vals)
            if res:
                return ApiResponse.success('Property Created')

        except Exception as error:
            return ApiResponse.error('', 500, error)

    @http.route('/api/v1/property/<int:id>',methods=["PUT"],type='http',auth='none',csrf=False)
    def update_property(self,id):
        property_record = request.env['property'].sudo().search([('id','=',id)])
        if not property_record:
            return ApiResponse.error('', 404, "Error:) Property Not Found")

        args = request.httprequest.data.decode()
        vals = json.loads(args)
        try:
            res = property_record.write(vals)
            if res:
                return ApiResponse.success('Property Updated', {
                        "id":property_record.id,
                        "name":property_record.name,
                        "postcode":property_record.postcode,
                    })

        except Exception as error:
            return ApiResponse.error('', 500, error)

    @http.route('/api/v1/property/<int:id>',methods=['GET'],type='http',auth='none',csrf=False)
    def get_property(self,id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=',id)])
            if not property_record:
                return ApiResponse.error('', 404, "Error:) Property Not Found")

            return ApiResponse.success('', {
                "id": property_record.id,
                "name": property_record.name,
                "postcode": property_record.postcode,
            })
        except Exception as error:
            return ApiResponse.error('', 500, error)

    @http.route('/api/v1/property/<int:id>',methods=['Delete'],type='http',auth='none',csrf=False)
    def delete_property(self,id):
        try:
            property_record = request.env['property'].sudo().search([('id', '=',id)])
            if not property_record:
                return ApiResponse.error('', 500, "Error:) Property Not Found")

            property_record.unlink()
            return ApiResponse.success('Property Deleted Successfully' )
        except Exception as error:
            return ApiResponse.error('', 500, error)

    @http.route('/api/v1/properties',methods=['GET'],type='http',auth='none',csrf=False)
    def list_properties(self):
        try:
            params = parse_qs(request.httprequest.query_string.decode('utf-8'))
            property_domain = []
            if params.get('state'):
                property_domain += [('state','=',params.get('state')[0])]

            page = max(int(params.get("page", [1])[0]), 1)
            limit = min(max(int(params.get("limit", [5])[0]), 1), 10)

            offset = (page - 1) * limit

            Property = request.env["property"].sudo()
            property_records = Property.search(property_domain,order='id Asc',offset=offset,limit=limit)
            property_total_count = Property.search_count(property_domain)
            if not property_records:
                return ApiResponse.paginated()
            response = [{
                "id":property_record.id,
                "name":property_record.name,
                "postcode":property_record.postcode,
                "state":property_record.state,
                "description":property_record.description,
                "owner_id":property_record.owner_id.name ,
            }for property_record in property_records]
            return ApiResponse.paginated('',response,page,limit,property_total_count,200)

        except Exception as error:
            return ApiResponse.error('', 500, error)
