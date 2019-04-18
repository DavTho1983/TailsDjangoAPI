from django.urls import path

from .views import PostcodessAPIListView, PostcodesAPIID, PostcodesWithinRadius

urlpatterns = [
    path(
        "<str:postcode>/<int:radius_km>",
        PostcodesWithinRadius.as_view(),
        name="results_api_radius",
    ),
    path("", PostcodessAPIListView.as_view(), name="results_api_list"),
    path("<int:pk>", PostcodesAPIID.as_view(), name="results_api_detail"),
]
