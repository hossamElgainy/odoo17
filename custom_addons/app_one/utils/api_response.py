from odoo.http import request


class ApiResponse:

    @staticmethod
    def paginated(message=None, data=None, page=1, limit=10, total_records=0, status=200):
        total_pages = (total_records + limit - 1) // limit

        return request.make_json_response({
            "success": True,
            "message": message,
            "data": data,
            "pagination": {
                "page": page,
                "limit": limit,
                "total_records": total_records,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1,
                "next_page": page + 1 if page < total_pages else None,
                "previous_page": page - 1 if page > 1 else None,
            }
        }, status=status)
    @staticmethod
    def success(message=None, data=None, status=200):
        return request.make_json_response({
            "success": True,
            "message": message,
            "data": data
        }, status=status)

    @staticmethod
    def error(message=None, status=400, errors=None):
        return request.make_json_response({
            "success": False,
            "message": message,
            "errors": errors or {}
        }, status=status)