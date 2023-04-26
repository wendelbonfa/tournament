# -*- coding: UTF-8 -*-
__author__ = 'Wendel Bonfá'

from django.db import models
from django.utils.translation import gettext_lazy as _

class Athlete(models.Model):
    _(u"""
        Model that identifies the athlete 
    """)

    register_number = models.DecimalField(
        verbose_name=_(u"Athlete number"),
        help_text=_(u"Athlete number."),
        max_digits=10,
        decimal_places=2          
    )

    name = models.CharField(
        verbose_name=_(u"Athlete name"),
        help_text=_(u"Athlete name."),
        max_length=1000,
    )

    association = models.CharField(
        verbose_name=_(u"Athlete association"),
        help_text=_(u"Athlete association."),
        max_length=1000,
        null=True,
        blank=True        
    )

    style = models.CharField(
        verbose_name=_(u"Presentation style"),
        help_text=_(u"Presentation style."),
        max_length=1000,
        null=True,
        blank=True        
    )  

    def __str__(self):
        return _(u"{0}".format(self.name))

    class Meta:
        verbose_name = _(u"Athlete")
        verbose_name_plural = _(u"Athletes") 


class Tournament(models.Model):
    _(u"""
        model that identifies the tournament
    """ )
    indenfification = models.CharField(
        verbose_name=_(u"tournament indenfification"),
        help_text=_(u"tournament indenfification."),
        max_length=1000,
    )

    date = models.DateTimeField(
        verbose_name=_(u"tournament date"),
        help_text=_(u"tournament date."),
    )    

    def __str__(self):
        return "{0}".format(self.indenfification)

    class Meta:
        verbose_name = _(u"Tournament")
        verbose_name_plural = _(u"Tournaments")


class Formula(models.Model):
    _(u"""
        calculation formula template
    """)
    description = models.CharField(
        verbose_name=_(u"formula description"),
        help_text=_(u"formula description."),
        max_length=1000,
    )

    formula = models.CharField(
        verbose_name=_(u"formula"),
        help_text=_(u"formula."),
        max_length=1000,
    )

class TypeGrades(models.Model):
    _(u"""
        model with types of notes
    """)
    description = models.CharField(
        verbose_name=_(u"Types of notes"),
        help_text=_(u"Types of notes."),
        max_length=1000,
    )

class Grades(models.Model):
    _(u"""
        Model that associates the grades to the athlete 
    """)    
    athlete = models.ForeignKey(
        Athlete,
        verbose_name=_(u"Athlete"),
        help_text=_(u"athlete to whom the grade will be assigned."),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )   

    tournament = models.ForeignKey(
        Tournament,
        verbose_name=_(u"Tournament"),
        help_text=_(u"tournament the athlete is participating in."),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )  

    grade = models.DecimalField(
        verbose_name=_(u"Grade"),
        help_text=_(u"Grade"),
        max_digits=10,
        decimal_places=2      
    )   

    type_grate = models.ForeignKey(
        TypeGrades,
        verbose_name=_(u"Type grades"),
        help_text=_(u"Type grades."),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )   

    validation = models.BooleanField(
        verbose_name=_(u"score validation"),
        help_text=_(u"score validation by the head judge"),   
    )   

    def __str__(self):
        return "{0}-{1}".format(self.tournament, self.athlete)

    class Meta:
        verbose_name = _(u"Grades")
        verbose_name_plural = _(u"Grades")      

class Deductions(models.Model):
    _(u"""
        Model that associates the deductions to the athlete 
    """)    
    athlete = models.ForeignKey(
        Athlete,
        verbose_name=_(u"Athlete"),
        help_text=_(u"athlete to whom the deduction will be assigned."),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )   

    tournament = models.ForeignKey(
        Tournament,
        verbose_name=_(u"Tournament"),
        help_text=_(u"tournament the athlete is participating in."),
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )  

    deductions = models.DecimalField(
        verbose_name=_(u"deductions"),
        help_text=_(u"deductions"),
        max_digits=10,
        decimal_places=2      
    )    

    def __str__(self):
        return "{0}-{1}".format(self.tournament, self.athlete)

    class Meta:
        verbose_name = _(u"Deductions")
        verbose_name_plural = _(u"Deductions")  