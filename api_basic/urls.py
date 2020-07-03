from django.urls import path
from .views import article_list,article_detail,ArticleAPIView,ArticleDetails,GenericAPIView
urlpatterns = [
    path('article/', article_list),
    # path('article/', ArticleAPIView.as_view()),
    path('generic/article/<int:id>/', GenericAPIView.as_view()),
    # path('details/<int:pk>/', article_detail),
    path('details/<int:pk>/', ArticleDetails.as_view()),
]
