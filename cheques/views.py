from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView

import re
from datetime import datetime
import time
import requests

from .models import Shop, Cheque, Product, Entry
from users.models import Profile
from .serializers import ChequeSerializer, EntrySerializer


def parse_qr_string(qr_string):
    time = re.findall(r't=(\w+)', qr_string)[0]
    summ = ''.join(re.findall(r's=(\d+).(\d{2})', qr_string)[0])
    fn = re.findall(r'fn=(\w+)', qr_string)[0]
    number = re.findall(r'i=(\w+)', qr_string)[0]
    fp = re.findall(r'fp=(\w+)', qr_string)[0]
    result = {'time': time, 'summ': summ, 'fn': fn, 'number': number, 'fp': fp}
    return result


# def fns_login(phone, password):
#     requests.get('https://proverkacheka.nalog.ru:9999/v1/mobile/users/login', \
#                  auth=(phone, password))


def check_cheque(qr_string_data, phone, password):
    headers = {'Device-Id':'', 'Device-OS':''}
    payload = {'fiscalSign': qr_string_data.get('fp'), 'date': qr_string_data.get('time'),'sum':qr_string_data.get('summ')}
    check_request = requests.get(f'https://proverkacheka.nalog.ru:9999/v1/ofds/*/inns/*/fss/{qr_string_data.get("fn")}/operations/1/tickets/{qr_string_data.get("number")}', \
                               params=payload, headers=headers,auth=(phone, password))
    print(f'Код ответа сервера ФНС на запрос проверки чека: {check_request.status_code}')
    return check_request.status_code


def request_cheque_entries(qr_string_data, phone, password):
    headers = {'Device-Id':'', 'Device-OS':''}
    request_info=requests.get(f'https://proverkacheka.nalog.ru:9999/v1/inns/*/kkts/*/fss/{qr_string_data.get("fn")}/tickets/{qr_string_data.get("number")}?fiscalSign={qr_string_data.get("fp")}&sendToEmail=no', \
                              headers=headers,auth=(phone, password))
    print(f'Код ответа сервера ФНС на запрос данных в чеке: {request_info.status_code}')
    data = request_info.json()
    return data
    

def fns_signup(email, name, phone):
    check_request = requests.post('https://proverkacheka.nalog.ru:9999/v1/mobile/users/signup', \
                      json = {"email": email,"name": name,"phone": phone})
    return check_request.status_code

     
class ScanChequeView(View):
    def get(self, request):
        return render(request, 'scan_cheque.html')
    
    def post(self, request):
        qr_string = request.POST.get('qrcode')
        qr_string_data = parse_qr_string(qr_string)
        cheque, create = Cheque.objects.get_or_create(
            number=qr_string_data.get('number'),
            defaults={
                'shop': Shop.objects.get(pk=1),
                'summ': f"{qr_string_data.get('summ')[:-2]}.{qr_string_data.get('summ')[-2:]}",
                'time': datetime.strptime(qr_string_data.get('time'), "%Y%m%dT%H%M%S")
            }
        )
        
        user = get_user_model().objects.get(email=settings.MY_EMAIL)
        password = settings.PASSWORD_FNS
        
        try:
            check_cheque_result = check_cheque(qr_string_data, user.profile.phone, password)
            time.sleep(2)
            if check_cheque_result == 204:
                data = request_cheque_entries(qr_string_data, user.profile.phone, password)
                for row in data['document']['receipt']['items']:
                    product, create = Product.objects.get_or_create(
                        name=row['name']
                    )
                    entry = Entry.objects.create(
                        cheque=cheque,
                        product=product,
                        price=row['price']/100,
                        quantity=row['quantity']
                    )
        except:
            fns_signup(email=user.email, name=user.profile.name, phone=user.profile.phone)
        
        return JsonResponse({
            'cheque_number': cheque.number
        })
    
    
class ListChequeView(ListView):
    model = Cheque
    context_object_name = 'cheques'
    template_name = 'cheque_list.html'
    

class DetailChequeView(DetailView):
    model = Cheque
    # context_object_name = 'cheque'
    template_name = 'cheque_detail.html'
    slug_field = 'number'
    slug_url_kwarg = 'number'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if request.is_ajax():
            time.sleep(1)
            cheque_serializer = ChequeSerializer(self.object)
            entries = self.object.entries.all()
            entries_serializer = EntrySerializer(entries, many=True)
            return JsonResponse({
                'cheque': cheque_serializer.data,
                'entries': entries_serializer.data
                }) 
        return self.render_to_response(context)