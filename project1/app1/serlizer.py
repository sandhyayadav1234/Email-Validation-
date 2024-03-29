from rest_framework import serializers
from .models import User
from xml.dom import ValidationErr
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from .utils import Utils
class UserRegisterSerlizer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
            
        }
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password !=password2:
            raise serializers.ValidationError("Password does't match!!!")
        
        return attrs

    def create(self, validated_data):
        
        return User.objects.create_user(**validated_data)
    
class UserLoginSerlizer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email','password']
    
class UserProfileSerlizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','email','name']
class ChangePasswordSerlizer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
        
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password !=password2:
            raise serializers.ValidationError("Password does't match!!!")
        
        user.set_password(password)
        user.save()
        return attrs
    
class RestPasswordEmailSerlizer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=['email']
        
    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
           user=User.objects.get(email=email)
           uuid=urlsafe_base64_encode(force_bytes(user.id))
           print("encoded",uuid)
           token=PasswordResetTokenGenerator().make_token(user)
           print("pasword Reset Token",token)
           link='http://localhost:3000/api/user/rest/'+uuid+'/'+token
           print("pssword Reset",link)
           #send Email
           body='Click a link to reset Password '+link
           data={
               'subject':'Reset your Password',
               'body':body,
               'to_mail':user.email
           }
           Utils.send_Email(data)
           return attrs
        else:
            raise ValidationErr("You Are not Register User")
      
class UserPasswordRestSerlizer(serializers.Serializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['password','password2']
        
    def validate(self, attrs):
        try:
            password=attrs.get('password')
            password2=attrs.get('password2')
            uuid=self.context.get('uuid')
            token=self.context.get('token')
            if password !=password2:
                raise serializers.ValidationError("Password  And Confrim Password does't match!!!")
            id=smart_str(urlsafe_base64_decode(uuid))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationErr("TOKEN IS NOT VALIDATE OR EXPEIRED")
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationErr("Token is not valid")