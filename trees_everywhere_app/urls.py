from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('planted_trees/', views.planted_trees_view, name='planted_trees'),
    path('tree/<int:tree_id>/', views.tree_details_view, name='tree_details'),
    path('add_planted_tree/', views.add_planted_tree_view, name='add_planted_tree'),
    path('user_planted_trees/', views.user_planted_trees_view, name='user_planted_trees'),
    path('api/user_planted_trees/', views.UserPlantedTreesAPIView.as_view(), name='user_planted_trees_api'),
]
