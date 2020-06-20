from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

import re
from datetime import datetime

from .models import Shop, Cheque


def parse_qr_string(qr_string):
    time = re.findall(r't=(\w+)', qr_string)[0]
    summ = re.findall(r's=(\w+)', qr_string)[0]
    fn = re.findall(r'fn=(\w+)', qr_string)[0]
    number = re.findall(r'i=(\w+)', qr_string)[0]
    fp = re.findall(r'fp=(\w+)', qr_string)[0]
    result = {'time': time, 'summ': summ, 'fn': fn, 'number': number, 'fp': fp}
    return result
        
        
class ScanChequeView(View):
    def get(self, request):
        return render(request, 'scan_cheque.html')
    
    def post(self, request):
        qr_string = request.POST.get('qrcode')
        qr_string_data = parse_qr_string(qr_string)
        try:
            cheque = Cheque.objects.get(number=qr_string_data.get('number'))
        except:
            time_formated = datetime.strptime(qr_string_data.get('time'), "%Y%m%dT%H%M%S").strftime("%Y-%m-%d %H:%M")
            shop = Shop.objects.get(pk=1)
            cheque = Cheque.objects.create(
                number=qr_string_data.get('number'),
                shop=shop,
                summ=qr_string_data.get('summ'),
                time=time_formated
                )       
        return JsonResponse({
            'cheque_number': cheque.number
        })
    
    
    
