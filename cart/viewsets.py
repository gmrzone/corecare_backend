# Rest Framework
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

# Django
from django.shortcuts import get_object_or_404

# Project Import
from .serializers import OrderSerializer
from .models import Order


class OrderViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        # queryset = Order.objects.all().select_related('coupon', 'user', 'category').prefetch_related('items')
        queryset = Order.objects.all().select_related('category', 'user', 'coupon').prefetch_related('items', 'items__service', 'coupon__category')
        ser = OrderSerializer(queryset, many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        # queryset = Order.objects.all().select_related('coupon','user', "category").prefetch_related('items')
        queryset = Order.objects.all().select_related('category', 'user', 'coupon').prefetch_related('items', 'items__service', 'coupon__category')
        order = get_object_or_404(queryset, receipt=pk)
        ser = OrderSerializer(order)
        return Response(ser.data)

    @action(detail=False, methods=['GET'])
    def user_order(self, request):
        # queryset = Order.objects.all().select_related('coupon', 'user', 'category').prefetch_related('items')
        queryset = Order.objects.all().select_related('category', 'user', 'coupon').prefetch_related('items', 'items__service', 'coupon__category')
        orders = queryset.filter(user=request.user)
        ser = OrderSerializer(orders, many=True)
        return Response(ser.data)