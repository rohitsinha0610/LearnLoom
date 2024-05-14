from django.urls import path 
from . import views


urlpatterns = [
    path('',views.landing_view,name='landing'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard'),
    path('profile/',views.profile_view,name='profile'),
    path('dashboard/join_class/', views.join_class_view, name='join_class'),  # Add this line for join class functionality
    path('dashboard/create_class/', views.create_class_view, name='create_class'),
    path('dashboard/classroom/<int:pk>/', views.classroom_view, name='classroom_page'),
    path('dashboard/classroom/assignments/', views.assignment_view, name='assignment_page'),
    path('dashboard/settings/', views.settings_view, name='settings'),
    path('dashboard/calendar/', views.calendar_view, name='calendar'),
    #path('dashboard/class/<int:pk>/', views.classroom_view, name='class_page'),
    path('dashboard/classroom/people/', views.add_people_view, name='people_page')
]
