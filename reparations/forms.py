from django import forms
from reparations.models import *
from django.shortcuts import get_object_or_404

class ReparationForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        max_length=2500, required=False)

    def __init__(self, *args, **kwargs):
        super(ReparationForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'class': 'form-control'})
        self.fields['client'].widget.attrs.update({'class': 'form-control'})
        self.fields['telephone_client'].widget.attrs.update(
            {'class': 'form-control'})

    class Meta:
        model = Reparation
        fields = ['item', 'client', 'telephone_client', 'description']


class FactureForm(forms.Form):
    item = forms.CharField(max_length=255)
    prix_de_gros = forms.DecimalField()
    prix = forms.DecimalField()
    quantite = forms.IntegerField()
    description = forms.CharField(
        widget=forms.Textarea(), max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        self.fields['item'].widget.attrs.update({'class': 'form-control'})
        self.fields['prix_de_gros'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['prix'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['quantite'].widget.attrs.update(
            {'class': 'form-control'})

    def save(self, *args, **kwargs):
        piece_id = kwargs.pop('piece_id')
        piece = get_object_or_404(Piece, id=piece_id)
        piece.item = self.cleaned_data['item']
        piece.prix_de_gros = self.cleaned_data['prix_de_gros']
        piece.prix = self.cleaned_data['prix']
        piece.quantite = self.cleaned_data['quantite']
        piece.description = self.cleaned_data['description']
        piece.save()


class MainOuevreForm(forms.Form):
    prix = forms.DecimalField()
    description = forms.CharField(
        widget=forms.Textarea(), max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(MainOuevreForm, self).__init__(*args, **kwargs)
        self.fields['prix'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update(
            {'class': 'form-control'})

    def save(self, *args, **kwargs):
        main_id = kwargs.pop('main_id')
        main = get_object_or_404(MainOuevre, id=main_id)
        main.prix = self.cleaned_data['prix']
        main.description = self.cleaned_data['description']
        main.save()
