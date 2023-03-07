from rest_framework import routers
from .views import LinkViewSet

router = routers.SimpleRouter()
router.register('link', LinkViewSet)

urlpatterns = []
urlpatterns += router.urls
