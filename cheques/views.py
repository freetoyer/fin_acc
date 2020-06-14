from django.shortcuts import render


def scan_cheque(request):
    return render(request, 'cheques/scan_cheque.html')

