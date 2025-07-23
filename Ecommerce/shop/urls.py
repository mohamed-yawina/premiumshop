from django.urls import path
from .views import index, detail, checkout, confirmation, login_view, register_view, logout_view, contact_view, about_view


urlpatterns = [
    path('', index, name='home'),
    path('products/<int:myid>/', detail, name='detail'),  
    path('checkout/', checkout, name='checkout'),
    path('confirmation/', confirmation, name='confirmation'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('contact/', contact_view, name='contact'),
    path('about/', about_view, name='about'),
]