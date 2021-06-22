
# Deprecated Viewss


# @api_view(['GET'])
# def GetCoupons(request):
#     coupon_codes = cache.get('coupon_code')
#     if coupon_codes:
#         return Response(coupon_codes)
#     else:
#         coupons = CouponCode.objects.all().prefetch_related('category')
#         Serializer = CouponCodeSerializers(coupons, many=True)
#         cache.set('coupon_code', Serializer.data)
#         return Response(Serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def createReview(request, slug):
#     category = EmployeeCategory.objects.get(slug=slug)
#     parent_id = request.data.get('parent', False)
#     try:
#         parent = CategoryReview.objects.get(id=parent_id)
#     except CategoryReview.DoesNotExist:
#         review = CategoryReview(star=request.data['star'], review=request.data['review'])
#     else:
#         review = CategoryReview(star=request.data['star'], review=request.data['review'], parent=parent)
#     review.user = request.user
#     review.category = category
#     review.save()
#     if parent_id:
#         a = CategoryReview.objects.filter(category=category).select_related('user', 'parent')
#         ser = CategoryReviewSerializer(a, many=True)
#     else:
#         ser = CategoryReviewSerializer(review)
#     return Response(ser.data)


# @api_view(['GET'])
# def getReviews(request, slug):
#     # employees = EmployeeCategory.objects.get(slug=slug).category_reviews.all().select_related('user', 'parent')
#     reviews = CategoryReview.objects.filter(category__slug=slug).select_related('user').prefetch_related('replies')
#     ser = CategoryReviewSerializer(reviews, many=True)
#     return Response(ser.data)