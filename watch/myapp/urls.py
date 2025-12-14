from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings  # <--- THIS WAS MISSING


urlpatterns = [
    path('', views.index, name='index'),
    
    # 2. Signup and Login
    # We use 'views.signup_view', NOT 'views.signup'
    path('signup/', views.signup_view, name='signup'),
    
    # We use 'views.login_view', NOT 'views.login'
    path('login/', views.login_view, name='login'),

    path('logout/', views.logout_view, name='logout'),

    path('order-now/', views.catalog_view, name='catalog'),
    path('place-order/', views.place_order, name='place_order'),
]# Ye line zaroor add karein:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)