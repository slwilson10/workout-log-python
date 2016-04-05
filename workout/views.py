from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.forms import ModelForm
from django.forms import TextInput
from django.forms import modelformset_factory
import json
from datetime import datetime
from .models import Workout

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        fields = '__all__'
        widgets = {
            'name':TextInput(attrs={'size':5}),
            'peak':TextInput(attrs={'size':1}),
            'cardio':TextInput(attrs={'size':1}),
            'fatburn':TextInput(attrs={'size':1}),
            'calories':TextInput(attrs={'size':2}),
            'heartrate':TextInput(attrs={'size':2}),
            'hours':TextInput(attrs={'size':1}),
            'minutes':TextInput(attrs={'size':1}),
            'seconds':TextInput(attrs={'size':1}),
            'distance':TextInput(attrs={'size':2}),
        }
def year(request):
    years = get_years()
    context = {'years': years}
    return render(request, 'year.html', context)

def month(request, year):
    year = datetime.strptime(year, '%Y').year
    months = Workout.objects.filter(date__year=year)
    context = {'months': months}
    return render(request, 'month.html', context)


def workout(request, year,  month):
    year = datetime.strptime(year, '%Y').year
    month = datetime.strptime(month,'%b').month
    workouts = Workout.objects.filter(date__year=year, date__month=month)
    workout_dates = get_dates()
    form = WorkoutForm()
    WorkoutFormset = modelformset_factory(Workout, form=WorkoutForm,
                         can_delete=True, can_order=True, extra=0)
    formset = WorkoutFormset(queryset=workouts.order_by('-date'))   
    context = {'workouts': workouts, 'formset': formset,
            'workout_dates': workout_dates, 'month': month}
    return render(request, 'list.html', context)
	
def delete(request, year, month, pk):
    workout = get_object_or_404(Workout, pk=pk)
    if request.method == 'DELETE':
        workout.delete()
        data = {'Delete':'ok'}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return redirect('list/'+year+'/'+month)

def update(request, month):
    WorkoutFormset = modelformset_factory(Workout, form=WorkoutForm)
    if request.method == 'POST':
        formset = WorkoutFormset(request.POST)
        if formset.is_valid():
            print ('POSTED')
            formset.save()
        return redirect('/list/'+year+'/'+month)
    else: print('NOT VALID')
    return redirect('/list/'+year+'/'+month)

def get_dates():
    workout_dates = []
    years = []
    all_workouts = Workout.objects.all()
    for w in all_workouts:
        y = w.date.year
        m = get_months(y)
        date = {'year':y,'months':m}
        if date not in workout_dates:
            workout_dates.append(date)
    return workout_dates

def get_years():
    years_group = []
    years = []
    for w in Workout.objects.all():
        year = w.date.year
        if year not in years:
            years.append(year)
    
    for y in years:
        workouts = len(Workout.objects.filter(date__year=y))
        group = {'year': y,'workouts': workouts}
        years_group.append(group)
    return years_group

def get_months(year):
    workouts = Workout.objects.filter(date__year=year)
    months = []
    for w in workouts:
       # month = w.date.strftime('%m')
        month = w.date.strftime('%b')
        if month not in months:
            months.append(month)
    return months
