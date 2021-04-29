from django.contrib import admin
from django.db.models import Count

from .models import *

# Register your models here.


# Registrace modelů v administraci aplikace
@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "film_count")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            # _ je skrytá proměnná, je součástí toho objektu
            _film_count=Count("film", distinct=True),
        )
        return queryset

    def film_count(self, obj):
        return obj._film_count

    film_count.admin_order_field = "_film_count"
    film_count.short_description = "Počet filmů"


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "rate_percent", "runtime_min")

    def release_year(self, obj):
        return obj.release_date.year

    def rate_percent(self, obj):
        return format_html("<b>{} %</b>", int(obj.rate * 10))

    def runtime_min(self, obj):
        return format_html("<span>{} min.</span>", int(obj.runtime))

    rate_percent.short_description = "Hodnocení filmu"
    release_year.short_description = "Rok uvedení"
    runtime_min.short_description = "Délka filmu"


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "filesize", "film_title")

    def film_title(self, obj):
        return obj.film.title
