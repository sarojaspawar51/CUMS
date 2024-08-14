from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import User
from .serializers import  UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
# from .pagination import CustomLimitOffsetPagination,CustomPageNumberPagination
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import JsonResponse
import requests
from django.views.decorators.http import require_GET
from .pagination import CustomPageNumberPagination



class UserAPIView(APIView):
    # pagination_class = CustomLimitOffsetPagination
    pagination_class = CustomPageNumberPagination
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def get_permissions(self):
        if self.request.method=='GET':
            return [AllowAny()]
        elif self.request.method=='POST':
            return [AllowAny()]
        return super().get_permissions()
    
    def get(self, request, pk=None):
        if pk is not None:
          
            try:
                user_objs= User.objects.get(id=pk)
                refresh= RefreshToken.for_user(user_objs)
                data={
                     'refresh':str(refresh),
                     'access':str(refresh.access_token)
                }
            except User.DoesNotExist:
                return Response({'status':'fail','message': f'Invaild Id:- {pk}.',}, status=status.HTTP_404_NOT_FOUND)

            serialized_data = UserSerializer(user_objs).data
            return Response({'status':'success','message': 'Data Fetch successfully', 'data':serialized_data,'datas':data}, status=status.HTTP_200_OK)
        else:
            user_objs = User.objects.all()
            print(f'135-------{user_objs}')
            serialized_data = UserSerializer(user_objs, many=True).data
            # paginator = self.pagination_class()
            # paginated_users = paginator.paginate_queryset(user_objs, request)
            # serialized_data = UserSerializer(paginated_users, many=True).data
            # return paginator.get_paginated_response(serialized_data)

            user_objs = User.objects.all().order_by('id')  
            paginator = self.pagination_class()
            paginated_users = paginator.paginate_queryset(user_objs, request)
            serialized_data = UserSerializer(paginated_users, many=True).data
            return paginator.get_paginated_response(serialized_data)
            return Response({'status':'success','message': 'Data Fetch successfully', 'data':serialized_data}, status=status.HTTP_200_OK)
   
   
    def post(self, request):
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user=serializer.save() 
                user.set_password(serializer.data['password'])
                user.save()
                return Response({'status': 'success', 'message': 'User created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    
            

class UserInfoAPIView(APIView):
      permission_classes = [IsAuthenticated]
      authentication_classes=[JWTAuthentication]

    #   pagination_class = CustomLimitOffsetPagination
      
      def get(self, request, pk=None):
        if pk is None:
            return Response({'status': 'fail', 'message': 'Must provide ID for retrieval'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(User, id=pk)
        user_objs= User.objects.get(id=pk)
        refresh= RefreshToken.for_user(user_objs)
        data={
                'refresh':str(refresh),
                'access':str(refresh.access_token)
        }
        serialized_data = UserSerializer(user).data
        return Response({'status': 'success', 'message': f'User with ID {pk} fetched successfully', 'data': serialized_data,'token':data}, status=status.HTTP_200_OK)

      def put(self, request, pk=None):
        if pk is None:
            return Response({'status': 'fail', 'message': 'Must provide ID for updating'}, status=status.HTTP_400_BAD_REQUEST)
        print(f"Updating user with ID: {pk}") 
        user_objs = get_object_or_404(User, id=pk)
        serializer = UserSerializer(user_objs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': f'User with ID {pk} updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

      def patch(self, request, pk=None):
           if pk is None:
                 return Response({'status': 'fail', 'message': 'Must provide ID for partial update'}, status=status.HTTP_400_BAD_REQUEST)
           user_objs = get_object_or_404(User, id=pk)
        #    name=request.data.get('name')
           serializer = UserSerializer(instance=user_objs,data=request.data, partial=True)
           if serializer.is_valid():
                 serializer.save()
                 return Response({'status': 'success', 'message': f'User with ID {pk} partially updated successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

      def delete(self, request, pk=None):
            if pk is None:
                  return Response({'status': 'fail', 'message': 'Must provide ID for deletion'}, status=status.HTTP_400_BAD_REQUEST)
            user_objs = get_object_or_404(User, id=pk)
            user_objs.delete()
            return Response({'status': 'success', 'message': f'User with ID {pk} deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
      
 #crud operations using JWT Authentication without ID
 
class UserProfileInfoAPIView(APIView):
     permission_classes = [IsAuthenticated]
     authentication_classes = [JWTAuthentication]

     def get(self, request):
        user = request.user
        serialized_data = UserSerializer(user).data
        return Response({'status': 'success', 'message': 'fetched successfully', 'data': serialized_data}, status=status.HTTP_200_OK)
     

     def post(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'User created successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


     def put(self, request):
         user = request.user
         serializer = UserSerializer(user, data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     def patch(self, request):
        user = request.user  
        serializer = UserSerializer(user, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'data': serializer.data}, status=status.HTTP_200_OK)



#Third party API Integration

# base_url = 'https://api.weatherbit.io/v2.0/current'  

# @require_GET
# def fetch_data(request):
#     api_key = request.GET.get('api_key', None)  
#     print(f'182---------{api_key}')
#     if not api_key:
#         return JsonResponse({'error': 'API key is required'}, status=400)

#     params = {
#         'key': api_key,  
#         'city': 'London',  
#     }

#     try:
#         response = requests.get(base_url, params=params)
#         response.raise_for_status()  

#         try:
#             data = response.json()
#             return JsonResponse(data)
#         except ValueError:
#             return JsonResponse({'error': 'Failed to decode JSON response'}, status=500)

#     except requests.exceptions.HTTPError as http_err:
#         return JsonResponse({'error': f'HTTP error occurred: {http_err}'}, status=500)
#     except Exception as err:
#         return JsonResponse({'error': f'Other error occurred: {err}'}, status=500)
    

    
class PublicAPIView(APIView):
    def get(self, request):
        base_url = 'https://api.weatherbit.io/v2.0/current'  

        api_key = request.GET.get('api_key',None)
        city = request.GET.get('city',None) 
 
        print(f'178-----{api_key}')

        params = {
        'key': api_key,  
        'city': city,  
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        # return JsonResponse(data)
        if response.status_code == 200:
            return Response({'status': 'success', 'message': 'fetched successfully', 'datas':data}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'fail', 'message': 'failed to fetch data',}, status=response.status_code)



    
     
