from django.contrib import admin
from .models import Contribution, Loan, RepaymentRecord,Userinfo
from django import forms
# Import the ExportCsvMixin
from .utils import ExportCsvMixin


class RepaymentRecordForm(forms.ModelForm):

    class Meta:
        model = RepaymentRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude loans that have been cleared from the dropdown list
        self.fields['loan'].queryset = Loan.objects.exclude(loan_status="Cleared")


@admin.register(Userinfo)
class UserinfoAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['user','phone','id_number']
    

@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['user', 'amount', 'date_contributed']
    list_filter = ['user',]
    actions = ["export_as_csv"]

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin,ExportCsvMixin):
    list_display = ['user', 'amount', 'remaining_amount', 'date_taken', 'interest_rate','loan_status']
    readonly_fields =['remaining_amount','interest_rate','loan_status']
    actions = ["export_as_csv"]

@admin.register(RepaymentRecord)
class RepaymentRecordAdmin(admin.ModelAdmin,ExportCsvMixin):
    
    list_display = ['loan_id','loan', 'amount_paid', 'date_paid','loan_balance',]
    readonly_fields = ['loan_balance',]
    list_filter = ['loan_id']
    search_fields = ['loan__user__username']
    actions = ["export_as_csv"]

    ##group_by
    # list_display_links = ('loan_id', 'loan')  # Fields that link to the change form

    def loan_id(self, obj):
        """
        Return the loan ID for grouping.
        """
        return obj.loan.id

    # loan_id.admin_order_field = 'loan__id'  # Allows ordering by loan ID
    # loan_id.short_description = 'Loan ID'
    ##end of group by
    form = RepaymentRecordForm
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Override the formfield to exclude loans that have been cleared from the dropdown list.
        """
        if db_field.name == "loan":
            kwargs["queryset"] = Loan.objects.exclude(loan_status="Cleared")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
