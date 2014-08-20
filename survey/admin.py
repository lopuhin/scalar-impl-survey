from django.contrib import admin
import survey.models


admin.site.register(survey.models.Image)


admin.site.register(survey.models.Description)


class FillerAdmin(admin.ModelAdmin):
    list_display = ['description', 'image', 'answer']

admin.site.register(survey.models.Filler, FillerAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ['description', 'image', 'item_set']


admin.site.register(survey.models.Item, ItemAdmin)


admin.site.register(survey.models.ItemSet)
