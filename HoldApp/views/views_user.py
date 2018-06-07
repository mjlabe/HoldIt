from HoldApp.models.models import Report, Case
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Q
from django.views import View


def is_user(user):
    return user.groups.filter(name='User').exists() | user.groups.filter(name='Contributor').exists() | \
           user.groups.filter(name='Worker').exists() | user.groups.filter(name='Admin').exists()


# TODO: limit the number of reports requested
@user_passes_test(is_user)
def case_list(request):
    """Display a list of Reports sorted by newest to oldest"""

    cases = Case.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'user/report_list.html', {'cases': cases})


# TODO: create specific classes for each case type and the view logic to decide which is used
class CaseView(View):
    """Display Case details.

    This class can be used by specific case types to inherit Case details."""
    @method_decorator(user_passes_test(is_user))
    def dispatch(self, request, *args, **kwargs):
        """Display the detailed view for a Report"""

        case = get_object_or_404(Case, pk=kwargs['pk'])
        return render(request, 'user/report_detail.html', {'case': case})


# @user_passes_test(is_user)
# def case_detail(request, pk):
#     """Display the detailed view for a Report"""
#
#     case = get_object_or_404(Case, pk=pk)
#     return render(request, 'user/report_detail.html', {'case': case})


# class ReportDetail(View):
#     form_class = ReportForm
#     initial = {'key': 'value'}
#     template_name = 'user/report_detail.html'
#
#     @method_decorator(user_passes_test(is_user))
#     def get(self, request, *args, **kwargs):
#         form = self.form_class(initial=self.initial)
#         return render(request, self.template_name, {'form': form})
#
#     @method_decorator(user_passes_test(is_user))    # TODO: dont do this!!!!
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             # <process form cleaned data>
#             return HttpResponseRedirect('/success/')
#
#         return render(request, self.template_name, {'form': form})

class OrderListJson(BaseDatatableView):
    # The model we're going to show
    model = Case

    # define the columns that will be returned
    columns = ['title', 'summary', 'created_date']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    order_columns = ['title', 'summary', 'created_date']

    # set max limit of records returned, this is used to protect our site if someone tries to attack our site
    # and make it return huge amount of data
    max_display_length = 500

    # def render_column(self, row, column):
    #     # We want to render user as a custom column
    #     if column == 'title':
    #         # escape HTML for security reasons
    #         return escape('{0} {1}'.format(row.customer_firstname, row.customer_lastname))
    #     else:
    #         return super(OrderListJson, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(title__istartswith=search)

        # more advanced example using extra parameters
        filter_title = self.request.GET.get(u'customer', None)

        if filter_title:
            customer_parts = filter_title.split(' ')
            qs_params = None
            for part in customer_parts:
                q = Q(title__istartswith=part) | Q(title__istartswith=part)
                qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        return qs
