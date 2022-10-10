from .models import Visitor
from datetime import datetime 

def visit_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        def get_client_ip(request):
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')
            return ip
        ip = get_client_ip(request)
        Visitor.objects.get_or_create(ip_add = ip)
        visitor = Visitor.objects.get(ip_add = ip)
        visitor.last_visit = datetime.now()
        visitor.save()
        

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware