

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