from django import forms
from portables.models import *


class PortableForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}), required=False, max_length=2500)

    def __init__(self, *args, **kwargs):
        super(PortableForm, self).__init__(*args, **kwargs)
        self.fields['marque'].widget.attrs.update({'class': 'form-control'})
        self.fields['model'].widget.attrs.update({'class': 'form-control'})
        self.fields['type'].widget.attrs.update({'class': 'form-control'})
        self.fields['prix_de_gros'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['prix'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['quantite'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].label = 'Select a image'
        self.fields['prix'].label = 'Prix de vendre'

    class Meta:
        model = Portable


class VendreForm(forms.Form):
    prix_de_vendre = forms.DecimalField(label='Prix de vendre (Unite)')
    quantite = forms.IntegerField()
    note = forms.CharField(max_length=255, required=False)

    def __init__(self, *args, **kwargs):
        super(VendreForm, self).__init__(*args, **kwargs)
        self.fields['prix_de_vendre'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['note'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['quantite'].widget.attrs.update(
            {'class': 'form-control'})
