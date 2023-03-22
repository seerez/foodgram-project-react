from django.urls import include, path

from users.views import SubscriptionViewSet, SubcribeView

urlpatterns = [
    path('users/subscriptions/', SubscriptionViewSet.as_view()),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/<int:pk>/subscribe/', SubcribeView.as_view())
]
