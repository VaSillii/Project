import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import Paginator
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView

from .forms import FormRegister, FormEdit, FormComment
from .models import UserAccount, Profile, Education, NameEducationalInstitution, Comment, TypeWork, Specialization, \
    WorkPrice


class RegistrationFormView(FormView):
    form_class = FormRegister
    success_url = '/'
    template_name = 'registration/registration.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationFormView, self).form_invalid(form)


class CustomPasswordChangeView(PasswordChangeView):
    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required(login_url='accounts:login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def profile_detail(request, user_id):
    user = get_object_or_404(UserAccount, id=user_id)
    form = FormComment()

    if request.method == 'POST':
        form = FormComment(request.POST)
        if form.is_valid() and form.cleaned_data['text_message'] != '' and form.cleaned_data['assessment'] != '':
            user_form_comment = form.save(commit=False)
            user_form_comment.user_id = user_id
            user_form_comment.user_comment_id = form.cleaned_data['user_comment']
            user_form_comment.text_message = form.cleaned_data['text_message']
            user_form_comment.assessment = 0 if form.cleaned_data['assessment'] == '' else form.cleaned_data[
                'assessment']
            user_form_comment.save()

    comment = Comment.objects.filter(user_id=user_id)
    avg_review = comment.aggregate(Avg('assessment'))['assessment__avg']
    user_data = {
        'user_data': user,
        'flag_save': 0,
        'previous_page': request.GET['page'],
        'form': form,
        'avg_review': 0 if avg_review is None else round(avg_review, 2),
        'comments': comment,
    }
    return render(request, 'profile_detail.html', context=user_data)


@login_required(login_url='accounts:login')
def profile_view(request):
    form = FormEdit()
    user = get_object_or_404(UserAccount, email=request.user)
    university = NameEducationalInstitution.objects.all()
    type_work = TypeWork.objects.all()
    spec_work = Specialization.objects.all()
    user_data = {
        'user_data': user,
        'form': form,
        'university': university,
        'type_work': type_work,
        'spec_works': spec_work,
        'flag_save': 0
    }
    if request.method == 'GET':
        return render(request, 'profile.html', context=user_data)

    if request.method == 'POST':
        form = FormEdit(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save(commit=False)

            profile_user = user_form.profile

            profile_user.surname = form.cleaned_data['surname']
            profile_user.name = form.cleaned_data['name']
            profile_user.patronymic = form.cleaned_data['patronymic']
            profile_user.phone_number = form.cleaned_data['phone_number']
            profile_user.dob = None if form.cleaned_data['dob'] == '' else form.cleaned_data['dob']
            profile_user.about_me = None if form.cleaned_data['dob'] == '' else form.cleaned_data['about_me']
            profile_user.addition_info = None if form.cleaned_data['addition_info'] == '' else form.cleaned_data[
                'addition_info']
            profile_user.position = 'guest' if form.cleaned_data['position'] == '' else form.cleaned_data['position']
            profile_user.photo = None if form.cleaned_data['avatar_user'] == '' else form.cleaned_data['avatar_user']

            if form.cleaned_data['type_work'] != '' and form.cleaned_data['price'] != '':
                if user_form.profile.education is None:
                    profile_work = WorkPrice()
                else:
                    profile_work = user_form.profile.work_price

                profile_work.type_work_id = form.cleaned_data['type_work']
                profile_work.price = form.cleaned_data['price']
                profile_work.save()
                profile_user.work_price = profile_work

            if form.cleaned_data['university'] != '' and form.cleaned_data['faculty'] != '' and form.cleaned_data[
                'specialization'] != '' and form.cleaned_data['graduation_date'] != '':
                if user_form.profile.education is None:
                    profile_edu = Education()
                else:
                    profile_edu = user_form.profile.education
                profile_edu.name_university_id = form.cleaned_data['university']#NameEducationalInstitution.objects.get(id=form.cleaned_data['university'])
                profile_edu.faculty = form.cleaned_data['faculty']
                profile_edu.specialization = form.cleaned_data['specialization']
                profile_edu.graduation_date = form.cleaned_data['graduation_date']
                profile_edu.save()
                profile_user.education = profile_edu
            else:
                # return HttpResponse(profile_user.education.delete())
                profile_user.education = None

            profile_user.save()
            user_form.profile = profile_user
            user_form.username = form.cleaned_data['username']
            user_form.email = form.cleaned_data['email']
            user_form.save()

            user_data['user_data'] = user_form
            user_data['form'] = form
            user_data['flag_save'] = 1
        else:
            user_data['form'] = form
            user_data['flag_save'] = 2
    return render(request, 'profile.html', context=user_data)
