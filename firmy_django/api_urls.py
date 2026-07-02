from rest_framework.routers import DefaultRouter

from .views import FirmaViewSet, SprawozdanieFinansoweViewSet


router = DefaultRouter()
router.register("firmy", FirmaViewSet, basename="api-firmy")
router.register("sprawozdania", SprawozdanieFinansoweViewSet, basename="api-sprawozdania")

urlpatterns = router.urls
