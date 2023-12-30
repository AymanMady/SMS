"""
URL configuration for SMS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    # path('etudiant/', views.etudiants, name="etudiant"),

    # etudiants
    path('etudiant/', views.etudiant, name="etudiant"),
    path('add_etudiant/', views.load_form_etudiant, name="add_etudiant"),
    path('get_add_etudiant/', views.add_etudiant),
    path('edit_etudiant/<int:id>', views.edit_etudiant, name="edit_etudiant"),
    path('update_etudiant/<int:id>', views.update_etudiant, name="update_etudiant"),
    path('delete_etudiant/<int:id>', views.delete_etudiant, name="delete_etudiant"),
    path('show_etudiant/<int:id>', views.show_etudiant, name="show_etudiant"),
    path('import-etudiants/', views.import_etudiants, name='import-etudiants'),

    # parents
    path('parent/', views.parent, name="parent"),
    path('add_parent/', views.load_form_parent, name="add_parent"),
    path('get_add_parent/', views.add_parent),
    path('edit_parent/<int:id>', views.edit_parent, name="edit_parent"),
    path('update_parent/<int:id>', views.update_parent, name="update_parent"),
    path('delete_parent/<int:id>', views.delete_parent, name="delete_parent"),
    path('import-parents/', views.import_parents, name='import-parents'),

    # inscriptions
    path('inscription/', views.inscription, name="inscription"),
    path('add_inscription/', views.load_form_inscription, name="add_inscription"),
    path('get_add_inscription/', views.add_inscription),
    path('edit_inscription/<int:id>', views.edit_inscription, name="edit_inscription"),
    path('update_inscription/<int:id>', views.update_inscription, name="update_inscription"),
    path('delete_inscription/<int:id>', views.delete_inscription, name="delete_inscription"),
    path('import-inscriptions/', views.import_inscriptions, name='import-inscriptions'),

    # enseiganats
    path('enseignant/', views.enseignant, name="enseignant"),
    path('add_enseignant/', views.load_form_enseignant, name="add_enseignant"),
    path('get_add_enseignant/', views.add_enseignant),
    path('edit_enseignant/<int:id>', views.edit_enseignant, name="edit_enseignant"),
    path('update_enseignant/<int:id>', views.update_enseignant, name="update_enseignant"),
    path('delete_enseignant/<int:id>', views.delete_enseignant, name="delete_enseignant"),
    path('import_enseignants/', views.import_enseignants, name='import_enseignants'),

    # affectationes
    path('affectation/', views.affectation, name="affectation"),
    path('add_affectation/', views.load_form_affectation, name="add_affectation"),
    path('get_add_affectation/', views.add_affectation),
    path('edit_affectation/<int:id>', views.edit_affectation, name="edit_affectation"),
    path('update_affectation/<int:id>', views.update_affectation, name="update_affectation"),
    path('delete_affectation/<int:id>', views.delete_affectation, name="delete_affectation"),


    # matieres
    path('matiere/', views.matiere, name="matiere"),
    path('add_matiere/', views.load_form_matiere, name="add_matiere"),
    path('get_add_matiere/', views.add_matiere),
    path('edit_matiere/<int:id>', views.edit_matiere, name="edit_matiere"),
    path('update_matiere/<int:id>', views.update_matiere, name="update_matiere"),
    path('delete_matiere/<int:id>', views.delete_matiere, name="delete_matiere"),
    path('import-matieres/', views.import_matieres, name='import-matieres'),

    # classes
    path('classes/', views.classes, name="classes"),
    path('add_classes/', views.load_form_classes, name="add_classes"),
    path('get_add_classes/', views.add_classes),
    path('edit_classes/<int:id>', views.edit_classes, name="edit_classes"),
    path('update_classes/<int:id>', views.update_classes, name="update_classes"),
    path('delete_classes/<int:id>', views.delete_classes, name="delete_classes"),
    path('list_absance/', views.list_absance, name="list_absance"),
    path('generer_list_absance/', views.generer_list_absance, name="generer_list_absance"),

    # notes
    path('note/', views.note, name="note"),
    path('add_note/', views.load_form_note, name="add_note"),
    path('get_add_note/', views.add_note),
    path('edit_note/<int:id>', views.edit_note, name="edit_note"),
    path('update_note/<int:id>', views.update_note, name="update_note"),
    path('delete_note/<int:id>', views.delete_note, name="delete_note"),
    path('import-notes/', views.import_notes, name='import-notes'),
    path('bulletin/', views.bulletin, name="bulletin"),
    path('generer_bulletin/', views.generer_bulletin, name="generer_bulletin"),
    path('bulletin_class/', views.bulletin_class, name="bulletin_class"),
    path('generer_bulletin_class/', views.generer_bulletin_class, name="generer_bulletin_class"),

    # examens
    path('examen/', views.examen, name="examen"),
    path('add_examen/', views.load_form_examen, name="add_examen"),
    path('get_add_examen/', views.add_examen),
    path('edit_examen/<int:id>', views.edit_examen, name="edit_examen"),
    path('update_examen/<int:id>', views.update_examen, name="update_examen"),
    path('delete_examen/<int:id>', views.delete_examen, name="delete_examen"),

    # timetables
    path('timetable/', views.timetable, name="timetable"),
    path('add_timetable/', views.load_form_timetable, name="add_timetable"),
    path('get_add_timetable/', views.add_timetable),
    path('edit_timetable/<int:id>', views.edit_timetable, name="edit_timetable"),
    path('update_timetable/<int:id>', views.update_timetable, name="update_timetable"),
    path('delete_timetable/<int:id>', views.delete_timetable, name="delete_timetable"),
    path('timetable_list/', views.timetable_list, name="timetable_list"),
    path('generer_timetable/', views.generer_timetable, name="generer_timetable"),

    # accounts
    # pointages
    path('add_pointage/', views.load_form_pointage, name="add_pointage"),
    path('get_add_pointage/', views.add_pointage),
    # salaires
    path('salaire/', views.salaire, name="salaire"),
    path('add_salaire/', views.load_form_salaire, name="add_salaire"),
    path('get_add_salaire/', views.add_salaire),
    # history
    path('enseignant_history/<int:id>', views.enseignant_history, name="enseignant_history"),

    # partenaires
    path('partenaire/', views.partenaire, name="partenaire"),
    path('add_partenaire/', views.load_form_partenaire, name="add_partenaire"),
    path('get_add_partenaire/', views.add_partenaire),
    path('edit_partenaire/<int:id>', views.edit_partenaire, name="edit_partenaire"),
    path('update_partenaire/<int:id>', views.update_partenaire, name="update_partenaire"),
    path('delete_partenaire/<int:id>', views.delete_partenaire, name="delete_partenaire"),
    # pret
    path('add_pret/', views.load_form_pret, name="add_pret"),
    path('get_add_pret/', views.add_pret),
    # pay
    path('add_pay/', views.load_form_pay, name="add_pay"),
    path('get_add_pay/', views.add_pay),


    # depenses
    path('depense/', views.depense, name="depense"),
    path('add_depense/', views.load_form_depense, name="add_depense"),
    path('get_add_depense/', views.add_depense),
    path('edit_depense/<int:id>', views.edit_depense, name="edit_depense"),
    path('update_depense/<int:id>', views.update_depense, name="update_depense"),
    path('delete_depense/<int:id>', views.delete_depense, name="delete_depense"),

    # parentaccounts
    path('parentaccounts/', views.parentaccounts, name="parentaccounts"),
    # payment
    path('add_payment/', views.load_form_payment, name="add_payment"),
    path('get_add_payment/', views.add_payment),
    # mois
    path('add_mois/', views.load_form_mois, name="add_mois"),
    path('get_add_mois/', views.add_mois),
    # ishaar
    path('ishaar/', views.ishaar, name="ishaar"),
    path('generer_ishaar/', views.generer_ishaar, name="generer_ishaar"),
    # history
    path('parent_history/<int:id>', views.parent_history, name="parent_history"),

]
