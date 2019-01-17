# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Employee
from .forms import EmployeeForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.db.models import Q



# Create your views here.

def show_employees(request):
    global employees
    if request.is_ajax():
        text = request.GET['children_id']
        node = Employee.objects.get(id=text)
        employees = node.get_descendants(include_self = "True").filter(level__lte=node.level + 3)
        data = {}
        data['employees'] = employees
        response = render(request, 'employees_list.html', {'employees': employees})
        return response
    else:
        employees = Employee.objects.all().filter(level__lte=1)
        return render(request, "employees.html", {'employees': employees})

def change_boss(request):
    if request.is_ajax():
        boss_id = request.GET['boss_id']
        children_id = request.GET['children_id']
        if boss_id == "nestable":
            current_child = Employee.objects.get(id=children_id)
            current_child.move_to(None, 'first-child')
            current_child.save()
        else:
            parent = Employee.objects.get(id=boss_id)
            current_child = Employee.objects.get(id=children_id)
            current_child.move_to(parent, 'first-child')
            current_child.save()
        return HttpResponse('')

def show_employees_all(request):
    if request.user.is_authenticated:
        if request.is_ajax():
            sort_by = request.GET['sort_by']
            search_text = request.GET['q_search']
            employees = Employee.objects.order_by(sort_by).filter(Q(employment_position__icontains=search_text))
            employees = employees | Employee.objects.order_by(sort_by).filter(Q(name__icontains=search_text))
            employees = employees | Employee.objects.order_by(sort_by).filter(Q(salary__icontains=search_text))
            employees = employees | Employee.objects.order_by(sort_by).filter(Q(employment_start_date__icontains=search_text))
            context = {}
            current_page = Paginator(list(employees), 20)
            page = request.GET['page']
            try:
                context['employees'] = current_page.page(page)
            except PageNotAnInteger:
                context['employees'] = current_page.page(1)
            except EmptyPage:
                context['employees'] = current_page.page(current_page.num_pages)
            response = render(request, 'employees_all_sort.html', context)
            return response
        else:
            employees = Employee.objects.order_by('date_added')
            context = {}
            current_page = Paginator(list(employees), 20)
            page = request.GET.get('page')
            try:
                context['employees'] = current_page.page(page)
            except PageNotAnInteger:
                context['employees'] = current_page.page(1)
            except EmptyPage:
                context['employees'] = current_page.page(current_page.num_pages)
            return render(request, 'employees_all.html', context)
    else:
        return HttpResponseRedirect("/users/login")

def edit (request, id):
    employee = Employee.objects.get(id=id)
    if request.method != 'POST':
        form = EmployeeForm(instance=employee, prefix='form')
        request.session['return_path'] = request.META.get('HTTP_REFERER','/')
    else:
        form = EmployeeForm(request.POST, instance=employee, prefix='form')
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
        return HttpResponseRedirect(request.session['return_path'])
    context = {'form': form}
    return render(request, 'edit.html', context)

def delete (request, id):
    parent = Employee.objects.get(id=id)
    for child in parent.get_children():
        print(child)
        child.parent = parent.parent
        child.save()
    parent.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
