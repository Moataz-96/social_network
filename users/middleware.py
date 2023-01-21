from django.utils.timezone import now
from users.models import CustomUser


class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            CustomUser.objects.filter(pk=request.user.pk).update(last_visit=now())
        response = self.get_response(request)
        return response
