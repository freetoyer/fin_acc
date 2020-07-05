from django.urls import path


from cheques.views import ScanChequeView, ListChequeView, DetailChequeView


urlpatterns = [
    # path('scan_cheque/', views.scan_cheque, name='scan_cheque' ),
    path('scan_cheque/', ScanChequeView.as_view(), name='scan_cheque' ),
    path('cheque_list/', ListChequeView.as_view(), name='cheque_list' ),
    path('cheque_detail/<str:number>/', DetailChequeView.as_view(), name='cheque_detail' ),
]