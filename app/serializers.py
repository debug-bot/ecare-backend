from rest_framework import serializers
from .models import Cart, Patient, Pharmacy, Lab, Rider, Test, User
import uuid
class ShowPharmaciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = ['name', 'location', 'contact']
        
class ShowLabsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lab
        fields = ['id','name', 'price']

class ShowTestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id','name']
        
class SubmitPatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','name', 'phone', 'city', 'address']
    def create(self, validated_data):
        user = self.context['request'].user
        name = user.first_name+' '+user.middle_name+' '+user.last_name
        instance = Patient.objects.create(user=self.context['request'].user,**validated_data)
        return instance


class ShowPatientDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','name', 'phone', 'city', 'address']
    def create(self, validated_data):
        user = self.context['request'].user
        name = user.first_name+' '+user.middle_name+' '+user.last_name
        instance = Patient.objects.create(user=self.context['request'].user,**validated_data)
        return instance
