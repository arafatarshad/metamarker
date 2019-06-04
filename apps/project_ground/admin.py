from django.contrib import admin
from .models import DatasetType,Project,ExtraDataset,PreprocessingTasks
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display=('id','author_first_name','author_last_name','description','email','reference_id','dataset')

class DatasetTypeAdmin(admin.ModelAdmin):
    list_display=('id','name')


class DatasetAdmin(admin.ModelAdmin):
    list_display=('id','name')

class PreprocessingTasksAdmin(admin.ModelAdmin):
    list_display=('id','name')


admin.site.register(DatasetType,DatasetTypeAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(ExtraDataset,DatasetAdmin)
admin.site.register(PreprocessingTasks,PreprocessingTasksAdmin)
