from django.urls import path
from gamefolio_app import views

app_name = 'gamefolio_app'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    
    path('accounts/register/', views.MyRegistrationView.as_view(), name='registration_register'),
    path('register_profile/', views.RegisterProfileView.as_view(), name='register_profile'),  
    
    path('profile/<username>/', views.ProfileView.as_view(), name='profile'),
    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),
    
    path('lists/', views.ListsView.as_view(), name='lists'),
    path('create_list/', views.CreateListView.as_view(), name='create_list'),
    path('<str:author_username>/<str:list_title>/<slug:slug>/delete/', views.ListDeleteView.as_view(), name='list_delete'),
    path('list/<author_username>/<list_title>/<slug:slug>', views.ListView.as_view(), name='list'),
    path('list/<str:author_username>/<str:list_title>/<str:slug>/remove_game/', views.RemoveGameView.as_view(), name='remove_game'),
    
    path('search/', views.SearchView.as_view(), name='search'),
    path('404/', views.NotFoundView.as_view(), name='404'),
    
    path('game/<slug:game_id>/', views.GamePageView.as_view(), name="game"),
]

