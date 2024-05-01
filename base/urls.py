from  django.urls import path
from . import views

urlpatterns = [
    path("", views.Home,name="home"),
    path('signup',views.SignUp,name="signup"),
    path('signin',views.SignIn,name="signin"),
    path('logout',views.Logout,name="logout"),
    path('profile',views.Profile,name="profile"),
    path('setting',views.Setting,name="setting"),

    
]