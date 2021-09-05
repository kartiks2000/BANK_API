from django.urls import path

from . import views

urlpatterns = [
    path("ifsc_query/<str:ifsc>", views.IFSC_query.as_view(), name="ifsc_query"),
    path("leaderboard/", views.LeaderBoard.as_view(), name="leaderboard"),
    path("searchhistory/", views.SearchHistory.as_view(), name="searchhistory"),
    path("ifsc_hit", views.IFSC_Hit.as_view(), name="ifsc_hit"),
    path("url_hit", views.URL_Hit.as_view(), name="url_hit"),
]
