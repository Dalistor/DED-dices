from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_view, name='redirect'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),

    path('selection/', views.selection_view, name='selection'),

    path('player_selection/', views.player_selection_view, name='player selection'),
    path('delete_character/<str:hash>/', views.delete_character, name='delete character'),
    path('play/<str:hash>/', views.character_play_view, name='character play'),
    path('player_token_creation/', views.player_token_creation_view, name='player token'),
    path('edit_token/<str:hash>/', views.view_edit_token, name='token edit'),

    path('character_autosave/<str:hash>/<str:field>/', views.character_autosave, name='character autosave'),

    path('campaign_creation/'. views.campaign_creation_view, name='create campaign')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)