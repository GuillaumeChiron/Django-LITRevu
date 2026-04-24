"""
URL configuration for booksproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView

import authentication.views
import app.views

urlpatterns = [
    # chemin admin
    path("admin/", admin.site.urls),
    # chemins: connexion, deconnexion et d'inscription
    path(
        "",
        LoginView.as_view(
            template_name="authentication/login_page.html",
            redirect_authenticated_user=True,
        ),
        name="login-page",
    ),
    path("logout/", LogoutView.as_view(), name="logout-page"),
    path("signup/", authentication.views.signup_page, name="signup-page"),
    path("home/", app.views.home_page, name="home-page"),
    # chemins: Ticket, Review
    # Ticket
    path("create-ticket/", app.views.create_ticket, name="create-ticket"),
    path("edit-ticket/<int:id>/", app.views.edit_ticket, name="edit-ticket"),
    path("delete-ticket/<int:id>/", app.views.delete_ticket, name="delete-ticket"),
    # Review
    path(
        "create-review/<int:id>/",
        app.views.create_review,
        name="create-review",
    ),
    path("edit-review/<int:id>/", app.views.edit_review, name="edit-review"),
    path("delete-review/<int:id>/", app.views.delete_review, name="delete-review"),
    path(
        "create-ticket-review/",
        app.views.create_ticket_review,
        name="create-ticket-review",
    ),
    # chemins : Dashboard, follow, unfollow
    path("dashboard-follow/", app.views.dashboard_follow, name="dashboard-follow"),
    path("follow-user/<int:id>/", app.views.follow_user, name="follow-user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
