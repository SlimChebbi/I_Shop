from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from lignes.forms import *
from lignes.models import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from feeds.models import *
from reports.models import *


@login_required()
def vendreligne(request, id):
    ligne = get_object_or_404(Vendre, pk=id)
    return render(request, 'lignes/vendre_ligne.html',
                  {'ligne': ligne})


@login_required()
def ligne(request, id):
    ligne = get_object_or_404(Ligne, pk=id)
    return render(request, 'lignes/ligne.html',
                  {'ligne': ligne})


@login_required()
def ooredoo(request):
    ooredoo = Ligne.objects.filter(type="Ooredoo")
    return render(request, 'lignes/ooredoo.html',
                  {'ooredoo': ooredoo})


@login_required()
def telecom(request):
    telecom = Ligne.objects.filter(type="Telecom")
    return render(request, 'lignes/telecom.html',
                  {'telecom': telecom})


@login_required()
def orange(request):
    orange = Ligne.objects.filter(type="Orange")
    return render(request, 'lignes/orange.html',
                  {'orange': orange})


@login_required()
def edite_ligne(request, id, type):
    ligne = get_object_or_404(Ligne, pk=id)
    if request.POST:
        form = LigneForm(request.POST, instance=ligne)
        if form.is_valid():
            form.save()
            if type == '1':
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Ligne/Ooredoo <a href="/lignes/ligne/{2}/" >{1}</a> .'.format(
                    request.user.username,  ligne.forfait, ligne.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('ooredoo'))
            elif type == '2':
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Ligne/Orange <a href="/lignes/ligne/{2}/" >{1}</a> .'.format(
                    request.user.username,  ligne.forfait, ligne.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('orange'))
            else:
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Ligne/Telecom <a href="/lignes/ligne/{2}/" >{1}</a> .'.format(
                    request.user.username,  ligne.forfait, ligne.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('telecom'))

    else:
        form = LigneForm(instance=ligne)
    return render(request, 'lignes/edit_ligne.html', {'form': form,
                                                      'type': type})


@login_required()
def delete_ligne(request, id, type):
    if id:
        ligne = get_object_or_404(Ligne, pk=id)
        ligne.delete()
    if type == '1':
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime  Ligne/Ooredoo  {1} .'.format(
            request.user.username,  ligne.forfait)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return HttpResponseRedirect(reverse('ooredoo'))
    elif type == '2':
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime  Ligne/Orange {1} .'.format(
            request.user.username,  ligne.forfait)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return HttpResponseRedirect(reverse('orange'))
    else:
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime  Ligne/Telecom  {1}  .'.format(
            request.user.username,  ligne.forfait)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return HttpResponseRedirect(reverse('telecom'))


@login_required()
def add_ligne(request, id):
    if request.method == 'POST':
        form = LigneForm(request.POST)
        if form.is_valid():
            pk = form.save()
            if id == '1':
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Ligne/Ooredoo <a href="/lignes/ligne/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('forfait'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('ooredoo'))
            elif id == '2':
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Ligne/Orange <a href="/lignes/ligne/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('forfait'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('orange'))
            else:
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Ligne/Telecom <a href="/lignes/ligne/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('forfait'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('telecom'))

        return render(request, 'lignes/add_ligne.html',
                      {'form': form, 'id': id})
    else:
        form = LigneForm()
        return render(request, 'lignes/add_ligne.html',
                      {'form': form, 'id': id})


@login_required()
def vendre_ligne(request, id, type):
    ligne = get_object_or_404(Ligne, pk=id)
    if request.method == 'POST':
        form = VendreForm(request.POST)
        if form.is_valid():
            prix_de_vendre = form.cleaned_data.get('prix_de_vendre')
            quantite = form.cleaned_data.get('quantite')
            note = form.cleaned_data.get('note')
            v = Vendre(item=ligne.forfait, type=ligne.type,
                       prix_de_gros=ligne.prix_de_gros,
                       prix_de_vendre=prix_de_vendre, quantite=quantite,
                       note=note, user=request.user.username,
                       ligne=ligne)
            v.save()
            ligne.quantite = ligne.quantite - quantite
            ligne.save()

            if type == '1':
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre  Ligne/Ooredoo <a href="/lignes/vendreligne/{2}/" >{1}</a>  .'.format(
                    request.user.username, ligne.forfait, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('ooredoo'))
            elif type == '2':
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre  Ligne/Orange <a href="/lignes/vendreligne/{2}/" >{1}</a>  .'.format(
                    request.user.username, ligne.forfait, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('orange'))
            else:
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre  Ligne/Telecom <a href="/lignes/vendreligne/{2}/" >{1}</a>  .'.format(
                    request.user.username, ligne.forfait, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('telecom'))

        return render(request, 'lignes/vendre.html',
                      {'form': form, 'ligne': ligne, 'id': id})

    else:
        form = VendreForm()
        return render(request, 'lignes/vendre.html',
                      {'form': form, 'ligne': ligne, 'id': id})
