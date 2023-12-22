import csv
from django.http import HttpResponse

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        writer = csv.writer(response)
        fields = [field.name for field in self.model._meta.fields]
        writer.writerow(fields)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])
        return response

    export_as_csv.short_description = "Export Selected as CSV"
