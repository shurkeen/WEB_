from app import views
from django.urls import path
from django.conf.urls.static import static
from askme import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('question/<int:question_id>', views.question, name='question'),
    path('ask', views.ask, name='ask'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('tag/<str:tag_id>', views.tag, name='tag'),
    path('like/', views.like, name='like'),
    path('like_answer/', views.like_answer, name='like_answer'),
    path('correct/', views.correct, name='correct'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATICFILES_DIRS[0]) \
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
