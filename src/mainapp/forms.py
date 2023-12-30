from django import forms
from .models import *

class etudiantForm(forms.ModelForm):
    class Meta:
        model= Etudiant
        fields = "__all__"

class enseignantForm(forms.ModelForm):
    class Meta:
        model= Enseignant
        fields = "__all__"

class classesForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__"

class matiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = "__all__"

class parentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"

class inscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = "__all__"

class affectationForm(forms.ModelForm):
    class Meta:
        model = Enseigner
        fields = "__all__"

class evaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = "__all__"

class noteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = "__all__"

class timetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = "__all__"

class salaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = "__all__"

class partenaireForm(forms.ModelForm):
    class Meta:
        model = Partenaire
        fields = "__all__"

class pretForm(forms.ModelForm):
    class Meta:
        model = Pret
        fields = "__all__"

class depenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = "__all__"

class paymentForm(forms.ModelForm):
    class Meta:
        model = ParentmoisPayment
        fields = "__all__"

class moisForm(forms.ModelForm):
    class Meta:
        model = Mois
        fields = "__all__"