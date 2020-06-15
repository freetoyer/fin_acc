from django.shortcuts import render


def scan_cheque(request):
    return render(request, 'scan_cheque.html')

