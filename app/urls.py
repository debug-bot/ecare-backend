from django.urls import path, include
from django.contrib import admin
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('tests',views.ShowTestsViewSet,basename='tests')
router.register('labs',views.ShowLabsViewSet,basename='labs')
router.register('pharmacies',views.ShowPharmaciesViewSet,basename='pharmacies')
router.register('address',views.SubmitPatientData,basename='address')
router.register('getaddress',views.GetPatientData,basename='get_address')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', views.CartItemViewSet.as_view(), name='cart'),
    path('order/', views.OrderPlaceViewSet.as_view(), name='order'),
    path('', include(router.urls))
]