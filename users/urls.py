
from django.urls import path
from . import views
from django.conf.urls.static import static
from website import settings



app_name = "users"
urlpatterns = [
    path("signup/", views.account_signup , name="signup"),
    path("login/", views.account_login , name="login"),
    path("logout/", views.account_logout , name="logout"),
    path("account/<int:pk>/", views.account_view , name="account"),
    path("search/<query>" ,views.search_view , name="search"),
    path("account/edit/" ,views.AccountUpdateView.as_view() , name="account_edit"),
    path("notification_delete/<notification_id>" ,views.delete_notification , name="notification-delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
