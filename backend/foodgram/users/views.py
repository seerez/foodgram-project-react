from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import FollowSerializer
from .serializers import CustomUsersSerializer
from users.models import Follow


User = get_user_model()


class UsersViewSet(UserViewSet):
    serializer_class = CustomUsersSerializer

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,)
            )
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated, )
    )
    def subscribe(self, request, id=None):
        author = get_object_or_404(User, id=id)
        user = request.user
        check_subscribe = Follow.objects.filter(
            user=user, author=author).exists()
        if request.method == 'POST':
            if check_subscribe or user == author:
                return Response({
                    'errors': ('You have already subscribed')
                }, status=status.HTTP_400_BAD_REQUEST)
            subscribe = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
                subscribe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if check_subscribe:
            Follow.objects.filter(user=user, author=author).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'You are not subscribed to this user'
        }, status=status.HTTP_400_BAD_REQUEST)







# from django.shortcuts import get_object_or_404
# from rest_framework import status, views
# from rest_framework.generics import ListAPIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from recipes.pagination import CustomPagination
# from users.models import Subscription, User
# from users.serializers import SubscribeSerializer, SubscriptionSerializer


# class SubscriptionViewSet(ListAPIView):
#     serializer_class = SubscriptionSerializer
#     pagination_class = CustomPagination
#     permission_classes = (IsAuthenticated,)

#     def get_queryset(self):
#         user = self.request.user
#         return user.follower.all()


# class SubscribeView(views.APIView):
#     pagination_class = CustomPagination
#     permission_classes = (IsAuthenticated,)

#     def post(self, request, pk):
#         author = get_object_or_404(User, pk=pk)
#         user = self.request.user
#         data = {'author': author.id, 'user': user.id}
#         serializer = SubscribeSerializer(
#             data=data, context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)

#     def delete(self, request, pk):
#         author = get_object_or_404(User, pk=pk)
#         user = self.request.user
#         subscription = get_object_or_404(
#             Subscription, user=user, author=author
#         )
#         subscription.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
