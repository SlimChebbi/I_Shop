from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from accessoires.forms import *
from accessoires.models import *
from reports.models import *
from feeds.models import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required()
def accessoire(request, id):
    access = get_object_or_404(Accessoire, pk=id)
    return render(request, 'accessoires/accessoire.html',
                  {'access': access})


@login_required()
def vendre(request, id):
    vendre = get_object_or_404(Vendre, pk=id)
    return render(request, 'accessoires/vendre_acess.html',
                  {'vendre': vendre})


@login_required()
def informatique(request):
    accessoires_inf = Accessoire.objects.filter(type="Informatique")
    return render(request, 'accessoires/informatique.html',
                  {'accessoires_inf': accessoires_inf})


@login_required()
def portable(request):
    accessoires_por = Accessoire.objects.filter(type="Portable")
    return render(request, 'accessoires/portable.html',
                  {'accessoires_por': accessoires_por})


@login_required()
def edite_accessoire(request, id, type):
    acess = get_object_or_404(Accessoire, pk=id)
    if request.POST:
        form = AccessoireForm(request.POST, request.FILES, instance=acess)
        if form.is_valid():
            form.save()
            if type == '1':
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Acessoire/informatique <a href="/accessoires/accessoire/{2}/" >{1}</a> .'.format(
                    request.user.username, acess.produit, acess.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return redirect('informatique')
            else:
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Acessoire/Telephone <a href="/accessoires/accessoire/{2}/" >{1}</a> .'.format(
                    request.user.username, acess.produit, acess.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return redirect('portable')

    else:
        form = AccessoireForm(instance=acess)
    return render(request, 'accessoires/edit_accessoires.html', {'form': form,
                                                                 'type': type})


@login_required()
def delete_accessoire(request, id, type):
    if id:
        acess = get_object_or_404(Accessoire, pk=id)
        acess.delete()
    if type == '1':
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime Acessoire/informatique {1} .'.format(
            request.user.username, acess.produit)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return HttpResponseRedirect(reverse('informatique'))
    else:
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime Acessoire/Telephone {1} .'.format(
            request.user.username, acess.produit)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return HttpResponseRedirect(reverse('portable'))


@login_required()
def add_accessoire(request, id):
    if request.method == 'POST':
        form = AccessoireForm(request.POST, request.FILES)
        if form.is_valid():
            pk = form.save()

            if id == '1':
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Acessoire/Iformatique <a href="/accessoires/accessoire/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('produit'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('informatique'))
            else:
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Acessoire/Telephone <a href="/accessoires/accessoire/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('produit'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('portable'))

        return render(request, 'accessoires/add_accessoire.html',
                      {'form': form, 'id': id})
    else:
        form = AccessoireForm()
        return render(request, 'accessoires/add_accessoire.html',
                      {'form': form, 'id': id})


@login_required()
def vendre_accessoire(request, id, type):
    acess = get_object_or_404(Accessoire, pk=id)
    if request.method == 'POST':
        form = VendreForm(request.POST)
        if form.is_valid():
            prix_de_vendre = form.cleaned_data.get('prix_de_vendre')
            quantite = form.cleaned_data.get('quantite')
            note = form.cleaned_data.get('note')
            username = request.user.username
            v = Vendre(item=acess.produit, type=acess.type,
                       prix_de_gros=acess.prix_de_gros,
                       prix_de_vendre=prix_de_vendre, quantite=quantite,
                       note=note, user=username, image=acess.image,
                       acces=acess)
            v.save()
            acess.quantite = acess.quantite - quantite
            acess.save()

            if type == '1':
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre Acessoire/Iformatique <a href="/accessoires/vendre/{2}/" >{1}</a> .'.format(
                    request.user.username, acess.produit, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('informatique'))
            else:
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre Acessoire/Telephone <a href="/accessoires/vendre/{2}/" >{1}</a> .'.format(
                    request.user.username, acess.produit, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('portable'))

        return render(request, 'accessoires/vendre.html',
                      {'form': form, 'acess': acess, 'id': id})

    else:
        form = VendreForm()
        return render(request, 'accessoires/vendre.html',
                      {'form': form, 'acess': acess, 'id': id})
