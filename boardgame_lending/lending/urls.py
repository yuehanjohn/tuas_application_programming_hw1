from django.urls import path
from . import views
from .views import SignUpView


urlpatterns = [
    path('', views.index, name='index'),
    path('borrow/<int:game_id>/', views.borrow_game, name='borrow_game'),
    path('return/<int:loan_id>/', views.return_game, name='return_game'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('add_game/', views.add_game, name='add_game'),
]

