from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Etudiant)
admin.site.register(Class)
admin.site.register(Parent)
admin.site.register(Enseignant)
admin.site.register(Matiere)
admin.site.register(Inscription)
admin.site.register(Enseigner)
admin.site.register(Evaluation)
admin.site.register(Note)
admin.site.register(Timetable)
admin.site.register(Salaire)
admin.site.register(Partenaire)
admin.site.register(Pret)
admin.site.register(Depense)
admin.site.register(Mois)
admin.site.register(ParentmoisPayment)

