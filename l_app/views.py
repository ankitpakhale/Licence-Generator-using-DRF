from django.shortcuts import render
from .models import Li_Model, Seller_detail
import string
import random
import csv
from django.http import HttpResponse
from .encryption_util import *
from .serializer import LicencePostSerializer, LicenceGetSerializer, SellerSerializer
from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from rest_framework import generics
from rest_framework.views import APIView

class create_seller(APIView):
    serializer_class = SellerSerializer
    def get(self, request):
        obj = Seller_detail.objects.all()
        s = SellerSerializer(obj, many = True)
        print(s.data)
        return Response(s.data) 

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print(request.data, "This is data")
        if serializer.is_valid():
            try:
                data = Seller_detail.objects.get(email = request.data['email'])
                print('This seller already exists')
            except:
                serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class generate_licence(APIView):
    serializer_class = LicencePostSerializer
    def get(self, request):
        obj = Li_Model.objects.all()
        s_data = LicenceGetSerializer(obj, many = True)
        print(s_data.data)
        return Response(s_data.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(request.data['seller_email'])
            for i in range(int(request.data['S_no'])):
                res = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = 12)))
                print(res)
                try:
                    data = Li_Model.objects.get(licence_no = res)
                    print(f"{data} already exists")
                except:
                    s_email = Seller_detail.objects.get(id = request.data['seller_email'])        
                    Li_Model.objects.create(seller_email= s_email, licence_no= res)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def exportcsv(request):
    students = Li_Model.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=final.csv'
    writer = csv.writer(response)
    writer.writerow(['licence_no'])
    studs = students.values_list('licence_no')
    for std in studs:
        writer.writerow(std)
    return response
