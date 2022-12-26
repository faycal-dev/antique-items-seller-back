from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from store.models import Product
from .serializers import AutoBidSerializer

# ---------------------------------------custom permission----------------------------------------------------------------


class UserbidWritePermission(permissions.BasePermission):
    message = "Editing bid is restricted the author only!"

    # in order to modify a bid you need to be the owner of it
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class UserbidReadPermission(permissions.BasePermission):
    message = "Reading bid is restricted the author or admin only!"

    # in order to modify a bid you need to be the owner of it
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff


# -------------------------------------------------------------------------------------------------------------------------

class GetBid(APIView, UserbidReadPermission):
    permission_classes = (UserbidReadPermission,)

    def get(self, request, slug):
        product_instance = get_object_or_404(Product, slug=slug)
        bid_instance = models.Bid.objects.filter(
            product=product_instance, user=request.user)
        auto_bid_instance = models.Auto_bid.objects.filter(
            user=request.user, products=product_instance)

        if(len(bid_instance) > 0 and len(auto_bid_instance) > 0):
            auto_bid = {
                "is_auto_bidding_active": True,
                "amout_left": auto_bid_instance[0].amout_left}

            return Response({"bid": bid_instance[0].bidding_amount,
                             "auto_bid": auto_bid}, status=status.HTTP_200_OK)

        elif (len(bid_instance) > 0):
            auto_bid = {"is_auto_bidding_active": False}
            return Response({"bid": bid_instance[0].bidding_amount,
                             "auto_bid": auto_bid}, status=status.HTTP_200_OK)

        elif (len(auto_bid_instance) > 0):
            auto_bid = {
                "is_auto_bidding_active": True,
                "amout_left": auto_bid_instance[0].amout_left}
            return Response({"bid": None,
                             "auto_bid": auto_bid}, status=status.HTTP_200_OK)

        else:
            auto_bid = {"is_auto_bidding_active": False}
            return Response({"bid": None,
                             "auto_bid": auto_bid}, status=status.HTTP_200_OK)


class GetAutoBid(generics.ListAPIView, UserbidReadPermission):
    permission_classes = (UserbidReadPermission, )
    serializer_class = AutoBidSerializer

    def get_queryset(self):
        return models.Auto_bid.objects.filter(user=self.request.user)


class SetAutoBidding(APIView, UserbidWritePermission):
    permission_classes = (UserbidWritePermission, )

    def post(self, request):
        bidding_max_amount = request.data["bidding_max_amount"]
        bidding_notification_threshold = request.data["bidding_notification_threshold"]

        try:
            auto_bid = models.Auto_bid.objects.filter(
                user=request.user)

            if (auto_bid.exists()):
                auto_bid_instance = models.Auto_bid.objects.get(
                    user=request.user)
                amout_left = auto_bid_instance.amout_left + \
                    (bidding_max_amount - auto_bid_instance.bidding_max_amount)

                auto_bid_instance.bidding_max_amount = bidding_max_amount
                auto_bid_instance.amout_left = amout_left
                auto_bid_instance.bidding_notification_threshold = bidding_notification_threshold
                auto_bid_instance.save()
                return Response(
                    {"success": "auto bid updated successfully"},
                    status=status.HTTP_200_OK
                )
            else:
                auto_bid_instance = models.Auto_bid.objects.create(user=request.user, bidding_max_amount=bidding_max_amount,
                                                                   amout_left=bidding_max_amount,
                                                                   bidding_notification_threshold=bidding_notification_threshold)
                return Response(
                    {"success": "auto bid created successfully"},
                    status=status.HTTP_201_CREATED
                )
        except Exception as e:
            return Response(
                {'error': 'Something went wrong when trying to add a auto bid'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ToggleProductAutoBid(APIView, UserbidWritePermission):
    permission_classes = (UserbidWritePermission, )

    def post(self, request, slug):
        product_instance = get_object_or_404(Product, slug=slug)
        try:
            user_auto_bid = models.Auto_bid.objects.filter(
                user=request.user)
            if (user_auto_bid.exists()):
                product_auto_bid = models.Auto_bid.objects.filter(
                    user=request.user, products=product_instance)
                if (product_auto_bid.exists()):
                    user_auto_bid[0].products.remove(product_instance)
                    return Response(
                        {'success': 'Product auto bidding remouved'},
                        status=status.HTTP_200_OK
                    )
                else:
                    user_auto_bid[0].products.add(product_instance)
                    return Response(
                        {'success': 'Product auto bidding added'},
                        status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {'error': 'You need to configure auto bidding first'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            print(e)
            return Response(
                {'error': 'Something went wrong when trying to toggle product from auto bid'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
