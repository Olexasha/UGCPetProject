from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("groups", GroupViewSet, basename="groups")
router.register("follow", FollowViewSet, basename="follow")

urlpatterns = [
    path(
        "posts/<int:post_pk>/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
        name="comments",
    ),
    path(
        "posts/<int:post_pk>/comments/<int:pk>/",
        CommentViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="comments-detail",
    ),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("", include("djoser.urls.jwt")),
]
