from django.urls import path


from cheques import views


urlpatterns = [
    path('scan_cheque/', views.scan_cheque, name='scan_cheque' ),
]