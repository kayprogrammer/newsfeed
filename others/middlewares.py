from django.utils import timezone

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user
        tzname = request.COOKIES.get('localtz') # For visitors

        if user.is_authenticated: # For admin users
            tzname = user.timezone.name if user.timezone else None

        try:
            timezone.activate(tzname)
        except:
            timezone.deactivate()
        
        response = self.get_response(request)
        return response
        
        