from .models import Visitor
import datetime

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
        if (request.path == '/nera/products/') and (request.method == 'GET'):
            ip = get_client_ip(request)
            Visitor.objects.get_or_create(ip_add = ip ,last_visit = datetime.datetime.now().strftime("%Y-%m-%d"))
            # visitor = Visitor.objects.get(ip_add = ip)
            # visitor.last_visit = datetime.date.today
            # visitor.save()
        
        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    return middleware