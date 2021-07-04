import json, jwt, bcrypt

from django.core import exceptions
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from my_settings import SECRET_KEY
from user.models import Account

class login_decorator:
    def __init__(self, func):
        self.func = func

    def __call__(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('authorization')
            payload = jwt.decode(access_token, SECRET_KEY, algorithms = 'HS256')
            user    = Account.objects.get(id=payload['account_id'])
            request.user = user
            return self.func(self, request, *args, **kwargs)

        # except jwt.exceptions.DecodeError:
            # return JsonResponse({"MESSAGE":"INVALIED_TOKEN"}, status=400)
        except Account.DoesNotExist:
            return JsonResponse({"MESSAGE":"INVALID_USER"}, status=401)


