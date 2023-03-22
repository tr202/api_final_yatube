import re

from http import HTTPStatus

from django.db import IntegrityError

from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import filters

from .permissions import IsOwnerOrReadOnly
from posts.models import Comment, Follow, Group, Post
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          GroupSerializer,
                          PostSerializer)

EXTRACT_POST_ID_PATTERN = r'posts\/([0-9]+)'


class BaseViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    ...


class FollowViewSet(BaseViewSet):
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticated)
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=following__username',)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=HTTPStatus.CREATED, headers=headers)
        except IntegrityError:
            return Response('Already exists', HTTPStatus.BAD_REQUEST)

    def get_queryset(self):
        username = self.request.GET.get('username')
        if username:
            return Follow.objects.filter(user__username=username)
        return Follow.objects.filter(
            user=self.request.user).select_related('following', 'user')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    serializer_class = CommentSerializer

    def get_post_id(self):
        pattern = EXTRACT_POST_ID_PATTERN
        return re.findall(pattern, self.request.path)[0]

    def get_queryset(self):
        return Comment.objects.filter(
            post=self.get_post_id()).select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post_id=self.get_post_id())


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all().select_related('author')
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.AllowAny,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ('get', 'post',)
