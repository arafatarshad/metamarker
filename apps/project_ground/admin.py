from django.contrib import admin
from .models import Project,ExtraDataset,PreprocessingTasks
# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display=('id','author_first_name','author_last_name','description','email','reference_id','dataset')



class DatasetAdmin(admin.ModelAdmin):
    list_display=('id','name','basefilename','project_id')

class PreprocessingTasksAdmin(admin.ModelAdmin):
    list_display=('id','name')

admin.site.register(Project,ProjectAdmin)
admin.site.register(ExtraDataset,DatasetAdmin)
admin.site.register(PreprocessingTasks,PreprocessingTasksAdmin)
