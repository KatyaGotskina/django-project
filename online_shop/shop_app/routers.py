from rest_framework import routers 
from .views import ProductViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'category', CategoryViewSet)