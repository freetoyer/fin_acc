from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

import re
from datetime import datetime
import requests

from .models import Shop, Cheque


def parse_qr_string(qr_string):
    time = re.findall(r't=(\w+)', qr_string)[0]
    summ = re.findall(r's=(\w+)', qr_string)[0]
    fn = re.findall(r'fn=(\w+)', qr_string)[0]
    number = re.findall(r'i=(\w+)', qr_string)[0]
    fp = re.findall(r'fp=(\w+)', qr_string)[0]
    result = {'time': time, 'summ': summ, 'fn': fn, 'number': number, 'fp': fp}
    return result


def fns_signup(email, name, phone):
    r = requests.post('https://proverkacheka.nalog.ru:9999/v1/mobile/users/signup', \
                      json = {"email": email,"name": name,"phone": phone})

        
        
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
                'summ': qr_string_data.get('summ'),
                'time': qr_string_data.get('time')
            }
        )

        return JsonResponse({
            'cheque_number': cheque.number
        })
    
    
    
