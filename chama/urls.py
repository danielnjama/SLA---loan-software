from django.contrib import admin
from django.urls import path

admin.site.site_header="Savings & Loans Association"
admin.site.site_title="Savings & Loans Association"
admin.site.index_title="SLA ADMIN"

urlpatterns = [
    path('admin/', admin.site.urls),
]
