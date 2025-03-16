from rest_framework import serializers
from .models import UserAccount, Customer, Photographer


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class CustomerSignupSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = Customer
        fields = ['user', 'customer_details']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserAccount.objects.create_user(**user_data)
        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class PhotographerSignupSerializer(serializers.ModelSerializer):
    user = UserAccountSerializer()

    class Meta:
        model = Photographer
        fields = ['user', 'phone_number']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserAccount.objects.create_user(**user_data)
        photographer = Photographer.objects.create(user=user, **validated_data)
        return photographer
