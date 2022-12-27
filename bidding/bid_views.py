from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import models
from store.models import Product
from .utils import Util
# ---------------------------------------custom permission----------------------------------------------------------------


class UserbidWritePermission(permissions.BasePermission):
    message = "Editing bid is restricted the author only!"

    # in order to modify a bid you need to be the owner of it
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


# -------------------------------------------------------------------------------------------------------------------------


class AddBidView(APIView, UserbidWritePermission):
    permission_classes = (UserbidWritePermission,)

    def verify_auto_bid(self, request, product, bid):
        users_with_auto_bid_active = models.Auto_bid.objects.filter(
            products=product, amout_left__gt=0).order_by("-amout_left")

        if (users_with_auto_bid_active.exists()):
            if (len(users_with_auto_bid_active) == 1):
                if (not users_with_auto_bid_active[0].user == request.user):
                    print("user not owner of autobid")
                    winner_bid = models.Bid.objects.get(
                        user=users_with_auto_bid_active[0].user, product=product)
                    # if the user auto bidding hase the needed amount
                    if (users_with_auto_bid_active[0].amout_left >= (bid.bidding_amount - winner_bid.bidding_amount + 1)):
                        print("the other user has the amount")
                        users_with_auto_bid_active[0].amout_left = users_with_auto_bid_active[0].amout_left - (
                            bid.bidding_amount - winner_bid.bidding_amount + 1)
                        winner_bid.bidding_amount = bid.bidding_amount + 1
                        product.regular_price = bid.bidding_amount + 1
                        users_with_auto_bid_active[0].save()

                        # if the treshold is passed
                        notification_treshold = users_with_auto_bid_active[0].bidding_max_amount * \
                            users_with_auto_bid_active[0].bidding_notification_threshold / 100
                        used_credit = users_with_auto_bid_active[0].bidding_max_amount - \
                            users_with_auto_bid_active[0].amout_left
                        if (used_credit >= notification_treshold):
                            Util.send_email(
                                users_with_auto_bid_active[0].user.email, used_credit)

                        winner_bid.save()
                        product.save()
                    # if he hasn't the needed amount he will broke
                    else:
                        print("the other user has not the right amount")
                        winner_bid.bidding_amount += users_with_auto_bid_active[0].amout_left
                        users_with_auto_bid_active[0].amout_left = 0
                        winner_bid.save()
                        users_with_auto_bid_active[0].save()

                        # if the treshold is passed
                        notification_treshold = users_with_auto_bid_active[0].bidding_max_amount * \
                            users_with_auto_bid_active[0].bidding_notification_threshold / 100
                        used_credit = users_with_auto_bid_active[0].bidding_max_amount - \
                            users_with_auto_bid_active[0].amout_left
                        if (used_credit >= notification_treshold):
                            Util.send_email(
                                users_with_auto_bid_active[0].user.email, used_credit)

            elif (len(users_with_auto_bid_active) > 1):
                print("there are many auto bidding users")
                winner_bid = models.Bid.objects.get(
                    user=users_with_auto_bid_active[0].user, product=product)
                winner_auto_bid = users_with_auto_bid_active[0]
                winner_bid_amount = 0

                for i in range(1, len(users_with_auto_bid_active)):
                    user_bid = models.Bid.objects.get(
                        user=users_with_auto_bid_active[i].user, product=product)

                    if (winner_bid.bidding_amount + winner_auto_bid.amout_left < user_bid.bidding_amount + users_with_auto_bid_active[i].amout_left):
                        # get the second biggest auto bid to outbid it
                        winner_bid_amount = max(
                            winner_bid.bidding_amount + winner_auto_bid.amout_left + 1, winner_bid_amount)
                        winner_bid.bidding_amount += winner_auto_bid.amout_left
                        winner_auto_bid.amout_left = 0
                        winner_bid.save()
                        winner_auto_bid.save()

                        # if the treshold is passed
                        notification_treshold = winner_auto_bid.bidding_max_amount * \
                            winner_auto_bid.bidding_notification_threshold / 100
                        used_credit = winner_auto_bid.bidding_max_amount - \
                            winner_auto_bid.amout_left
                        if (used_credit >= notification_treshold):
                            Util.send_email(
                                winner_auto_bid.user.email, used_credit)

                        winner_bid = user_bid
                        winner_auto_bid = users_with_auto_bid_active[i]
                    else:
                        # get the second biggest auto bid to outbid it
                        winner_bid_amount = max(user_bid.bidding_amount +
                                                users_with_auto_bid_active[i].amout_left + 1, winner_bid_amount)
                        user_bid.bidding_amount += users_with_auto_bid_active[i].amout_left
                        users_with_auto_bid_active[i].amout_left = 0
                        user_bid.save()
                        users_with_auto_bid_active[i].save()

                        # if the treshold is passed
                        notification_treshold = users_with_auto_bid_active[i].bidding_max_amount * \
                            users_with_auto_bid_active[i].bidding_notification_threshold / 100
                        used_credit = users_with_auto_bid_active[i].bidding_max_amount - \
                            users_with_auto_bid_active[i].amout_left
                        if (used_credit >= notification_treshold):
                            Util.send_email(
                                users_with_auto_bid_active[i].user.email, used_credit)

                # get the user with the (biggest auto bidding amount left + amount of bid made by him)
                # then compare it to the bid made that triggered the auto bidding
                if (bid.bidding_amount > winner_bid.bidding_amount + winner_auto_bid.amout_left):
                    winner_bid.bidding_amount += winner_auto_bid.amout_left
                    winner_auto_bid.amout_left = 0
                    winner_bid.save()
                    winner_auto_bid.save()

                    # if the treshold is passed
                    notification_treshold = winner_auto_bid.bidding_max_amount * \
                        winner_auto_bid.bidding_notification_threshold / 100
                    used_credit = winner_auto_bid.bidding_max_amount - \
                        winner_auto_bid.amout_left
                    if (used_credit >= notification_treshold):
                        Util.send_email(
                            winner_auto_bid.user.email, used_credit)

                else:
                    winner_auto_bid.amout_left -= max(
                        winner_bid_amount, bid.bidding_amount + 1) - winner_bid.bidding_amount
                    winner_bid.bidding_amount = max(
                        winner_bid_amount, bid.bidding_amount + 1)
                    product.regular_price = max(
                        winner_bid_amount, bid.bidding_amount + 1)
                    winner_bid.save()
                    winner_auto_bid.save()
                    product.save()

                    # if the treshold is passed
                    notification_treshold = winner_auto_bid.bidding_max_amount * \
                        winner_auto_bid.bidding_notification_threshold / 100
                    used_credit = winner_auto_bid.bidding_max_amount - \
                        winner_auto_bid.amout_left
                    if (used_credit >= notification_treshold):
                        Util.send_email(
                            winner_auto_bid.user.email, used_credit)

    def post(self, request):
        product_id = request.data["product_id"]
        bidding_amount = request.data["bidding_amount"]

        product_object = get_object_or_404(Product, id=product_id)

        try:
            bid = models.Bid.objects.filter(
                user=request.user, product=product_object)

            if(bid.exists()):
                bid_instance = models.Bid.objects.get(
                    user=request.user, product=product_object)
                if(bidding_amount > product_object.regular_price and bid_instance.bidding_amount != product_object.regular_price):

                    bid_instance.bidding_amount = bidding_amount
                    product_object.regular_price = bidding_amount
                    product_object.save()
                    bid_instance.save()
                    self.verify_auto_bid(request, product_object, bid_instance)
                    return Response(
                        {"success": "bid updated successfully"},
                        status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {'error': 'The bidding amount must be greater than the last bid or your bid is the higher'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                if(bidding_amount > product_object.regular_price):

                    bid_instance = models.Bid.objects.create(
                        product=product_object, user=request.user, bidding_amount=bidding_amount)

                    product_object.regular_price = bidding_amount
                    product_object.save()
                    self.verify_auto_bid(request, product_object, bid_instance)
                    return Response(
                        {"success": "bid created successfully"},
                        status=status.HTTP_201_CREATED
                    )
                else:
                    return Response(
                        {'error': 'The bidding amount must be greater than the last bid'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

        except Exception as e:
            return Response(
                {'error': 'Something went wrong when trying to add a bid'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
