from django.urls import path
from .bid_views import AddBidView
from .auto_bid_views import GetBid, SetAutoBidding, ToggleProductAutoBid, GetAutoBid

app_name = "bidding"

urlpatterns = [
    # routes for bidding
    path('', AddBidView.as_view(), name="bid"),
    path("get-bid/<slug:slug>/", GetBid.as_view(), name="get bid"),
    path("get-auto-bid/", GetAutoBid.as_view(), name="get bid"),
    path("set-auto-bid-config/", SetAutoBidding.as_view(), name="auto bid config"),
    path("toggle-product-auto-bid/<slug:slug>/",
         ToggleProductAutoBid.as_view(), name="toggle product from auto bid"),


]
