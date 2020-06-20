from django.urls import path


from cheques.views import ScanChequeView


urlpatterns = [
    # path('scan_cheque/', views.scan_cheque, name='scan_cheque' ),
    path('scan_cheque/', ScanChequeView.as_view(), name='scan_cheque' ),
]