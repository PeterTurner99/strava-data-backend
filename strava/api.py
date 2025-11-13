from ninja import Router
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import get_user_model
from ninja.security import django_auth

router = Router()
User = get_user_model()


@ensure_csrf_cookie
@router.get('pull_activities/', auth=django_auth)
def pull_activities(request):
    user = request.user
    access_token = user.get_access_token()
    
    
    return 200, {'message':'success'}