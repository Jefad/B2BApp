from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.auth_urls')),
    path('api/products/', include('products.urls')),
    path('api/purchase/', include('users.purchase_urls'))
]
