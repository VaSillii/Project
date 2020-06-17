from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from accounts.models import UserAccount, TypeWork, Specialization, Profile, Comment
from .forms import FormOrderWork
from .models import Order


def spec_view(request):
    return render(request, 'order_spec.html')


@login_required(login_url='accounts:login')
def my_orders(request):
    orders = Order.objects.filter(client=request.user)
    orders_to_do = Order.objects.filter(master=request.user)
    context = {
        'orders': orders,
        'orders_to_do': orders_to_do,
    }
    return render(request, 'my_order.html', context=context)


@login_required(login_url='accounts:login')
def order_view(request, category_id):
    users = UserAccount.objects.all()
    form = FormOrderWork()
    specialization = get_object_or_404(Specialization, id=category_id)

    try:
        type_work = TypeWork.objects.filter(specialization_id=category_id)

        if category_id == 1:
            masters = UserAccount.objects.filter(Q(profile__specialization_id=category_id) | Q(profile__position='master'))
        elif category_id == 2:
            masters = UserAccount.objects.filter(Q(profile__specialization_id=category_id) | Q(profile__position='programmer'))
        else:
            masters = UserAccount.objects.filter(Q(profile__specialization_id=category_id))
        avg = {}
        for item in masters:
            val_avd = Comment.avd_assessment(item.id)
            avg[item.username] = 0 if val_avd is None else val_avd
    except TypeWork.DoesNotExist:
        return HttpResponseNotFound()
    except UserAccount.DoesNotExist:
        return HttpResponseNotFound()

    if request.method == 'POST':
        form = FormOrderWork(request.POST, instance=request.user)
        if form.is_valid():
            Order.objects.create(
                client_id=request.user.id,
                master_id=form.cleaned_data['master'],
                spec_order_id=form.cleaned_data['spec_order'],
                type_work_id=form.cleaned_data['type_work'],
                date_of_completion=form.cleaned_data['date_of_completion'],
                price=form.cleaned_data['price']
            )
            return redirect('orders:my_order')

    context = {
        'form': form,
        'spec_id': specialization,
        'list_specialist': users,
        'type_work': type_work,
        'masters': masters,
        'avd': avg
    }
    return render(request, 'order.html', context=context)


class SpecialistsListView(ListView):
    context_object_name = 'list_specialist'
    template_name = 'specialist.html'

    def get_context_data(self, **kwargs):
        context = super(SpecialistsListView, self).get_context_data(**kwargs)
        context['number_page'] = self.request.GET.get('page')
        return context

    def get_queryset(self):
        data = UserAccount.objects.all()
        paginator = Paginator(data, 15)
        page = self.request.GET.get('page')
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        return data
