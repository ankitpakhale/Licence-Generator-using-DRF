from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Li_Model, Seller_detail


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller_detail
        fields = '__all__'

class LicenceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Li_Model
        fields = '__all__'

    def to_representation(self, instance):
        rep = super(LicenceGetSerializer, self).to_representation(instance)
        rep['seller_email'] = instance.seller_email.email
        return rep

class LicencePostSerializer(serializers.ModelSerializer):
    S_no = serializers.CharField(max_length=1000)
    class Meta:
        model = Li_Model
        fields = ['seller_email', 'S_no']

class ExportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Li_Model
        fields = ['seller_email']