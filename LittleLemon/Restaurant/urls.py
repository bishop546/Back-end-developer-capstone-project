from django.urls import path, include
from .views import SingleMenuItemView, MenuItemsView, BookingView, UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'tables', BookingView)
router.register(r'users', UserView, basename='user')  

urlpatterns = [
    path('menu/', MenuItemsView.as_view(), name='menu-items'),
    path('menu/<int:pk>/', SingleMenuItemView.as_view(), name='single-menu-item'),
    path('booking/', include(router.urls)),
    path('users/', include(router.urls)),
]