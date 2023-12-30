from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed
from django.dispatch import receiver
from django.db.models import Sum
from datetime import datetime ,timezone


class Class(models.Model):
    libelle = models.CharField(max_length=50)

class Employee(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    nom_ar = models.CharField(max_length=50)
    prenom_ar = models.CharField(max_length=50)
    date_naiss = models.DateField(null=True)
    sexe = models.CharField(max_length=10)
    mobile = models.CharField(max_length=12)
    grade = models.CharField(max_length=12)
    salaire = models.IntegerField()

class Enseignant(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    date_naiss = models.DateField(null=True)
    sexe = models.CharField(max_length=10)
    mobile = models.CharField(max_length=12)
    montant_total = models.IntegerField(blank=True, null=True,default=0)

class Salaire(models.Model):
    id_ens = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    pointage = models.IntegerField(blank=True, null=True)
    salaire = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

@receiver(post_save, sender=Salaire)
def update_montant_total(sender, instance, **kwargs):
    enseignant = instance.id_ens
    pointages = enseignant.salaire_set.aggregate(total_pointages=models.Sum('pointage'))['total_pointages'] or 0
    salaires = enseignant.salaire_set.aggregate(total_salaires=models.Sum('salaire'))['total_salaires'] or 0
    enseignant.montant_total = pointages - salaires
    enseignant.save()


class Enseigner(models.Model):
    id_matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    id_ens = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    id_class = models.ForeignKey(Class, on_delete=models.CASCADE)



class Mois(models.Model):
    nom = models.CharField(max_length=20)
    annee = models.IntegerField()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Lorsqu'un mois est créé, affectez-le à tous les parents
        parents = Parent.objects.all()
        for parent in parents:
            ParentmoisPayment.objects.create(id_parent=parent, mois_paye=self)



class Parent(models.Model):
    nom = models.CharField(max_length=50, blank=True, null=True)
    prenom = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    mobile2 = models.CharField(max_length=12, null=True, blank=True)
    date_inscription = models.DateField(null=True, blank=True)
    frais_mensuels = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0, blank=True)

    def update_frais_mensuels(self):
        # Calculez la somme des frais mensuels des étudiants associés à ce parent
        total_frais_mensuels = self.etudiant_set.aggregate(Sum('frais_mensuels'))['frais_mensuels__sum']
        self.frais_mensuels = total_frais_mensuels or 0

    def get_montant_restant(self):
        # Calculez le montant restant du parent en fonction des mois impayés
        mois_impayes = ParentmoisPayment.objects.filter(id_parent=self.id, pay=False)
        montant_restant = self.frais_mensuels * mois_impayes.count()
        return montant_restant

class ParentmoisPayment(models.Model):
    id_parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    mois_paye = models.ForeignKey(Mois, on_delete=models.CASCADE, null=True)
    date_payment = models.DateField(blank=True, null=True)
    montant_paye = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    pay = models.BooleanField(default=False)

class Etudiant(models.Model):
    nom = models.CharField(max_length=50, null=True, blank=True)
    prenom = models.CharField(max_length=50, null=True, blank=True)
    nom_fr = models.CharField(max_length=50, null=True, blank=True)
    prenom_fr = models.CharField(max_length=50, null=True, blank=True)
    date_naiss = models.DateField(null=True, blank=True)
    sexe = models.CharField(max_length=50, null=True, blank=True)
    NNI = models.BigIntegerField(null=True, blank=True)
    RIM = models.CharField(max_length=20, null=True, blank=True)
    id_parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    date_inscription = models.DateField(null=True, blank=True)
    id_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    numero_absence = models.IntegerField(default=0, blank=True)
    frais_mensuels = models.IntegerField(null=True,default=0, blank=True)


@receiver(pre_save, sender=Etudiant)
def generer_numero_absence(sender, instance, **kwargs):
    # Vérifiez si l'étudiant n'a pas déjà un numéro d'absence attribué
    if instance.numero_absence == 0:
        # Récupérez la classe de l'étudiant
        classe_etudiant = instance.id_class
        if classe_etudiant:
            # Comptez le nombre d'étudiants dans la même classe
            nombre_etudiants = Etudiant.objects.filter(id_class=classe_etudiant).count()
            # Ajoutez 1 au nombre d'étudiants pour obtenir le numéro d'absence
            instance.numero_absence = nombre_etudiants + 1



class Inscription(models.Model):
    id_etud = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    id_matiere = models.ForeignKey('Matiere', on_delete=models.CASCADE)
    annee = models.CharField(max_length=50,null=True)

class Matiere(models.Model):
    libelle = models.CharField(max_length=50)
    coefficient = models.CharField(max_length=50)
    note_complete = models.CharField(max_length=50,blank=True)

class Partenaire(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    montant_total = models.IntegerField(blank=True, null=True,default=0)

class Pret(models.Model):
    id_partenaire = models.ForeignKey(Partenaire, on_delete=models.CASCADE)
    pret = models.IntegerField(blank=True, null=True)
    pay = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

@receiver(post_save, sender=Pret)
def update_montant_total(sender, instance, **kwargs):
    Partenaire = instance.id_partenaire
    pret = Partenaire.pret_set.aggregate(total_pret=models.Sum('pret'))['total_pret'] or 0
    pay = Partenaire.pret_set.aggregate(total_pay=models.Sum('pay'))['total_pay'] or 0
    Partenaire.montant_total = pret - pay
    Partenaire.save()

class Proprietaire(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    pourcentage = models.IntegerField()

class Evaluation(models.Model):
    libelle = models.CharField(max_length=50)
    coefficient = models.IntegerField(blank=True,null=True)
    date = models.DateField(blank=True,null=True)

class Note(models.Model):
    valeur = models.FloatField()
    id_etud = models.ForeignKey(Etudiant, on_delete=models.CASCADE)
    id_matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    id_evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE)
    type = models.CharField(max_length=50,blank=True)

class Timetable(models.Model):
    id_ens = models.ForeignKey(Enseignant, on_delete=models.CASCADE)
    id_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    id_matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    start_time = models.TimeField(blank=True,null=True)
    end_time = models.TimeField(blank=True,null=True)
    day = models.CharField(max_length=50)

class Depense(models.Model):
    libelle = models.CharField(max_length=50)
    montant_total = models.IntegerField(blank=True, null=True,default=0)
    date = models.DateField(blank=True, null=True)

class Etudiant_evaluaion(models.Model):
    id_etud = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    id_evaluation = models.ForeignKey('Evaluation', on_delete=models.CASCADE)
    total = models.IntegerField(blank=True, null=True, default=0)
    range = models.IntegerField(blank=True,null=True, default=0)

    def save(self, *args, **kwargs):
        # Calculer le score total de l'étudiant dans cette évaluation
        total_score = Note.objects.filter(id_etud=self.id_etud, id_evaluation=self.id_evaluation).aggregate(total=models.Sum('valeur'))['total'] or 0
        self.total = total_score

        # Calculer le classement de l'étudiant dans sa classe pour cette évaluation
        etudiants_dans_evaluation = Etudiant_evaluaion.objects.filter(id_evaluation=self.id_evaluation).order_by('-total')
        rang = 1
        for etudiant in etudiants_dans_evaluation:
            if etudiant.id_etud == self.id_etud:
                self.range = rang
                break
            rang += 1

        super().save(*args, **kwargs)


@receiver(post_save, sender=Evaluation)
def create_etudiant_evaluations(sender, instance, created, **kwargs):
    if created:
        # Lorsqu'une nouvelle évaluation est créée, affectez-la à tous les étudiants
        etudiants = Etudiant.objects.all()
        for etudiant in etudiants:
            Etudiant_evaluaion.objects.create(id_etud=etudiant, id_evaluation=instance)

