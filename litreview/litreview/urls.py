"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import feed.views
import authentication.views
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', LoginView.as_view(template_name='authentication/login.html',
                               redirect_authenticated_user=True), name='login'),

    path('logout/', authentication.views.logout_user, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),

    path('home/', feed.views.home, name='home'),

    path('subscription/', authentication.views.subscription_page, name='subscription'),
    path('unfollow/<int:pk>/', authentication.views.unfollow, name='unfollow'),

    path('posts/', feed.views.posts, name='posts'),

    path('tickets/add/', feed.views.ticket_create, name='ticket_create'),
    path('tickets/<int:ticket_id>/', feed.views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:ticket_id>/update/', feed.views.ticket_update, name='ticket_update'),
    path('tickets/<int:ticket_id>/delete/', feed.views.ticket_delete, name='ticket_delete'),

    path('ticket_reviews/add/', feed.views.ticket_review_create, name='ticket_review_create'),
    path('tickets/<int:ticket_id>/reviews/add/', feed.views.review_create, name='review_create'),
    path('reviews/<int:review_id>/update/', feed.views.review_update, name='review_update'),
    path('reviews/<int:review_id>/', feed.views.review_detail, name='review_detail'),
    path('reviews/<int:review_id>/delete/', feed.views.review_delete, name='review_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
