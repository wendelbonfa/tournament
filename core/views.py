# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, render
import json
import pytz
import random
from datetime import datetime
from core.models import Deductions, Athlete, \
    Tournament, TypeGrades, Grades, Formula
from django.template.response import TemplateResponse

def index(request):
    context = {}
    template = "main.html"
    return TemplateResponse(request, template, context)
