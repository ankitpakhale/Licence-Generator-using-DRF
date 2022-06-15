from django.shortcuts import render
from .models import Li_Model, Seller_detail
import string
import random
import csv
from django.http import HttpResponse
from .encryption_util import *
from .serializer import LicencePostSerializer, LicenceGetSerializer, SellerSerializer, ExportSerializer
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



class All_create_seller(APIView):
    # serializer_class=SellerSerializer
    def get(self,request,id=None,format=None):
        if id is not None:
            try:
                s=Seller_detail.objects.get(id=id)
                s=SellerSerializer(s)
            except:
                msg={"msg":"id does not exists"}
                return Response(msg)    
        else:
            s=Seller_detail.objects.all()
            s=SellerSerializer(s,many=True)
        
        return Response(s.data)


    def post(self,request,format=None):        
        s=SellerSerializer(data=request.data)
        print(s)
        if s.is_valid():
            s.save()
            msg={'msg':'data saved into db'}
            return Response(msg)
        return Response(s.error_messages)    


    def put(self,request,id=None,format=None):
        if id is not None:
            print(id)
            obj=Seller_detail.objects.get(id=id)
            s=SellerSerializer(obj,data=request.data)
            if s.is_valid():
                s.save()
                msg={'msg':'data updated'}
                return Response(msg)
        else:
            id=request.data['id']
            obj=Seller_detail.objects.get(id=id)
            s=SellerSerializer(obj,data=request.data)
            if s.is_valid():
                s.save()
                msg={'msg':'data updated'}
                return Response(msg)
        return Response(s.error_messages)    

    def patch(self,request,id=None,format=None):
        if id is not None:
            print(id)
            obj=Seller_detail.objects.get(id=id)
            s=SellerSerializer(obj,data=request.data)
            if s.is_valid():
                s.save()
                msg={'msg':'data updated'}
                return Response(msg)
        else:        
            id=request.data['id']
            obj=Seller_detail.objects.get(id=id)
            s=SellerSerializer(obj,data=request.data,partial=True)
            if s.is_valid():
                s.save()
                msg={'msg':'data updated'}
                return Response(msg)
            return Response(s.error_messages)    
    
    def delete(self,request,id):
        obj=Seller_detail.objects.get(id=id)
        print(obj)
        obj.delete()
        msg={'msg':'data delete'}
        return Response(msg)
        

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

class exportcsv(APIView):
    serializer_class = ExportSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():            
            s_data = Seller_detail.objects.get(id= request.data['seller_email'])
            l_seller = Li_Model.objects.filter(seller_email= s_data)                        
            response = HttpResponse()
            response['Content-Disposition'] = f'attachment; filename={s_data}.csv'
            writer = csv.writer(response)
            writer.writerow(['User Email', 'Licence No', 'Used'])            
            l_studs = l_seller.values_list('licence_no', 'is_used')
            for std in l_studs:
                l=[]
                l.append(s_data.email)
                l.append(std[0])
                l.append(std[1])
                writer.writerow(l)
            return response
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

