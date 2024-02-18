from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serlizer import UserRegisterSerlizer,UserLoginSerlizer,UserProfileSerlizer,ChangePasswordSerlizer,RestPasswordEmailSerlizer,UserPasswordRestSerlizer
from django.contrib.auth import authenticate,login
from rest_framework.permissions import IsAuthenticated

#create token manually
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



# Create your views here.

class Register(APIView):
    def post(self,request):
        serlizer=UserRegisterSerlizer(data=request.data)
        if serlizer.is_valid(raise_exception=True):
            user=serlizer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'mesg': 'You Have been Register successfully'},status=status.HTTP_201_CREATED)
        return Response(serlizer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserLogin(APIView):
    def post(self,request):
        serilzer=UserLoginSerlizer(data=request.data)
        if serilzer.is_valid(raise_exception=True):
            email=serilzer.data.get('email')
            password=serilzer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                # login(request,user)
                return Response({'token':token,'mesg': 'Login successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({'errors':{'non fields error':['Email or Password is not Valid']}},status=status.HTTP_404_NOT_FOUND)
        return Response({'mesg': 'not found'},status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serlizer=UserProfileSerlizer(request.user)
        return Response(serlizer.data,status=status.HTTP_200_OK)
        
class UserCangePassword(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        serlizer=ChangePasswordSerlizer(data=request.data,context={'user':request.user})
        if serlizer.is_valid(raise_exception=True):
            return Response({'mesg':' Password has been Change successfully'},status=status.HTTP_200_OK)
        return Response(serlizer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordRestEmail(APIView):
    def post(self,request):
       serlizer=RestPasswordEmailSerlizer(data=request.data)
       if serlizer.is_valid(raise_exception=True):
           return Response({'mesg':' Password  Reset successfully,  Please check your Email'},status=status.HTTP_200_OK)
       return Response(serlizer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserPasswordRestView(APIView):
    def post(self,request,uuid,token):
        serlizer= UserPasswordRestSerlizer(data=request.data, context={'uuid':uuid,'token':token})    
        if serlizer.is_valid(raise_exception=True):
           return Response({'mesg':' Password  Reset  Succeessfully'},status=status.HTTP_200_OK)
        return Response(serlizer.errors,status=status.HTTP_400_BAD_REQUEST)
    