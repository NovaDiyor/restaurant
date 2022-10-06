from django.urls import path
from .views import *
urlpatterns = [
    path('menu/', GetMenyu.as_view()),
    path('getall/<int:pk>/', GetAll.as_view()),
    path('register/', Register),
    path('login/', login_view),
    path('orderitem_create/', OrderItemcreate),
    path('order_create/', Ordercreated),
    path('delete/<int:pk>/', Delete),

]