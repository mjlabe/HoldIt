import datetime
from django.db.models import Count
from controlcenter import Dashboard, widgets, app_settings
from HoldApp.models.models import Case, Packet
from collections import defaultdict
from django.utils import timezone, timesince
from controlcenter.widgets.core import WidgetMeta


# def formfield_for_foreignkey(self, db_field, request, **kwargs):
#     if db_field.name == 'packet':
#         kwargs["queryset"] = Packet.objects.filter(case__status='New').all()
#     return super(CaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# class CaseInline(admin.StackedInline):
#     model = Case
#     show_change_link = True
#     extra = 0
#     fields = ('title',)
#     readonly_fields = ('title',)

STATUS_CHOICES = (
    ('N', 'New'),
    ('P', 'In Progress'),
    ('C', 'Complete')
)


class PacketAllAdmin(widgets.ItemList):
    model = Packet
    title = 'All Packets'
    list_display = ('title', 'summary', 'assignedUser', 'created_date', 'mod_date')


class PacketAssignedAdmin(widgets.ItemList):
    model = Packet
    title = 'Assigned'
    list_display = ('title', 'summary', 'assignedUser', 'created_date', 'mod_date')
    queryset = model.objects.filter(assignedUser__isnull=False)


class PacketUnassignedAdmin(widgets.ItemList):
    model = Packet
    title = 'Unassigned'
    list_display = ('title', 'summary', 'created_date', 'mod_date')
    queryset = model.objects.filter(assignedUser__isnull=True)


class CaseNewAdmin(widgets.ItemList):
    model = Case
    title = 'New Cases'
    list_display = ('title', 'file1', 'file2', 'packet', 'created_date', 'mod_date')
    list_editable = ('packet',)
    queryset = model.objects.filter(status='N')


class CaseInProgressAdmin(widgets.ItemList):
    model = Case
    title = 'In Progress'
    list_display = ('title', 'file1', 'file2', 'packet', 'created_date', 'mod_date')
    list_editable = ('packet',)
    queryset = model.objects.filter(status='P')


class CaseCompleteAdmin(widgets.ItemList):
    model = Case
    title = 'Complete'
    list_display = ('title', 'file1', 'file2', 'packet', 'created_date', 'mod_date')
    list_editable = ('packet',)
    queryset = model.objects.filter(status='C')


class CaseStatusSingleBarChart(widgets.SingleBarChart):
    # Displays score of each restaurant.
    title = 'Metrics'
    model = Case

    class Chartist:
        options = {
            # Displays only integer values on y-axis
            'onlyInteger': True,
            # Visual tuning
            'chartPadding': {
                'top': 24,
                'right': 0,
                'bottom': 0,
                'left': 0,
            }
        }

    def legend(self):
        # Duplicates series in legend, because Chartist.js
        # doesn't display values on bars
        return self.series

    def values(self):
        # Returns pairs of restaurant names and order count.
        queryset = self.get_queryset()
        return (queryset.values_list('status')
                        .annotate(number=Count('status'))
                        .order_by('status')[:self.limit_to])


class MyDashboard(Dashboard):
    widgets = (widgets.Group([PacketAllAdmin, PacketAssignedAdmin, PacketUnassignedAdmin]),
               widgets.Group([CaseNewAdmin, CaseInProgressAdmin, CaseCompleteAdmin]),
               CaseStatusSingleBarChart)
