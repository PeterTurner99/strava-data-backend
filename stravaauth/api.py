from django.http import HttpResponse, JsonResponse
from ninja import Router
from django.views.decorators.csrf import ensure_csrf_cookie
from stravaauth.schema import ConnectSchema, MessageSchema
from django.contrib.auth import get_user_model, login
from ninja.security import django_auth
from strava.utils import send_initial_strava_post_auth

router = Router()
User = get_user_model()

@ensure_csrf_cookie
@router.post("callback/", response={200:MessageSchema, 401:MessageSchema})
def strava_connect(request, code_data: ConnectSchema):
    code = code_data.code
    exchange_data = {"code": code , "grant_type": "authorization_code"}
    data =  send_initial_strava_post_auth(exchange_data)
    if not data:
        return 401, {'message': 'Unable to authenticate', 'success': False}
    
    
    athlete = data.get('athlete')

    expires_at_int = data.get('expires_at')
    refresh_token = data.get('refresh_token')
    access_token = data.get('access_token')
    athlete_id = athlete.get('id')
    username = athlete.get('username') or (f"{athlete.get('firstname')}_{athlete.get('lastname')}")
    ftp = athlete.get('ftp')
    weight = athlete.get('weight')

    user_filter = User.objects.filter(athelete_id=athlete_id)
    if not user_filter.exists():
        user = User.objects.create(
            expires_at_int=expires_at_int,
            password="temp",
            refresh_token=refresh_token,
            access_token=access_token,
            athelete_id=athlete_id,
            username=username,
            ftp=ftp,
            weight=weight,
        )
        user.set_unusable_password()
        user.save()
    else:
        user = user_filter.first()
        user.refresh_token = refresh_token
        user.access_token = access_token
        user.save()
    login(request, user)
    return 200, {'message': 'Successfully authenticated', 'success': True}

@router.get("set-csrf-token/")
@ensure_csrf_cookie
def set_csrf_token(request):
    """
    We set the CSRF cookie on the frontend.
    """
    return HttpResponse()


@router.get('test/',auth=django_auth)
def test(request):
    return 200, {'message':'success'}


