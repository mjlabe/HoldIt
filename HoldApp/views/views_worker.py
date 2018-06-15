from django.shortcuts import render, redirect, get_object_or_404
from ..models.models import Packet
from ..forms import PacketForm
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from .views_user import CaseView

def is_worker(user):
    return user.groups.filter(name='Worker').exists() | user.groups.filter(name='Admin').exists()


@user_passes_test(is_worker)
def packet_list_assigned(request):
    """View assigned packets.

    Display a list of Reports sorted by newest to oldest"""

    packets = Packet.objects.filter(assignedUser=request.user).order_by('-created_date')
    return render(request, 'worker/packet_list.html', {'packets': packets})


@user_passes_test(is_worker)
def packet_list_queue(request):
    """View assigned packets.

    Display a list of Reports sorted by newest to oldest"""

    packets = Packet.objects.filter(assignedUser__isnull=True).order_by('-created_date')
    return render(request, 'worker/packet_list.html', {'packets': packets})


@user_passes_test(is_worker)
def packet_detail(request, pk):
    """View assigned packet.

    This view combines the Report model and the corresponding data model. This needs to be made into an abstract class
    that can be implemented by ths specific views of different case types.
    """

    packet = get_object_or_404(Packet, pk=pk)
    cases = packet.case_set.all()

    return render(request, "worker/packet_detail.html", {'packet': packet, 'cases': cases})


def packet_edit(request, pk):
    """Display the New Report form.

    This view combines the Report model and the corresponding data model. This needs to be made into an abstract class
    that can be implemented by ths specific views of different case types.
    """

    packet = get_object_or_404(Packet, pk=pk)

    # TODO: make this an abstract class to handle every type of report
    if request.method == "POST":
        packet_form = PacketForm(request.POST)

        if packet_form.is_valid():
            packet = packet_form.save()

            # TODO: How to save relationship?

            return redirect('packet_edit', pk=packet.pk)

    else:
        packet_form = PacketForm(instance=packet)

    return render(request, "worker/packet_edit.html", {'packet_form': packet_form})


# class CaseEditView(CaseView):
#     """Display Case details.
#
#     This class can be used by specific case types to inherit Case details."""
#     @method_decorator(user_passes_test(is_worker))
#     def dispatch(self, request, *args, **kwargs):
#         """Display the detailed view for a Report"""
#
#         case = get_object_or_404(Case, pk=kwargs['pk'])
#         return render(request, 'user/report_detail.html', {'case': case})
