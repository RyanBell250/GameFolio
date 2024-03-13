from django.urls import path
from gamefolio_app import views

app_name = 'gamefolio_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('register_profile/', views.MyRegistrationView.as_view(), name='register_profile'),
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    path('lists/', views.ListsView.as_view(), name='lists'),
    path('list/<author_username>/<list_title>', views.ListView.as_view(), name='list'),

]