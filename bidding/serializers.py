from rest_framework import serializers
from users.serializers import UserSerializer

from .models import Bid, Auto_bid


class BidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bid
        fields = ["bidding_amount"]

class AdminBidSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Bid
        fields = ["bidding_amount", "user"]


class AutoBidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auto_bid
        fields = ["bidding_max_amount",
                  "amout_left", "bidding_notification_threshold"]