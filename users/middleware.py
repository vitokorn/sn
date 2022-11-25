from django.utils.timezone import now
from users.models import SNUser


class LastActivityTraceMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        member: SNUser = request.user
        if member.is_authenticated:
            member.last_activity = now()
            member.save()
        return response