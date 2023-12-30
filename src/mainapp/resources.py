# myapp/resources.py
from import_export import resources
from .models import Etudiant , Parent ,Enseignant ,Matiere ,Inscription ,Note

class EtudiantResource(resources.ModelResource):
    class Meta:
        model = Etudiant
        skip_unchanged = True
        report_skipped = False

class ParentResource(resources.ModelResource):
    class Meta:
        model = Parent
        skip_unchanged = True
        report_skipped = False

class EnseignantResource(resources.ModelResource):
    class Meta:
        model = Enseignant
        skip_unchanged = True
        report_skipped = False

class MatiereResource(resources.ModelResource):
    class Meta:
        model = Matiere
        skip_unchanged = True
        report_skipped = False

class InscriptionResource(resources.ModelResource):
    class Meta:
        model = Inscription
        skip_unchanged = True
        report_skipped = False

class NoteResource(resources.ModelResource):
    class Meta:
        model = Note
        skip_unchanged = True
        report_skipped = False