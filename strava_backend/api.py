from ninja import NinjaAPI


api = NinjaAPI(csrf=True)

api.add_router('/auth/','stravaauth.api.router')
api.add_router('/','strava.api.router')


