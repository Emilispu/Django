from django.contrib import admin
from .models import Pages, PageReview


class PagesAdmin(admin.ModelAdmin):
    list_display = ("title", "created_data", "href_name")


class PageReviewAdmin(admin.ModelAdmin):
    list_display = ("title", "reviewer", "data_created", "content")


admin.site.register(Pages, PagesAdmin)
admin.site.register(PageReview, PageReviewAdmin)
