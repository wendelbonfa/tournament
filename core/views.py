# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json
import pytz
import random
from datetime import datetime
from tournament.models import Athlete, Category, \
    Championship, ChampionshipVSAthlete, Department,\
    Gender, Order, GroupsChampionship, \
    UserProfile, Deductions, Representatives
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.core import serializers
from django.http import Http404

def check_group(*groups):

    def decorator(function):
        def wrapper(request, *args, **kwargs):
            if request.user.groups.filter(name__in=groups).exists():
                return function(request, *args, **kwargs)
            raise Http404

        return wrapper

    return decorator


def index(request):
    context = {}
    template = "main.html"
    return TemplateResponse(request, template, context)


def load_categories(request):
    department = request.POST['department']
    categories = Category.objects.filter(department_id=int(department))
    context = serializers.serialize('json', categories)
    return HttpResponse(context)


def load_groups(request):  
    if request.POST['change'] == 'department':
        department = int(request.POST['department'])
        categories = Category.objects.filter(department_id=department, amount__gte=2)
        athletes = Athlete.objects.filter(department__id=department, categories=categories[0])
        groupschampionship = GroupsChampionship.objects.filter(gym_id=request.user.id, categories=categories[0]).order_by('id')  
        sel_athletes = []
        for i in groupschampionship:
            sel_athletes = sel_athletes + [ i for i in i.athletes.all().values_list('id', flat=True)]  
    elif request.POST['change'] == 'category':
        department = int(request.POST['department'])
        category = int(request.POST['category'])
        categories = Category.objects.filter(department_id=department, amount__gte=2)
        athletes = Athlete.objects.filter(department__id=department, categories__id=category)
        groupschampionship = GroupsChampionship.objects.filter(gym_id=request.user.id, categories__id=category).order_by('id')  
        sel_athletes = []
        for i in groupschampionship:
            sel_athletes = sel_athletes + [ i for i in i.athletes.all().values_list('id', flat=True)]
    context = {
      'categories': serializers.serialize('json', categories),
      'athletes': serializers.serialize('json', athletes.exclude(id__in=sel_athletes)),
      'athletes_': serializers.serialize('json', athletes.filter(id__in=sel_athletes)),
      'groupschampionship': serializers.serialize('json', groupschampionship)
    }
    return HttpResponse(json.dumps(context))  


def remove(request):
    context = {}  
    msg = ""
    try:
      if request.POST:
        if request.POST['delete']:
            if 'athleta' in request.POST:
                instance = Athlete.objects.get(pk=int(request.POST['athleta']))
                name = instance.name
                instance.delete()
                msg = f"O atleta {name} foi removido com sucesso"
            if 'representative_id' in request.POST:
                instance = Representatives.objects.get(id=request.POST['representative_id'])
                name = instance.name
                instance.delete()            
                msg = f"O representante {name} foi removido com sucesso"
      
    except:
      msg = "Erro na remoção do atleta"
    context['msg'] = msg
    return HttpResponse(json.dumps(context))  


@login_required(login_url='/accounts/login/')
@check_group("Administrators")
def prize_draw(request):
    
    if request.POST:
        championship = request.POST["championship"]        
        championship_md = Championship.objects.get(id=int(championship))
        category = request.POST["category"]
        category_md = Category.objects.get(id=int(category))
        gender = request.POST["gender"]
        subathletes = ChampionshipVSAthlete.objects.filter(championship=championship_md, athlete__categories__id=int(category), athlete__gender__id=int(gender))
        position = [i for i in range(1, (len(subathletes))+1)]
        random.shuffle(position)
        csv_list = {}
        for i, l in enumerate(subathletes):
            try:
                order = Order.objects.get(subscription=l.subscription, championship__id=int(championship), category__id=int(category), athlete=l.athlete)
                order.championship = championship_md
                order.gym = UserProfile.objects.get(user=l.gym)
                order.subscription = l.subscription
                order.category = category_md
                order.athlete = l.athlete
                order.position = position[i]
                order.save()
            except:
                order = Order()
                order.championship = championship_md
                order.gym = UserProfile.objects.get(user=l.gym)
                order.subscription = l.subscription              
                order.category = category_md
                order.athlete = l.athlete
                order.position = position[i]
                order.save()    
            csv_list[position[i]] = (str(l.subscription).zfill(5), l.athlete.name, UserProfile.objects.get(user=l.gym).gym)

        context = {
          'csv_list': dict(sorted(csv_list.items()))
        }
        return HttpResponse(json.dumps(context))
  
    context = {}
    championships = Championship.objects.all().order_by('-id')    
    departments = Department.objects.all()
    categories = Category.objects.filter(department=departments[0]) 
    genders = Gender.objects.all()
    context = {
      'championships': championships,
      'departments': departments,
      'categories': categories,
      'genders': genders
    }
    template = "prize_draw.html"
    return TemplateResponse(request, template, context)


@login_required(login_url='/accounts/login/')
def athlete_register(request):
    u"""
      Função de cadastro/edição de atletas
    """
    if request.POST:
        try:
            edit = Athlete.objects.get(gym_id=request.user.id, name=request.POST['name'])
            edit.name = request.POST['name']
            edit.rg = request.POST['rg']
            edit.cpf = request.POST['cpf']
            edit.rg_file = request.FILES['rg_file']
            edit.cpf_file = request.FILES['cpf_file']            
            try:
                edit.name_resp = request.POST['name']
                edit.rg_resp  = request.POST['rg']
                edit.cpf_resp  = request.POST['cpf']
                edit.rg_file_resp  = request.FILES['rg_file']
                edit.cpf_file_resp  = request.FILES['cpf_file']            
            except:
                pass
            edit.gender = Gender.objects.get(id=int(request.POST['gender']))
            edit.gym = User.objects.get(id=request.user.id)
            edit.style = request.POST['style']
            edit.weight = request.POST['weight'].replace(",", ".")
            edit.age = request.POST['birth_date']
            edit.foto = request.FILES['foto']
            edit.medical_certificate = request.FILES['medical_certificate']
            edit.issue_date = request.POST['issue_date']
            edit.inatived = False          
            edit.save()          
            for style in request.POST.getlist('style'):
                edit.categories.add(style)
        except:
            try:
                new = Athlete()
                if Athlete.objects.all():
                    new.register_number = 1
                else:    
                    new.register_number = 1                 
                new.name = request.POST['name']
                new.rg = request.POST['rg']
                new.cpf = request.POST['cpf']
                new.rg_file = request.FILES['rg_file']
                new.cpf_file = request.FILES['cpf_file']
                try:
                    new.name_resp = request.POST['resp_name']
                    new.rg_resp  = request.POST['resp_rg']
                    new.cpf_resp  = request.POST['resp_cpf']
                    new.rg_file_resp  = request.FILES['resp_rg_file']
                    new.cpf_file_resp  = request.FILES['resp_cpf_file']            
                except:
                    pass                
                new.gender = Gender.objects.get(id=int(request.POST['gender']))
                new.gym = User.objects.get(id=request.user.id)
                new.style = request.POST['style']
                new.weight = request.POST['weight'].replace(",", ".")
                new.age = request.POST['birth_date']
                new.foto = request.FILES['foto']
                new.medical_certificate = request.FILES['medical_certificate']
                new.issue_date = request.POST['issue_date']
                new.inatived = False
                new.save()
                for style in request.POST.getlist('style'):
                    new.categories.add(style)                
            except Exception as e:
                return render(request,'erro_cadastro.html')
        
    athletes = Athlete.objects.filter(gym_id=request.user.id)
    try:
        profile = UserProfile.objects.get(user=request.user)
    except:
        context = {}
        template = "athlete_register_erro.html"
        return TemplateResponse(request, template, context)          
    genders = Gender.objects.all()
    categories = Category.objects.all().order_by('department_id')
    context = {
        'genders': genders,
        'athletes': athletes,
        'categories': categories,
        'profile': profile
    }
    template = "athlete_register.html"
    return TemplateResponse(request, template, context)  


@login_required(login_url='/accounts/login/')
def grades(request):
    if request.POST:
        championship = request.POST["championship"]
        category = request.POST["category"]
        gender = request.POST["gender"]  
        list_athlete = Order.objects.filter(championship__id=int(championship)).filter(category__id=int(category)).filter(athlete__gender__id=int(gender)).order_by('position').values_list('position', 'subscription', 'athlete__name', 'gym__gym', 'athlete__style')   
        return HttpResponse(json.dumps(list(list_athlete)))
    championships = Championship.objects.all().order_by('-id')
    departments = Department.objects.all()
    categories = Category.objects.filter(department=departments[0]) 
    genders = Gender.objects.all()  
    context = {
      'championships': championships,
      'departments': departments,
      'genders': genders,
      'categories': categories
    }
    template = "grades.html"
    return TemplateResponse(request, template, context)    


@login_required(login_url='/accounts/login/')
def deductions(request):
    deductions = Deductions.objects.all()
    if request.POST:
        championship = request.POST["championship"]
        category = request.POST["category"]
        gender = request.POST["gender"]  
        list_athlete = {
          'orders': json.dumps(list( Order.objects.filter(championship__id=int(championship)).filter(category__id=int(category)).filter(athlete__gender__id=int(gender)).order_by('position').values_list('position', 'subscription', 'athlete__name', 'gym__gym', 'athlete__style'))), 
          'deductions': serializers.serialize('json', deductions)
        }
        return HttpResponse(json.dumps(list_athlete))
    championships = Championship.objects.all().order_by('-id')
    departments = Department.objects.all()
    categories = Category.objects.filter(department=departments[0]) 
    genders = Gender.objects.all()  

    context = {
      'championships': championships,
      'departments': departments,
      'genders': genders,
      'categories': categories,
      'deductions': deductions
    }
    template = "deductions.html"
    return TemplateResponse(request, template, context)  


@login_required(login_url='/accounts/login/')
def enrolled(request):
    championships = Championship.objects.all().order_by('-id')  
    enrolled = None

    context = {
      'championships':championships,
      'enrolled': enrolled,
    }
    template = "enrolled.html"
    return TemplateResponse(request, template, context)


@login_required(login_url='/accounts/login/')
def championship_register(request):
    championships = Championship.objects.all().order_by('-id')  
    athletes = Athlete.objects.filter(gym_id=request.user.id)

    if request.POST:
        try:
            championship = Championship.objects.get(id=int(request.POST['championship']))
            number_subscriptions = championship.number_subscriptions + 1
            athlete = Athlete.objects.get(gym_id=request.user.id, id=int(request.POST['athlete']))
            new = ChampionshipVSAthlete()
            new.athlete = athlete
            new.championship = championship  
            new.subscription = number_subscriptions
            new.gym = request.user
            new.save()  
            championship.number_subscriptions = number_subscriptions
            championship.save()
        except:
            pass
    subscriptions = ChampionshipVSAthlete.objects.filter(athlete__in=athletes)
    context = {
      'championships':championships,
      'athletes': athletes,
      'subscriptions': subscriptions
    }
    template = "championship_register.html"
    return TemplateResponse(request, template, context)


@login_required(login_url='/accounts/login/')
def select_categories(request):
    athlete = None
    if request.GET:
        athlete = Athlete.objects.get(id=int(request.GET['athlete']))       
    if request.POST:
        department = Department.objects.get(id=int(request.POST['department']))    
        categories = Category.objects.filter(id__in=request.POST.getlist('categories'))
        athlete = Athlete.objects.get(id=int(request.POST['athlete']))
        athlete.department.add(department) 
        for i in categories:
          athlete.categories.add(i) 
        athlete.save()
    departments = Department.objects.all()
    categories = Category.objects.filter(department=departments[0])
    if not athlete:
        return redirect('/championship_register/')      
    context = {
        'departments': departments,
        'categories': categories,
        'athlete': athlete
    }
    template = "select_categories.html"
    return TemplateResponse(request, template, context)


def groups(request):

    if request.POST:
        newgroup = GroupsChampionship()
        newgroup.name = request.POST['name']        
        newgroup.championship = Championship.objects.get(id=int(request.POST['championship']))
        newgroup.gym = request.user
        newgroup.categories = Category.objects.get(id=request.POST['category'])
        newgroup.save()
        athletes = Athlete.objects.filter(id__in=request.POST.getlist('athlete'))
        for i in athletes:
          newgroup.athletes.add(i) 
        newgroup.save()      

    championships = Championship.objects.all().order_by('-id')  
    departments = Department.objects.all()
    categories = Category.objects.filter(department=departments[0], amount__gte=2)  
    athletes = Athlete.objects.filter(department=departments[0], categories=categories[0])
    groupschampionship = GroupsChampionship.objects.filter(gym_id=request.user.id, categories=categories[0]).order_by('id')  
    sel_athletes = []
    for i in groupschampionship:
        sel_athletes = sel_athletes + [ i for i in i.athletes.all().values_list('id', flat=True)]     
    context = {
      'departments': departments,
      'categories': categories,
      'athletes': athletes.exclude(id__in=sel_athletes),
      'groupschampionship': groupschampionship,
      'championships': championships
    }
    template = "groups.html"
    return TemplateResponse(request, template, context)
   

@login_required(login_url='/accounts/login/')
def summaries(request):
    if request.POST:
        championship = request.POST["championship"]
        category = request.POST["category"]
        gender = request.POST["gender"]  
        list_athlete = Order.objects.filter(championship__id=int(championship)).filter(category__id=int(category)).filter(athlete__gender__id=int(gender)).order_by('position').values_list('position', 'subscription', 'athlete__name', 'gym__gym', 'athlete__style')   
        return HttpResponse(json.dumps(list(list_athlete)))
    championships = Championship.objects.all().order_by('-id')
    departments = Department.objects.all()
    categories = Category.objects.filter(department=departments[0]) 
    genders = Gender.objects.all()  
    context = {
      'championships': championships,
      'departments': departments,
      'genders': genders,
      'categories': categories
    }
    template = "summaries.html"
    return TemplateResponse(request, template, context)   


@login_required(login_url='/accounts/login/')
def profile(request):
    try:
        profile = UserProfile.objects.get(user_id=request.user.id)
        gyn_id = profile.register_number
    except:
        gyn_id = len(UserProfile.objects.all()) + 1
        profile = None
        context = {} 
    
    try:
        representatives = Representatives.objects.filter(
            profile_id=profile.pk
        )
    except:
        representatives = []

    if request.POST:        
        if 'rep_name' in request.POST:
            try:
                representative = Representatives.objects.get(
                    profile_id=profile.id
                )
                representative.cel_phone = request.POST['rep_celphone']  
                representative.cpf = request.POST['rep_cpf']  
                representative.name =  request.POST['rep_name']                  
            except:
                representative = Representatives()
                representative.cel_phone = request.POST['rep_celphone']  
                representative.cpf = request.POST['rep_cpf']  
                representative.name =  request.POST['rep_name'] 
                representative.profile = profile
            representative.save()
        else:
            if profile:
                profile.register_number = request.POST['register_number']  
                profile.social_reason = request.POST['social_reason']  
                profile.fantasy_name = request.POST['fantasy_name']  
                profile.address = request.POST['address']  
                profile.phone = request.POST['phone']  
                profile.cel_phone = request.POST['cel_phone']  
                profile.whats_app = request.POST['whats_app']  
                profile.responsible = request.POST['responsible']  
                profile.cpf = request.POST['cpf']  
                profile.user = User.objects.get(id=request.user.id)
                if 'logo' in request.FILES and request.FILES['logo']:
                    profile.logo = request.FILES['logo'] 
                for style in request.POST.getlist('style'):
                    profile.categories.add(style)                   
            else:
                profile = UserProfile()
                profile.register_number = request.POST['register_number']  
                profile.social_reason = request.POST['social_reason']  
                profile.fantasy_name = request.POST['fantasy_name']                  
                profile.address = request.POST['address']  
                profile.phone = request.POST['phone']  
                profile.cel_phone = request.POST['cel_phone']  
                profile.whats_app = request.POST['whats_app']  
                profile.responsible = request.POST['responsible']  
                profile.cpf = request.POST['cpf']  
                if 'logo' in request.FILES and request.FILES['logo']:
                    profile.logo = request.FILES['logo'] 
                profile.user = User.objects.get(id=request.user.id)
                profile.inatived = True
                for style in request.POST.getlist('style'):
                    profile.categories.add(style)                   
            profile.save()            
   
    categories = Category.objects.all().order_by('department_id')
    template = "profile.html"
    context = {
        'gyn_id': gyn_id,
        'profile': profile,
        'categories': categories,
        'representatives': representatives
    }
    return TemplateResponse(request, template, context)   