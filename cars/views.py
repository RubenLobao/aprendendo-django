from urllib import request
from cars.forms import CarModelForm
from django.shortcuts import render, redirect
from cars.models import Car
from django.views import View
from django.db.models import Q
from django.views.generic import ListView, CreateView


# def car_view(request):
#     cars = Car.objects.all()
#     search = request.GET.get('search', '')
#     if search:
#         cars = Car.objects.filter(model__icontains=search).order_by('model')

#     return render(
#         request,
#         'cars.html',
#         {'cars': cars}
#     )

# class CarsView(View):
#     def get(self, request):
#         cars = Car.objects.all()
#         search = request.GET.get('search', '')
#         if search:
#             cars = Car.objects.filter(
#                 Q(model__icontains=search) | Q(brand__name__icontains=search)
#             ).order_by('model')

#         return render(
#             request,
#             'cars.html',
#             {'cars': cars}
#         )

class CarsListView(ListView):
    model = Car
    template_name = 'cars.html'
    context_object_name = 'cars'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('model')
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(model__icontains=search) | Q(brand__name__icontains=search)
            )
        return queryset
    

# def new_car_view(request):
#     if request.method == 'POST':
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('cars_list')
#     else:
#         new_car_form = CarModelForm()
#     return render(request, 'new_car.html', {'new_car_form': new_car_form})

# class NewCarView(View):
#     def get(self, request):
#         new_car_form = CarModelForm()
#         return render(request, 'new_car.html', {'new_car_form': new_car_form})

#     def post(self, request):
#         new_car_form = CarModelForm(request.POST, request.FILES)
#         if new_car_form.is_valid():
#             new_car_form.save()
#             return redirect('cars_list')
#         return render(request, 'new_car.html', {'new_car_form': new_car_form})
    
class NewCarCreateView(CreateView):
    model = Car
    form_class = CarModelForm
    template_name = 'new_car.html'
    success_url = '/cars/'