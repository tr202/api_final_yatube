from django.urls import include, path

from rest_framework import routers

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, 'posts')
router_v1.register('groups', GroupViewSet, 'groups')
router_v1.register('follow', FollowViewSet, 'follow')
router_v1.register(r'posts\/[\d]+\/comments', CommentViewSet, 'comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
