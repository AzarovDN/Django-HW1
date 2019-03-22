from django.shortcuts import render_to_response, redirect
from django.urls import reverse
import csv
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open('data-398-2018-08-30.csv', newline='', encoding='cp1251') as csvfile:
        data = csv.DictReader(csvfile)
        bus_stations_dict = {}
        data_list = []
        for line in data:
            bus_stations_dict['Name'] = line['Name']
            bus_stations_dict['Street'] = line['Street']
            bus_stations_dict['District'] = line['District']
            data_list.append(bus_stations_dict)
            bus_stations_dict = {}

    paginator = Paginator(data_list, 10)
    page = request.GET.get('page')

    context = {}
    context['bus_stations'] = paginator.get_page(page)

    try:
        context['current_page'] = paginator.page(page).number
    except PageNotAnInteger:
        # Если None, то выбираем первую страницу
        context['current_page'] = paginator.page(1).number

    try:
        context['prev_page_url'] = f'bus_stations?page={paginator.get_page(page).previous_page_number()}'
    except EmptyPage:
        context['prev_page_url'] = None
    try:
        context['next_page_url'] = f'bus_stations?page={paginator.get_page(page).next_page_number()}'
    except EmptyPage:
        context['next_page_url'] = None

    return render_to_response('index.html', context)
