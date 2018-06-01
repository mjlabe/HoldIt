from django.contrib import admin
from .models.models import Case, Packet


def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'packet':
        kwargs["queryset"] = Packet.objects.filter(case__status='New').all()
    return super(CaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class CaseInline(admin.StackedInline):
    model = Case
    show_change_link = True
    extra = 0
    fields = ('title',)
    readonly_fields = ('title',)


@admin.register(Packet)
class PacketAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'created_date', 'mod_date')
    inlines = [CaseInline]
    list_filter = ('created_date', 'mod_date')
    search_fields = ('title', 'summary',)
    advanced_filter_fields = (
        'title', 'summary', 'created_date', 'mod_date')
        # even use related fields as lookup fields
        # 'country__name', 'posts__title', 'comments__content')


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'file1', 'file2', 'packet', 'status', 'created_date', 'mod_date')
    list_filter = ('status', 'created_date', 'mod_date')
    list_editable = ('packet',)
    search_fields = ('title', 'summary', 'status',)
    advanced_filter_fields = (
        'title', 'packet', 'status', 'created_date', 'mod_date')
        # even use related fields as lookup fields
        # 'country__name', 'posts__title', 'comments__content')

