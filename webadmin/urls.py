from django.urls import path
from .views import UpdateDeleteProductView, CreateProductView, GetProductBids

app_name = "webadmin"

urlpatterns = [
    # routes for jwt auth
    path('update-product/<slug:slug>/',
         UpdateDeleteProductView.as_view(), name="update"),
    path('create-product/', CreateProductView.as_view(), name="create"),
    path('get-product-bids/<slug:slug>/', GetProductBids.as_view(), name="product-bids"),
]
