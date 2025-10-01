from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VPNServerViewSet, GameViewSet, ConnectionViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'servers', VPNServerViewSet)
router.register(r'games', GameViewSet)
router.register(r'connections', ConnectionViewSet, basename='connection')
router.register(r'profile', UserProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
]