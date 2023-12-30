from django.shortcuts import render, redirect, HttpResponse,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Etudiant,Enseignant,Parent,Class,Matiere,Inscription,Enseigner,Evaluation,Note,Timetable,Salaire,Partenaire,Pret,Depense,ParentmoisPayment,Mois
from .forms import etudiantForm, enseignantForm, classesForm, matiereForm, parentForm, inscriptionForm, affectationForm ,evaluationForm, noteForm , timetableForm,salaireForm,partenaireForm,pretForm,depenseForm,paymentForm,moisForm
from django.shortcuts import render
from django.contrib import messages
from tablib import Dataset
from django.db.models import Sum
from django.contrib import messages
from .resources import EtudiantResource, ParentResource, EnseignantResource ,MatiereResource ,InscriptionResource, NoteResource
# Create your views here.

@login_required
def home(request):
    classes = Class.objects.all()
    gender_percentages = []

    for classe in classes:
        students_in_class = Etudiant.objects.filter(id_class=classe)
        total_students = students_in_class.count()

        if total_students > 0:
            girls_count = students_in_class.filter(sexe='أنثى').count()
            boys_count = students_in_class.filter(sexe='ذكر').count()

            girls_percentage = (girls_count / total_students) * 100
            boys_percentage = (boys_count / total_students) * 100

            gender_percentages.append({
                'class': classe.libelle,
                'girls_percentage': girls_percentage,
                'boys_percentage': boys_percentage,
            })
    # Calculate the sum of students, teachers, parents
    total_students = Etudiant.objects.count()
    total_teachers = Enseignant.objects.count()
    total_parents = Parent.objects.count()

    # Calculate the profit
    total_montant_paye = ParentmoisPayment.objects.aggregate(total_montant_paye=Sum('montant_paye'))['total_montant_paye'] or 0
    total_pret_pay = Pret.objects.aggregate(total_pret_pay=Sum('pay'))['total_pret_pay'] or 0
    total_expenses = Salaire.objects.aggregate(total_salaires=Sum('salaire'))['total_salaires'] or 0
    total_expenses += Depense.objects.aggregate(total_depenses=Sum('montant_total'))['total_depenses'] or 0
    total_pret_amount = Pret.objects.aggregate(total_pret_amount=Sum('pret'))['total_pret_amount'] or 0

    total_profit = (total_montant_paye + total_pret_pay) - (total_expenses + total_pret_amount)

    # Create a context dictionary with the calculated values
    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        'total_profit': total_profit,
        'gender_percentages':gender_percentages,
    }
    # Render the template with the context
    return render(request, 'home.html', context)
# etudiants
def etudiant(request):
    all_etudiant= Etudiant.objects.all()
    return render(request,"etudiants/index.html",{"etudiants": all_etudiant,"navbar":'etudiant'})


def load_form_etudiant(request):
    form = etudiantForm()
    parents = Parent.objects.all()
    classes = Class.objects.all()
    return render(request, "etudiants/add.html",{'form':form,"navbar":'etudiant','parents':parents,'classes':classes})
def add_etudiant(request):
    if request.method == 'POST':
        form = etudiantForm(request.POST)
        if form.save():
            messages.success(request, 'تم إضافة الطالب بنجاح')
            return redirect('etudiant')


def edit_etudiant(request, id):
    etudiant = Etudiant.objects.get(id=id)
    parents = Parent.objects.all()
    classes = Class.objects.all()
    form = etudiantForm()
    return render(request,'etudiants/edit.html',{'etudiant':etudiant,"navbar":'etudiant','form':form,'parents':parents,'classes':classes})
def update_etudiant(request, id):
    etudiant = Etudiant.objects.get(id=id)
    form = etudiantForm(request.POST, instance=etudiant)
    form.save()
    messages.info(request, 'تم تعديل الطالب بنجاح')
    return redirect('etudiant')
def delete_etudiant(request, id):
    etudiant = Etudiant.objects.get(id=id)
    etudiant.delete()
    messages.warning(request, 'تم إزالة الطالب بنجاح')
    return redirect('etudiant')
def show_etudiant(request, id):
    etudiant = Etudiant.objects.get(id=id)
    parents = Parent.objects.all()
    classes = Class.objects.all()
    form = etudiantForm()
    return render(request,'etudiants/show.html',{'etudiant':etudiant,"navbar":'etudiant','form':form,'parents':parents,'classes':classes})

def import_etudiants(request):
    if request.method == 'POST':
        etudiant_resource = EtudiantResource()
        dataset = Dataset()
        new_etudiants = request.FILES['myfile']

        if not new_etudiants.name.endswith('xlsx'):
            messages.error(request, 'Le fichier doit être un fichier Excel (.xlsx)')
        else:
            imported_data = dataset.load(new_etudiants.read(), format='xlsx')
            for row in imported_data:
                # Associez les données du fichier Excel aux champs de modèle Etudiant
                etudiant = Etudiant(
                    nom=row[0],
                    prenom=row[1],
                    nom_fr=row[2],
                    prenom_fr=row[3],
                    date_naiss=row[4],
                    sexe=row[5],
                    NNI=row[6],
                    RIM=row[7],
                    date_inscription=row[9],
                    frais_mensuels=row[11],
                )
                # Associez l'ID du parent et de la classe en utilisant les noms du parent et du libellé de la classe (comme dans les exemples précédents)
                etudiant.id_parent = Parent.objects.get(nom=row[8])
                etudiant.id_class = Class.objects.get(libelle=row[10])
                etudiant.save()
            messages.success(request, 'تم إضافة الطلاب بنجاح')
    all_etudiant = Etudiant.objects.all()
    return render(request, 'etudiants/index.html',{"etudiants": all_etudiant,"navbar":'etudiant'})


# parents
def parent(request):
    all_parent= Parent.objects.all()
    return render(request,"parents/index.html",{"parents": all_parent,"navbar":'parent'})

def load_form_parent(request):
    form = parentForm()
    return render(request, "parents/add.html",{'form':form,"navbar":'parent'})
def add_parent(request):
    form = parentForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الوكيل بنجاح')
    return redirect('parent')
def edit_parent(request, id):
    parent = Parent.objects.get(id=id)
    form = parentForm()
    return render(request,'parents/edit.html',{'parent':parent,"navbar":'parent','form':form})
def update_parent(request, id):
    parent = Parent.objects.get(id=id)
    form = parentForm(request.POST, instance=parent)
    form.save()
    messages.info(request, 'تم تعديل الوكيل بنجاح')
    return redirect('parent')
def delete_parent(request, id):
    parent = Parent.objects.get(id=id)
    parent.delete()
    messages.warning(request, 'تم إزالة الوكيل بنجاح')
    return redirect('parent')

def import_parents(request):
    if request.method == 'POST':
        etudiant_resource = ParentResource()
        dataset = Dataset()
        new_etudiants = request.FILES['myfile']

        if not new_etudiants.name.endswith('xlsx'):
            messages.error(request, 'Le fichier doit être un fichier Excel (.xlsx)')
        else:
            imported_data = dataset.load(new_etudiants.read(), format='xlsx')
            for row in imported_data:
                # Associez les données du fichier Excel aux champs de modèle Etudiant
                parent = Parent(
                    nom=row[0],
                    prenom=row[1],
                    mobile=row[2],
                    mobile2=row[3],
                )
                parent.save()

            messages.success(request, 'تم إضافة الوكلاء بنجاح')
    all_parent= Parent.objects.all()
    return render(request,"parents/index.html",{"parents": all_parent,"navbar":'parent'})

# inscription
def inscription(request):
    all_inscription= Inscription.objects.all()
    return render(request,"inscriptions/index.html",{"inscriptions": all_inscription,"navbar":'inscription'})
def load_form_inscription(request):
    form = inscriptionForm()
    etudiants = Etudiant.objects.all()
    matieres = Matiere.objects.all()
    return render(request, "inscriptions/add.html",{'form':form,"navbar":'inscription','etudiants':etudiants,'matieres':matieres})
def add_inscription(request):
    form = inscriptionForm(request.POST)
    form.save()
    return redirect('inscription')
def edit_inscription(request, id):
    inscription = Inscription.objects.get(id=id)
    form = inscriptionForm()
    etudiants = Etudiant.objects.all()
    matieres = Matiere.objects.all()
    return render(request,'inscriptions/edit.html',{'inscription':inscription,"navbar":'inscription','form':form,'etudiants':etudiants,'matieres':matieres})
def update_inscription(request, id):
    inscription = Inscription.objects.get(id=id)
    form = inscriptionForm(request.POST, instance=inscription)
    form.save()
    return redirect('inscription')
def delete_inscription(request, id):
    inscription = Inscription.objects.get(id=id)
    inscription.delete()
    return redirect('inscription')
def import_inscriptions(request):
    if request.method == 'POST':
        etudiant_resource = InscriptionResource()
        dataset = Dataset()
        new_etudiants = request.FILES['myfile']

        if not new_etudiants.name.endswith('xlsx'):
            messages.error(request, 'Le fichier doit être un fichier Excel (.xlsx)')
        else:
            imported_data = dataset.load(new_etudiants.read(), format='xlsx')
            for row in imported_data:
                inscription = Inscription(
                    annee=row[2],
                )
                inscription.id_etud = Etudiant.objects.get(nom=row[0])
                inscription.id_matiere = Matiere.objects.get(libelle=row[1])
                inscription.save()

            messages.success(request, 'Importation réussie')
    all_inscription = Inscription.objects.all()
    return render(request, 'inscriptions/index.html',{"inscriptions": all_inscription,"navbar":'inscription'})

# enseignants
def enseignant(request):
    all_enseignant= Enseignant.objects.all()
    return render(request,"enseignants/index.html",{"enseignants": all_enseignant,"navbar":'enseignant'})

def load_form_enseignant(request):
    form = enseignantForm()
    return render(request, "enseignants/add.html",{'form':form,"navbar":'enseignant'})
def add_enseignant(request):
    form = enseignantForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة المعلم بنجاح')
    return redirect('enseignant')
def edit_enseignant(request, id):
    enseignant = Enseignant.objects.get(id=id)
    form = enseignantForm()
    return render(request,'enseignants/edit.html',{'enseignant':enseignant,"navbar":'enseignant','form':form})
def update_enseignant(request, id):
    enseignant = Enseignant.objects.get(id=id)
    form = enseignantForm(request.POST, instance=enseignant)
    form.save()
    messages.info(request, 'تم تعديل المعلم بنجاح')
    return redirect('enseignant')
def delete_enseignant(request, id):
    enseignant = Enseignant.objects.get(id=id)
    enseignant.delete()
    messages.warning(request, 'تم إزالة المعلم بنجاح')
    return redirect('enseignant')
def import_enseignants(request):
    if request.method == 'POST':
        enseignants_resource = EnseignantResource()
        dataset = Dataset()
        new_etudiants = request.FILES['myfile']

        if not new_etudiants.name.endswith('xlsx'):
            messages.error(request, 'Le fichier doit être un fichier Excel (.xlsx)')
        else:
            imported_data = dataset.load(new_etudiants.read(), format='xlsx')
            for row in imported_data:
                # Associez les données du fichier Excel aux champs de modèle Etudiant
                enseignant = Enseignant(
                    nom=row[0],
                    prenom=row[1],
                    date_naiss=row[2],
                    sexe=row[3],
                    mobile=row[4],
                    salaire=row[5],
                )
                # Associez l'ID du parent et de la classe en utilisant les noms du parent et du libellé de la classe (comme dans les exemples précédents)
                enseignant.save()
            messages.success(request, 'تم إضافة المعلمين بنجاح')            
    all_enseignant= Enseignant.objects.all()
    return render(request,"enseignants/index.html",{"enseignants": all_enseignant,"navbar":'enseignant'})


# Affectation
def affectation(request):
    all_affectation= Enseigner.objects.all()
    return render(request,"affectations/index.html",{"affectations": all_affectation,"navbar":'affectation'})
def load_form_affectation(request):
    form = affectationForm()
    enseignants = Enseignant.objects.all()
    matieres = Matiere.objects.all()
    classes = Class.objects.all()
    return render(request, "affectations/add.html",{'form':form,"navbar":'affectation','enseignants':enseignants,'matieres':matieres,'classes':classes})
def add_affectation(request):
    form = affectationForm(request.POST)
    form.save()
    return redirect('affectation')
def edit_affectation(request, id):
    affectation = Enseigner.objects.get(id=id)
    form = affectationForm()
    enseignants = Enseignant.objects.all()
    matieres = Matiere.objects.all()
    classes = Class.objects.all()
    return render(request,'affectations/edit.html',{'affectation':affectation,"navbar":'affectation','form':form,'enseignants':enseignants,'matieres':matieres,'classes':classes})
def update_affectation(request, id):
    affectation = Enseigner.objects.get(id=id)
    form = affectationForm(request.POST, instance=affectation)
    form.save()
    return redirect('affectation')
def delete_affectation(request, id):
    affectation = Enseigner.objects.get(id=id)
    affectation.delete()
    return redirect('affectation')

# matiere
def matiere(request):
    all_matiere= Matiere.objects.all()
    return render(request,"matieres/index.html",{"matieres": all_matiere,"navbar":'matiere'})
def load_form_matiere(request):
    form = matiereForm()
    return render(request, "matieres/add.html",{'form':form,"navbar":'matiere'})
def add_matiere(request):
    form = matiereForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة المادة بنجاح')
    return redirect('matiere')
def edit_matiere(request, id):
    matiere = Matiere.objects.get(id=id)
    form = matiereForm()
    return render(request,'matieres/edit.html',{'matiere':matiere,"navbar":'matiere','form':form})
def update_matiere(request, id):
    matiere = Matiere.objects.get(id=id)
    form = matiereForm(request.POST, instance=matiere)
    form.save()
    messages.info(request, 'تم تعديل المادة بنجاح')
    return redirect('matiere')
def delete_matiere(request, id):
    matiere = Matiere.objects.get(id=id)
    matiere.delete()
    messages.warning(request, 'تم إزالة المادة بنجاح')
    return redirect('matiere')
def import_matieres(request):
    if request.method == 'POST':
        etudiant_resource = MatiereResource()
        dataset = Dataset()
        new_etudiants = request.FILES['myfile']

        if not new_etudiants.name.endswith('xlsx'):
            messages.error(request, 'Le fichier doit être un fichier Excel (.xlsx)')
        else:
            imported_data = dataset.load(new_etudiants.read(), format='xlsx')
            for row in imported_data:
                # Associez les données du fichier Excel aux champs de modèle Etudiant
                matiere = Matiere(
                    libelle=row[0],
                    coefficient=row[1],
                    note_complete=row[2],
                )
                matiere.save()

        messages.success(request, 'تم إضافة الموادة بنجاح')
    all_matiere= Matiere.objects.all()
    return render(request,"matieres/index.html",{"matieres": all_matiere,"navbar":'matieres'})


# classes
def classes(request):
    all_classes= Class.objects.all()
    return render(request,"classes/index.html",{"classes": all_classes,"navbar":'classes'})

def load_form_classes(request):
    form = classesForm()
    return render(request, "classes/add.html",{'form':form,"navbar":'classes'})

def add_classes(request):
    form = classesForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الصف بنجاح')
    return redirect('classes')

def edit_classes(request, id):
    classe = Class.objects.get(id=id)
    form = classesForm()
    return render(request,'classes/edit.html',{'classe':classe,"navbar":'classes','form':form})

def update_classes(request, id):
    classes = Class.objects.get(id=id)
    form = classesForm(request.POST, instance=classes)
    form.save()
    messages.info(request, 'تم تعديل الصف بنجاح')
    return redirect('classes')

def delete_classes(request, id):
    classes = Class.objects.get(id=id)
    classes.delete()
    messages.warning(request, 'تم إزالة الصف بنجاح')
    return redirect('classes')

def list_absance(request):
    all_classes= Class.objects.all()
    return render(request,"classes/list_absance.html",{"classes": all_classes,"navbar":'list_absance'})

def generer_list_absance(request):
    if request.method == 'POST':
            id_class = request.POST.get('id_class')
            mois = request.POST.get('mois')
            classe = Class.objects.get(id=id_class)

            etudiants = Etudiant.objects.filter(id_class=id_class)


            return render(request,"classes/generer_list_absance.html",{"classe": classe, 'mois': mois, 'etudiants': etudiants,"a":0})


# notes
def note(request):
    all_note= Note.objects.all()
    return render(request,"notes/index.html",{"notes": all_note,"navbar":'note'})
def load_form_note(request):
    etudiants = Etudiant.objects.all()
    matieres = Matiere.objects.all()
    all_examen= Evaluation.objects.all()
    form = noteForm()
    return render(request, "notes/add.html",{'form':form,"navbar":'note','etudiants':etudiants,'matieres':matieres,'examens': all_examen})
def add_note(request):
    form = noteForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الدرجة بنجاح')
    return redirect('note')
def edit_note(request, id):
    note = Note.objects.get(id=id)
    etudiants = Etudiant.objects.all()
    matieres = Matiere.objects.all()
    all_examen= Evaluation.objects.all()
    form = noteForm()
    return render(request,'notes/edit.html',{'note':note,"navbar":'note','form':form,'etudiants':etudiants,'matieres':matieres,'examens': all_examen})
def update_note(request, id):
    note = Note.objects.get(id=id)
    form = noteForm(request.POST, instance=note)
    form.save()
    messages.info(request, 'تم تعديل الدرجة بنجاح')
    return redirect('note')
def delete_note(request, id):
    note = Note.objects.get(id=id)
    note.delete()
    messages.warning(request, 'تم إزالة الدرجة بنجاح')
    return redirect('note')
def import_notes(request):
    if request.method == 'POST':
        etudiant_resource = NoteResource()
        dataset = Dataset()
        new_etudiants = request.FILES['myfile']

        if not new_etudiants.name.endswith('xlsx'):
            messages.error(request, 'Le fichier doit être un fichier Excel (.xlsx)')
        else:
            imported_data = dataset.load(new_etudiants.read(), format='xlsx')
            for row in imported_data:
                note = Note(
                    valeur=row[2],
                    type=row[4],
                )
                note.id_etud = Etudiant.objects.get(nom=row[0])
                note.id_matiere = Matiere.objects.get(libelle=row[1])
                note.id_evaluation = Evaluation.objects.get(libelle=row[3])
                note.save()
            messages.success(request, 'تم إضافة الدرجات بنجاح')

    all_note = Note.objects.all()
    return render(request, 'notes/index.html',{"notes": all_note,"navbar":'note'})

def bulletin(request):
    etudiants = Etudiant.objects.all()
    all_examen= Evaluation.objects.all()
    return render(request,"notes/bulletin.html",{'etudiants':etudiants,'examens': all_examen})

def generer_bulletin(request):
    if request.method == 'POST':
            id_etud = request.POST.get('id_etud')
            id_evaluation = request.POST.get('id_evaluation')
            etudiant = Etudiant.objects.get(id=id_etud)
            evaluation = Evaluation.objects.get(id=id_evaluation)
            notes = Note.objects.filter(id_etud=id_etud,id_evaluation=id_evaluation)

            return render(request,"notes/generer_bulletin.html",{"etudiant": etudiant, 'evaluation': evaluation ,"notes":notes})


def bulletin_class(request):
    # Retrieve the list of classes
    all_examen= Evaluation.objects.all()
    classes = Class.objects.all()
    return render(request, "notes/bulletin_class.html", {'classes': classes,'examens': all_examen})


def generer_bulletin_class(request):
    if request.method == 'POST':
        # Get the selected class and evaluation ID from the form
        selected_class = request.POST.get('id_class')
        selected_evaluation_id = request.POST.get('id_evaluation')

        # Get the selected evaluation object
        selected_evaluation = Evaluation.objects.get(pk=selected_evaluation_id)

        # Get all students in the selected class
        students = Etudiant.objects.filter(id_class=selected_class)

        # Create a list to store bulletin data for each student
        bulletins = []

        for student in students:
            # Retrieve the notes for the student and selected evaluation
            notes_ar = Note.objects.filter(id_etud=student, id_evaluation=selected_evaluation,type="ar")
            notes_fr = Note.objects.filter(id_etud=student, id_evaluation=selected_evaluation,type="fr")

            # Append the student's bulletin data to the list
            bulletin_data = {
                'etudiant': student,
                'evaluation': selected_evaluation,  # Pass the selected evaluation to the template
                'notes_ar': notes_ar,
                'notes_fr': notes_fr,
            }
            bulletins.append(bulletin_data)

        return render(request, "notes/generer_bulletin_class.html", {'bulletins': bulletins})


# examen
def examen(request):
    all_examen= Evaluation.objects.all()
    return render(request,"examens/index.html",{"examens": all_examen,"navbar":'examen'})
def load_form_examen(request):
    form = evaluationForm()
    return render(request, "examens/add.html",{'form':form,"navbar":'examen'})
def add_examen(request):
    form = evaluationForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الإمتحان بنجاح')
    return redirect('examen')
def edit_examen(request, id):
    examen = Evaluation.objects.get(id=id)
    form = evaluationForm()
    return render(request,'examens/edit.html',{'examen':examen,"navbar":'examen','form':form})
def update_examen(request, id):
    examen = Evaluation.objects.get(id=id)
    form = evaluationForm(request.POST, instance=examen)
    form.save()
    messages.info(request, 'تم تعديل الإمتحان بنجاح')
    return redirect('examen')
def delete_examen(request, id):
    examen = Evaluation.objects.get(id=id)
    examen.delete()
    messages.warning(request, 'تم إزالة الإمتحان بنجاح')
    return redirect('examen')

# timetable
def timetable(request):
    all_timetable= Timetable.objects.all()
    return render(request,"timetables/index.html",{"timetables": all_timetable,"navbar":'timetable'})

def load_form_timetable(request):
    form = timetableForm()
    enseignants = Enseignant.objects.all()
    matieres = Matiere.objects.all()
    classes = Class.objects.all()
    return render(request, "timetables/add.html",{'form':form,"navbar":'timetable','enseignants':enseignants,'matieres':matieres,'classes':classes})
def add_timetable(request):
    form = timetableForm(request.POST)
    form.save()
    return redirect('timetable')
def edit_timetable(request, id):
    timetable = Timetable.objects.get(id=id)
    form = timetableForm()
    enseignants = Enseignant.objects.all()
    matieres = Matiere.objects.all()
    classes = Class.objects.all()
    return render(request,'timetables/edit.html',{'timetable':timetable,"navbar":'timetable','form':form,'enseignants':enseignants,'matieres':matieres,'classes':classes})
def update_timetable(request, id):
    timetable = Timetable.objects.get(id=id)
    form = timetableForm(request.POST, instance=timetable)
    form.save()
    return redirect('timetable')
def delete_timetable(request, id):
    timetable = Timetable.objects.get(id=id)
    timetable.delete()
    return redirect('timetable')

def timetable_list(request):
    all_classes= Class.objects.all()
    all_enseignants = Enseignant.objects.all()
    return render(request,"timetables/timetable.html",{"classes": all_classes,'enseignants':all_enseignants, "navbar":'list_absance'})

def generer_timetable(request):
    if request.method == 'POST':
        id_class = request.POST.get('id_class')
        id_ens = request.POST.get('id_ens')

        # timetable = Timetable.objects.get(id_class=id_class)
        timetable = Timetable.objects.get(id_ens=id_ens)


        return render(request,"timetables/genere_timetable.html",{"timetable":timetable})


# Accounts

# pointages
def load_form_pointage(request):
    form = salaireForm()
    enseignants = Enseignant.objects.all()
    return render(request, "accounts/pointage.html",{'form':form,"navbar":'accounts','enseignants':enseignants})
def add_pointage(request):
    form = salaireForm(request.POST)
    form.save()
    return redirect('enseignant')
# salaires
def salaire(request):
    all_enseignant= Enseignant.objects.all()
    return render(request,"accounts/salaires.html",{"enseignants": all_enseignant,"navbar":'accounts'})
def load_form_salaire(request):
    form = salaireForm()
    enseignants = Enseignant.objects.all()
    return render(request, "accounts/add_salaire.html",{'form':form,"navbar":'accounts','enseignants':enseignants})
def add_salaire(request):
    form = salaireForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الدفع بنجاح')
    return redirect('salaire')


# Partenaires
def partenaire(request):
    all_partenaire= Partenaire.objects.all()
    return render(request,"accounts/list_partenaire.html",{"partenaires": all_partenaire,"navbar":'partenaire'})

def load_form_partenaire(request):
    form = partenaireForm()
    return render(request, "accounts/add_partenaire.html",{'form':form,"navbar":'partenaire'})
def add_partenaire(request):
    form = partenaireForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة مقترض بنجاح')
    return redirect('partenaire')
def edit_partenaire(request, id):
    partenaire = Partenaire.objects.get(id=id)
    form = partenaireForm()
    return render(request,'accounts/edit_partenaire.html',{'partenaire':partenaire,"navbar":'partenaire','form':form})
def update_partenaire(request, id):
    partenaire = Partenaire.objects.get(id=id)
    form = partenaireForm(request.POST, instance=partenaire)
    form.save()
    messages.info(request, 'تم تعديل مقترض بنجاح')
    return redirect('partenaire')
def delete_partenaire(request, id):
    partenaire = Partenaire.objects.get(id=id)
    partenaire.delete()
    messages.warning(request, 'تم إزالة مقترض بنجاح')
    return redirect('partenaire')

# prets
def load_form_pret(request):
    form = pretForm()
    all_partenaire= Partenaire.objects.all()
    return render(request, "accounts/add_pret.html",{'form':form,"navbar":'accounts','partenaires':all_partenaire})
def add_pret(request):
    form = pretForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الأقتراض بنجاح')
    return redirect('partenaire')

# pays
def load_form_pay(request):
    form = pretForm()
    all_partenaire= Partenaire.objects.all()
    return render(request, "accounts/add_pay.html",{'form':form,"navbar":'accounts','partenaires':all_partenaire})
def add_pay(request):
    form = pretForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة المبلغ المدفوع  بنجاح')
    return redirect('partenaire')

# depenses
def depense(request):
    all_depense= Depense.objects.all()
    return render(request,"depenses/index.html",{"depenses": all_depense,"navbar":'depense'})

def load_form_depense(request):
    form = depenseForm()
    return render(request, "depenses/add.html",{'form':form,"navbar":'depense'})
def add_depense(request):
    form = depenseForm(request.POST)
    form.save()
    return redirect('depense')
def edit_depense(request, id):
    depense = Depense.objects.get(id=id)
    form = depenseForm()
    return render(request,'depenses/edit.html',{'depense':depense,"navbar":'depense','form':form})
def update_depense(request, id):
    depense = Depense.objects.get(id=id)
    form = depenseForm(request.POST, instance=depense)
    form.save()
    return redirect('depense')
def delete_depense(request, id):
    depense = Depense.objects.get(id=id)
    depense.delete()
    return redirect('depense')


# parents accounts
def parentaccounts(request):
    all_parent= Parent.objects.all()
    return render(request,"parentaccounts/index.html",{"parents": all_parent,"navbar":'parentaccounts'})

# payment
def load_form_payment(request):
    form = paymentForm()
    all_parent= Parent.objects.all()
    all_mois= Mois.objects.all()
    return render(request, "parentaccounts/add_payment.html",{'form':form,"navbar":'accounts',"parents": all_parent,"mois": all_mois})

def add_payment(request):
    if request.method == 'POST':
        id_parent = request.POST.get('id_parent')
        mois_paye = request.POST.get('mois_paye')
        montant_paye = request.POST.get('montant_paye')
        date_payment = request.POST.get('date_payment')

        # Get the existing payment entry for the selected parent and month, if it exists
        payment_entry = get_object_or_404(ParentmoisPayment, id_parent=id_parent, mois_paye=mois_paye)

        # Update the attributes and set pay=True
        payment_entry.montant_paye = montant_paye
        payment_entry.date_payment = date_payment
        payment_entry.pay = True  # Set pay to True
        payment_entry.save()
        messages.success(request, 'تم إضافة المبلغ المدفوع  بنجاح')
        # Redirect to a success page or display a success message
        return redirect('parentaccounts')

# mois

def load_form_mois(request):
    form = moisForm()
    return render(request, "parentaccounts/add_mois.html",{'form':form,"navbar":'accounts'})
def add_mois(request):
    form = moisForm(request.POST)
    form.save()
    messages.success(request, 'تم إضافة الشهر  بنجاح')
    return redirect('parentaccounts')

# ishaar
def ishaar(request):
    all_parent= Parent.objects.all()
    return render(request,"parentaccounts/ishaar.html",{"parents": all_parent})


def generer_ishaar(request):
    selected_parent_ids = []
    if request.method == 'POST':
        # Process the form data to get selected parent IDs
        selected_parent_ids.append(request.POST.get('id_parent1'))
        selected_parent_ids.append(request.POST.get('id_parent2'))
        selected_parent_ids.append(request.POST.get('id_parent3'))
        selected_parent_ids.append(request.POST.get('id_parent4'))

        # Fetch the parent and student data based on selected parent IDs
        selected_parents = Parent.objects.filter(id__in=selected_parent_ids)
        students_for_selected_parents = {}
        months_for_selected_parents = {}

        for parent in selected_parents:
            students_for_selected_parents[parent] = Etudiant.objects.filter(id_parent=parent)
            # Fetch the months related to this parent with pay=False
            months_for_selected_parents[parent] = Mois.objects.filter(
                parentmoispayment__id_parent=parent,
                parentmoispayment__pay=False
            )

        # Prepare the data to be passed to the template
        context = {
            'selected_parents': selected_parents,
            'students_for_selected_parents': students_for_selected_parents,
            'months_for_selected_parents': months_for_selected_parents,
        }

        # Render the second page template with the data
        return render(request, 'parentaccounts/generer_ishaar.html', context)
    else:
        # Handle GET request or display the form again
        return render(request, 'parentaccounts/ishaar.html')


# history

def parent_history(request, id):
    parentPayment = ParentmoisPayment.objects.filter(id_parent=id)
    return render(request,'parentaccounts/history.html',{"parentpayment":parentPayment})

def enseignant_history(request, id):
    salaire = Salaire.objects.filter(id_ens=id)
    return render(request,'accounts/enseignant_history.html',{"salaire":salaire})
