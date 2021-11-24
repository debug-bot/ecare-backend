from django.shortcuts import render

from rest_framework import mixins, serializers

from rest_framework import permissions, status, authentication

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.core.mail import send_mail

from .models import Cart, Order, Patient, Pharmacy, Lab, Rider, Test, User

from .serializers import ShowLabsSerializer, ShowPharmaciesSerializer, ShowTestsSerializer, SubmitPatientDataSerializer

class ShowTestsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Test.objects.all()
    serializer_class = ShowTestsSerializer
    #permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']
     
    
class ShowLabsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Lab.objects.all()
    serializer_class = ShowLabsSerializer
    #permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']
    def list(self, request, *args, **kwargs):
        id = request.query_params.get('test_id','1')
        query_set = Test.objects.get(id=id).labs

        #queryset = self.filter_queryset(query_set)

        #page = self.paginate_queryset(queryset)
        #if page is not None:
        #    serializer = self.get_serializer(page, many=True)
        #    return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)   
    
class ShowPharmaciesViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = ShowPharmaciesSerializer
    #permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get']
    
class SubmitPatientData(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = SubmitPatientDataSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post']
    
class GetPatientData(mixins.ListModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Patient.objects.all()
    serializer_class = SubmitPatientDataSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get','delete']
    def list(self, request, *args, **kwargs):
        # email = request.user.email
        # User.objects.get(email="adnan.newton@gmail.com")
        query_set = Patient.objects.filter(user=request.user)

        #queryset = self.filter_queryset(query_set)

        #page = self.paginate_queryset(queryset)
        #if page is not None:
        #    serializer = self.get_serializer(page, many=True)
        #    return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(query_set, many=True)
        return Response(serializer.data)   
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


from django.shortcuts import get_object_or_404
import ast
class CartItemViewSet(APIView):
    def post(self, request):
        data = request.data.get('data',None)
        print(data)
        data = ast.literal_eval(data)
        print(data)
        items = []
        for i in data:
            o = i.split(',')
            test_id = o[0]
            lab_id = o[1]
            item = self.fn(test_id, lab_id)
            items.append(item)
        return Response(items)
    def fn(self,test_id, lab_id):
        price = self.price_method(test_id, lab_id)
        test_name = self.test_name_method(test_id, lab_id)
        lab_name = self.lab_name_method(test_id, lab_id)
        discount = self.discount_method(test_id, lab_id)
        discounted_price = self.discounted_method(test_id, lab_id)
        return {'price':price,'test_name':test_name,'lab_name':lab_name,'discount':discount,'discounted_price':discounted_price,'test_id':test_id,'lab_id':lab_id}
    def price_method(self,test_id, lab_id):
           
        try:
            lab = Test.objects.get(id=test_id).labs.get(id=lab_id)
            return lab.price
        except:
            print('error')
            return 0
        
    def test_name_method(self,test_id,lab_id):
        try:
            return Test.objects.get(id=test_id).name
        except:
            return None
    def lab_name_method(self,test_id, lab_id):
        try:
            return Test.objects.get(id=test_id).labs.get(id=lab_id).name
        except:
            return None
    def discount_method(self,test_id, lab_id):
     
        try:
            lab = Test.objects.get(id=test_id).labs.get(id=lab_id)
            return lab.discount_percent
        except:
            print('error')
            return 0
        
    def discounted_method(self,test_id, lab_id):
        try:
            lab = Test.objects.get(id=test_id).labs.get(id=lab_id)
            percent = lab.discount_percent
            price = lab.price
            return (price) - ((price*percent) / 100)
        except:
            print('error')
            return 0
        
class OrderPlaceViewSet(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request):
        try:
            data = request.data.get('data',None)
            price = request.data.get('price',None)
            discount = request.data.get('discount',None)
            discounted_price = request.data.get('discounted_price',None)
            items = request.data.get('items',None)
            address = request.data.get('address',None)
            print(request.data)
            patient=Patient.objects.get(id=address)
            Order.objects.create(patient=patient,items=data)
            message = f'Your order successfully placed\n\n       Total Items Ordered = {items}\n\n   Actual Price = Rs. {price}\n   Discount = Rs. {discount}\n   Discounted Price = Rs. {discounted_price}\n\n\n  Shipment Address = {patient.address}\n  City = {patient.city}\n  Phone Number = {patient.phone}\n  Name = {patient.name}\n\n\n-Thank You for trusting eCare!'
            send_mail('ORDER Placed',message,settings.EMAIL_HOST_USER,['chhamza2655@gmail.com','adnan.newton@gmail.com',request.user.email])
            return Response('ok')
        except Exception as e:
            print(e)
            send_mail('ERROR placing order','Something went wrong, your order could not be placed',settings.EMAIL_HOST_USER,['usmanbinshafiq@gmail.com','adnan.newton@gmail.com',request.user.email])
            return Response('error')