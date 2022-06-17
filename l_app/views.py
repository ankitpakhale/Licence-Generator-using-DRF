from django.shortcuts import render, redirect
from .models import Li_Model, Seller_detail
import string
import random
import csv
from django.http import HttpResponse
from .encryption_util import encrypt, decrypt

def create_seller(request):
    if request.POST:
        email = request.POST.get('email')
        name = request.POST.get('name')
        age = request.POST.get('age')
        print(email, name, age)
        Seller_detail.objects.create(email = encrypt(email), name = encrypt(name), age = age)
    return redirect('generate_licence')

def generate_licence(request):
    res = ''
    if request.POST:
        email = request.POST['seller_email']
        entry = int(request.POST.get('license_nos', False))
        s_email = Seller_detail.objects.get(email = email)
        for i in range(entry):
            N = 12
            res = str(''.join(random.choices(string.ascii_uppercase + string.digits, k = N)))
            try:
                data = Li_Model.objects.get(licence_no = res)
            except:
                Li_Model.objects.create(seller_email= s_email, licence_no= res)
    return render(request, 'entry.html')

def exportcsv(request):
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