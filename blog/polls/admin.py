from django.contrib import admin
from .models import Question,Choice


# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text','pub_date')
    search_fields = ('question_text',)
admin.site.register(Question,QuestionAdmin)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question','choice_text','votes')
    search_fields = ('question',)
admin.site.register(Choice,ChoiceAdmin)
