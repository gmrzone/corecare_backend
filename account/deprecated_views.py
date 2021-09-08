# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_current_user(request):
#     user = request.user
#     serializer = UserSerializer(user)
#     return Response(serializer.data)


# @api_view(['POST'])
# def signup(request):
#     number = request.data.get('number')
#     try:
#         user = CustomUser.objects.get(number=number)
#         if not user.verified:
#             user.delete()
#             raise CustomUser.DoesNotExist()
#     except CustomUser.DoesNotExist:
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             data = serializer.save(password=make_password(f"{number}corecare"))
#         # if validate_number(number):
#         #     print("Ok")
#         #     CustomUser.objects.create_user(number=number, password=f"{number}corecare")
#         #     print("Not OK")
#         #     secret_key = generate_key_for_otp(number)
#         #     key = base64.b32encode(secret_key.encode())
#         #     otp = pyotp.TOTP(key, interval=300, digits=6)
#         #     print(otp.now())
#         #     data = {'status': 'ok', 'msg': "A 6 Digit OTP Has Been Send to Your Mobile Number {0}".format(number), 'otp': otp.now()}
#         else:
#             data = {'status': 'error', 'msg': "Invalid Number"}
#     else:
#         data = {'status': 'warning', 'msg': 'An Account with number {0} already Exist with us. Please Login or Reset Your Password.'.format(number)}
#     return Response(data)

# @api_view(['POST'])
# def verify_otp(request):
#     number = request.data.get('number')
#     entered_otp = request.data.get('entered_otp')
#     password = request.data.get('password1')
#     if entered_otp and len(entered_otp) == 6:
#         secret_key = generate_key_for_otp(number)
#         key = base64.b32encode(secret_key.encode())
#         otp = pyotp.TOTP(key, interval=300, digits=6)
#         if otp.verify(entered_otp):
#             user = get_object_or_404(CustomUser, number=number)
#             user.set_password(password)
#             user.verified = True
#             user.save()
#             data = {'status': 'ok', 'msg': 'Your Number Has been Verified Sucessfully'}
#         else:
#             data = {'status': 'error', 'msg': 'Invalid OTP or OTP Expired'}

#     else:
#         data = {'status': 'error', 'msg': 'Please Enter a valid 6 digit OTP'}
#     return Response(data)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def update_profile_image(request):
#     image = request.data.get('image')
#     number = request.data.get('number')
#     password = request.data.get('password')
#     user = get_object_or_404(CustomUser, number=number)
#     if user.check_password(password):
#         if image:
#             user.photo = image
#         user.save()
#         data = {'status': 'ok', 'message': 'Profile Photo Updated'}
#     else:
#         data = {'status': 'error', 'message': "Invalid Number"}
#     return Response(data)


# def update_user(user, first_name, last_name, email, address_1, address_2, city, state, pincode, new_account):
#     user.first_name = first_name
#     user.last_name = last_name
#     user.email = email
#     user.address_1 = address_1
#     user.address_2 = address_2
#     user.city = city
#     user.state = state
#     user.pincode = pincode
#     user.save()
#     if new_account:
#         new_signup.delay(user.id)

# @api_view(['POST'])
# def signup_additional(request):
#     user = request.user
#     first_name = request.data.get('first_name')
#     last_name = request.data.get('last_name')
#     email = request.data.get('email')
#     address_1 = request.data.get('address_1')
#     address_2 = request.data.get('address_2')
#     city = request.data.get('city')
#     state = request.data.get('state')
#     pincode = request.data.get('pincode')
#     number = request.data.get('number')
#     password = request.data.get('password')
#     email_exist = CustomUser.objects.filter(email=email).exists()
#     if isinstance(user, AnonymousUser):
#         if first_name and last_name and email and address_1 and address_2 and city and state and pincode and number:
#             if email_exist:
#                 data = {'status': 'error', 'msg': 'We Already have an account associated with email {0}'.format(email)}
#             else:
#                 user = get_object_or_404(CustomUser, number=number)
#                 if user.check_password(password):
#                     print("Correect Password")
#                     update_user(user, first_name, last_name, email, address_1, address_2, city, state, pincode, new_account=True)
#                     data = {'status': 'ok', 'msg': 'Profile Sucessfully Updated'}
#                 else:
#                     data = {'status': 'error', 'msg': 'Invalid Number'}
#         else:
#             data = {'status': 'error', 'msg': 'Please Provide all the required fields'}
#     else:
#         if email_exist:
#             data = {'status': 'error', 'msg': 'We Already have an account associated with email {0}'.format(email)}
#         else:
#             update_user(user, first_name, last_name, email, address_1, address_2, city, state, pincode, new_account=False)
#             data = {'status': 'ok', 'msg': 'Profile Sucessfully Updated'}
#     return Response(data)
