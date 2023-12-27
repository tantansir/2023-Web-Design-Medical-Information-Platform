from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from .models import Hospital
from .models import Department
from .models import Illness


class HospitalResource(resources.ModelResource):
    class Meta:
        model = Hospital


class HospitalAdmin(ImportExportModelAdmin):
    resource_classes = [HospitalResource]


@admin.register(Hospital)
class HospitalAdmin(ImportExportModelAdmin):
    pass


class DepartmentResource(resources.ModelResource):
    class Meta:
        model = Department


class DepartmentAdmin(ImportExportModelAdmin):
    resource_classes = [DepartmentResource]


@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    pass


class IllnessResource(resources.ModelResource):
    class Meta:
        model = Illness


class IllnessAdmin(ImportExportModelAdmin):
    resource_classes = [IllnessResource]


@admin.register(Illness)
class IllnessAdmin(ImportExportModelAdmin):
    pass
