# @api_view(['POST'])
# def add_service_to_cart(request):
#     service_id = request.data['service_id']
#     category = request.data['category']
#     try:
#         service = Service.objects.get(id=service_id)
#     except Service.DoesNotExist:
#         data = {'status': 'error'}
#     else:
#         try:
#             cart = Cart(request=request)
#             cart.add(service, category) 
#         except CategoryChange as e:
#             data = {'status': 'category_change', "mssg": str(e)}
#         else:
#             data = request.session[settings.CART_SESSION_ID]
#     return Response(data)


# @api_view(['POST'])
# def remove_service_from_cart(request):
#     service_id = request.data['service_id']
#     try:
#         service = Service.objects.get(id=service_id)
#     except Service.DoesNotExist:
#         data = {'status': 'error'}
#     else:
#         cart = Cart(request=request)
#         cart.remove(service)
#         data = request.session[settings.CART_SESSION_ID]
#     return Response(data)

# @api_view(['POST'])
# def delete_service(request):
#     service_id = request.data.get('service_id')
#     try:
#         service = Service.objects.get(id=service_id)
#     except Service.DoesNotExist:
#         data = {'status': 'error'}
#     else:
#         cart = Cart(request=request)
#         cart.delete_service(service)
#         data = cart.get_basic_cart()
#     return Response(data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_razorPay_order(request):
#     user = request.user
#     if user.address_1 and user.address_2 and user.city and user.state and user.pincode:
#         cart = Cart(request)
#         # client = razorpay.Client(auth=('rzp_test_Fz30Ps4aOA4Zke', 'HS7mZz3v6G9dLeaS5LY1tejl'))
#         order_amount = cart.get_discounted_total()[0]
#         order_currency = "INR"
#         allowed_characters = datetime.now().strftime('%Y%m%d%H%M%S') + ascii_uppercase + ascii_lowercase
#         order_receipt = 'ORD' + str(user.id) + get_random_string(17, allowed_characters)
#         shipping_address = f"{user.address_1} {user.address_2} {user.city} {user.state} {user.pincode}"
#         notes = {'shipping address': shipping_address}
#         order = client.order.create({'amount': float(order_amount) * 100, 'currency': order_currency, 'receipt': order_receipt, 'notes': notes})
#         if order['status'] == 'created':
#             cart.razorpay_order_created(order['id'], order_receipt)
#         data = {'status': 'ok', "receipt": order_receipt, 'order_details': order, 'user': {'name': f"{user.first_name} {user.last_name}", 'email': user.email, 'number': user.number}, 'notes': notes['shipping address']}
#     else:
#         data = {'status': 'error', 'msg': 'address_error'}
#     return Response(data)