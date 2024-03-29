from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_view, name='redirect'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('selection/', views.selection_view, name='selection'),

    path('player_selection/', views.player_selection_view, name='player selection'),
    path('delete_token/<str:hash>/', views.delete_character, name='delete character'),
    path('play/<str:hash>/', views.character_play_view, name='character play'),
    path('player_token_creation/', views.player_token_creation_view, name='player token'),
    path('edit_token/<str:hash>/', views.view_edit_token, name='token edit'),

    path('character_autosave/<str:hash>/<str:field>/', views.character_autosave, name='character autosave'),

    path('campaign_selection/', views.campaign_selection_view, name='campaign selection'),
    path('campaign_creation/', views.campaign_creation_view, name='create campaign'),
    path('campaign_edit/<str:hash>/', views.campaign_edit_view, name='campaign_edit'),
    path('campaign_delete/<str:hash>/', views.campaign_delete_view, name='campaign_edit'),
    path('campaign_userSearch/', views.userSearch, name='user search'),
    path('campaign_manage/<str:hash>/', views.campaig_manage_view, name='campaign manage'),

    path('campaign_autosave/<str:hash>/<str:field>/', views.campaign_autosave, name='campaign_autosave'),

    path('new_entity/at-<str:hash>/', views.new_entity_view, name='new entity'),
    path('entity_delete/<str:entity>/<str:campaign>/', views.entity_delete, name='delete entity'),
    path('entity_edit/<str:entity>/<str:campaign>/', views.entity_edit_view, name='edit entity'),

    path('sendMessage/<str:campaign>/<str:character>/', views.send_message, name='send message'),
    path('getMessage/<str:campaign>/', views.get_message, name='send message')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)