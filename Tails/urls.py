from django.contrib import admin
from django.urls import include, path

from Postcodes.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path("api/", include("Postcodes.urls")),
    path('admin/', admin.site.urls),
]