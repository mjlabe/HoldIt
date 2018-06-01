import datetime
from django.db.models import Count
from controlcenter import Dashboard, widgets, app_settings
from HoldApp.models.models import Case, Packet
from collections import defaultdict
from django.utils import timezone, timesince
from controlcenter.widgets.core import WidgetMeta


def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'packet':
        kwargs["queryset"] = Packet.objects.filter(case__status='New').all()
    return super(CaseAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


# class CaseInline(admin.StackedInline):
#     model = Case
#     show_change_link = True
#     extra = 0
#     fields = ('title',)
#     readonly_fields = ('title',)


class PacketAdmin(widgets.ItemList):
    model = Packet
    list_display = ('title', 'summary', 'created_date', 'mod_date')


class CaseAdmin(widgets.ItemList):
    model = Case
    list_display = ('title', 'file1', 'file2', 'packet', 'status', 'created_date', 'mod_date')
    list_editable = ('packet',)
    
    
class LatestCasesWidget(widgets.ItemList):
    # Displays latest 20 Cases in the the status
    title = 'Ciao latest Cases'
    model = Case
    queryset = (model.objects
                     .select_related('packet')
                     .filter(created_date__gte=timezone.now().date(),
                             status='New'))
                     # .Case_by('pk'))
    # This is the magic
    list_display = [app_settings.SHARP, 'pk', 'packet', 'ago']

    # If list_display_links is not defined, first column to be linked
    list_display_links = ['pk']

    # Makes list sortable
    sortable = True

    # Shows last 20
    limit_to = 20

    # Display time since instead of date.__str__
    def ago(self, obj):
        return timesince(obj.created_date)
    
    
STATUS = [
    'New',
    'In Progress',
    'Complete',
]

# Metaclass arguments are: class name, base, properties.
latest_cases_widget = [WidgetMeta(
                           '{}LatestCases'.format(name),
                           (LatestCasesWidget,),
                           {'queryset': (LatestCasesWidget
                                            .queryset
                                            .filter(status=name)),
                            'title': name + ' cases',
                            'changelist_url': (
                                 Case, {'status__name__exact': name})})
                        for name in STATUS]


class CaseLineChart(widgets.LineChart):
    # Displays Cases dynamic for last 7 days
    title = 'Cases this week'
    model = Case
    limit_to = 7
    # Lets make it bigger
    width = widgets.LARGER

    class Chartist:
        # Visual tuning
        options = {
            'axisX': {
                'labelOffset': {
                    'x': -24,
                    'y': 0
                },
            },
            'chartPadding': {
                'top': 24,
                'right': 24,
            }
        }

    def legend(self):
        # Displays status names in legend
        return STATUS

    def labels(self):
        # Days on x-axis
        today = timezone.now().date()
        labels = [(today - datetime.timedelta(days=x)).strftime('%d.%m')
                  for x in range(self.limit_to)]
        return labels

    def series(self):
        # Some dates might not exist in database (no Cases are made that
        # day), makes sure the chart will get valid values.
        series = []
        for status in self.legend:
            # Sets zero if date not found
            item = self.values.get(status, {})
            series.append([item.get(label, 0) for label in self.labels])
        return series

    def values(self):
        # Increases limit_to by multiplying it on restautant quantity
        limit_to = self.limit_to * len(self.legend)
        queryset = self.get_queryset()
        # This is how `GROUP BY` can be made in django by two fields:
        # status name and date.
        # Caseed.created is datetime type but we need to group by days,
        # here we use `DATE` function (sqlite3) to convert values to
        # date type.
        # We have to sort by the same field or it won't work
        # with django ORM.
        queryset = (queryset.extra({'baked':
                                        'DATE(created_date)'})
                        .select_related('status')
                        .values_list('status__name', 'baked')
                        .Case_by('-baked')
                        .annotate(ocount=Count('pk'))[:limit_to])

        # The key is status name and the value is a dictionary of
        # date:Case_count pair.
        values = defaultdict(dict)
        for status, date, count in queryset:
            # `DATE` returns `YYYY-MM-DD` string.
            # But we want `DD-MM`
            day_month = '{2}.{1}'.format(*date.split('-'))
            values[status][day_month] = count
        return values


class MyDashboard(Dashboard):
    widgets = (PacketAdmin, CaseAdmin, LatestCasesWidget, CaseLineChart)
