# -*- coding: UTF-8 -*-
__author__ = 'Wendel Bonfá'

from django.contrib import admin

from core.models import Deductions, Athlete, \
    Tournament, TypeGrades, Grades, Formula
from django.utils.translation import gettext_lazy as _

admin.site.register(Tournament)
admin.site.register(TypeGrades)
admin.site.register(Athlete)
admin.site.register(Formula)
admin.site.register(Grades)
admin.site.register(Deductions)
