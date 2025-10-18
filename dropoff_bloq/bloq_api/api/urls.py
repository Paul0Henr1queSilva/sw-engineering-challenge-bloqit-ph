from rest_framework.routers import SimpleRouter
from .views import RentViewSet, LockerViewSet, BloqViewSet

route = SimpleRouter(trailing_slash=False)
route.register(r'rents', RentViewSet, basename='rent')
route.register(r'lockers', LockerViewSet, basename='locker')
route.register(r'bloqs', BloqViewSet, basename='bloq')

urlpatterns = route.urls