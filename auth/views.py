# from rest_framework import generics, permissions
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from django.contrib.auth.hashers import make_password, check_password
# # from rest_framework.response import Response
# from .models import Photographer
# from .serializers import PhotographerSerializer

# class PhotographerSignUpView(generics.CreateAPIView):
#     queryset = Photographer.objects.all()
#     # serializer_class = PhotographerSerializer

# class PhotographerSignInView(generics.GenericAPIView):
#     serializer_class = PhotographerSerializer

#     # def post(self, request, *args, **kwargs):
#     #     email = request.data.get('email')
#     #     password = request.data.get('password')
#     #     try:
#     #         photographer = Photographer.objects.get(email=email)
#     #         if check_password(password, photographer.password):
#     #             refresh = RefreshToken.for_user(photographer)
#     #             return Response({
#     #                 'refresh': str(refresh),
#     #                 'access': str(refresh.access_token),
#     #             })
#     #         return Response({'error': 'Invalid credentials'}, status=400)
#     #     except Photographer.DoesNotExist:
#     #         return Response({'error': 'User  not found'}, status=404)

# class PhotographerLogoutView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]

#     # def post(self, request):
#     #     # Simply return a success response, as JWT tokens are stateless
#     #     return Response({'message': 'Successfully logged out'}, status=200)