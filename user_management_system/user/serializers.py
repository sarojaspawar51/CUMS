from rest_framework import serializers
from user.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = [
        #     'id','firstname', 'lastname', 'email', 'mobilenumber', 'gender']
        fields = "__all__"
