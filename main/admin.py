from django.contrib import admin
from .models import Question, Answer

class MainAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)


admin.site.register(Question, MainAdmin)
admin.site.register(Answer, MainAdmin)
