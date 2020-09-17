from django.urls import path

from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('index', views.index, name='index'),
    path('signup', views.signupView, name='signup'),
    path('login', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('add', views.addGift, name='add'),
    path('purchase/<gift_id>', views.purchaseGift, name='purchase'),
    path('unpurchase/<gift_id>', views.unpurchaseGift, name='unpurchase'),
    path('deletegift/<gift_id>', views.deleteGift, name='deletegift'),
    path('generatereport', views.generateReport, name='generatereport'),
    path('deletecomplete', views.deleteCompleted, name='deletecomplete'),
    path('deleteall', views.deleteAll, name='deleteall')
]
