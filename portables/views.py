from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from portables.forms import *
from portables.models import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from feeds.models import *
from reports.models import *


@login_required()
def vendre_port(request, id):
    vendre = get_object_or_404(Vendre, pk=id)
    return render(request, 'portables/vendre_port.html',
                  {'vendre': vendre})


@login_required()
def portable(request, id):
    portable = get_object_or_404(Portable, pk=id)
    return render(request, 'portables/portable.html',
                  {'portable': portable})


@login_required()
def nouveau(request):
    nouveau = Portable.objects.filter(type="Nouveau")
    return render(request, 'portables/nouveau.html',
                  {'nouveau': nouveau})


@login_required()
def occasion(request):
    occasion = Portable.objects.filter(type="Occasion")
    return render(request, 'portables/occasion.html',
                  {'occasion': occasion})


@login_required()
def edite_portable(request, id, type):
    port = get_object_or_404(Portable, pk=id)
    if request.POST:
        form = PortableForm(request.POST,  request.FILES, instance=port)
        if form.is_valid():
            form.save()
            if type == '1':
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Telephon/Nouveaux <a href="/portables/portable/{2}/" >{1}</a> .'.format(
                    request.user.username,  port.marque + '-' + port.model, port.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return redirect('nouveau')
            else:
                adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifie Telephon/Occasion <a href="/portables/portable/{2}/" >{1}</a> .'.format(
                    request.user.username,  port.marque + '-' + port.model, port.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return redirect('occasion')

    else:
        form = PortableForm(instance=port)
    return render(request, 'portables/edit_portables.html', {'form': form,
                                                                 'type': type})


@login_required()
def delete_portable(request, id, type):
    if id:
        port = get_object_or_404(Portable, pk=id)
        port.delete()
    adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime Telephon {1} .'.format(
        request.user.username, port.marque + '-' + port.model, port.id)
    feed = Feed(user=request.user.username, post=adding)
    feed.save()
    if type == '1':
        return redirect('nouveau')
    else:
        return redirect('occasion')


@login_required()
def add_portable(request, id):
    if request.method == 'POST':
        form = PortableForm(request.POST, request.FILES,)
        if form.is_valid():
            pk = form.save()
            if id == '1':
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Telephon/Nouveaux <a href="/portables/portable/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('marque') + '-' + form.cleaned_data.get('model'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('nouveau'))
            else:
                adding = u' <span class="glyphicon glyphicon-pencil"></span> <b>{0}</b> ajoute Telephon/Occasion <a href="/portables/portable/{2}/" >{1}</a> .'.format(
                    request.user.username, form.cleaned_data.get('marque') + '-' + form.cleaned_data.get('model'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('occasion'))

        return render(request, 'portables/add_portables.html',
                      {'form': form, 'id': id})
    else:
        form = PortableForm()
        return render(request, 'portables/add_portables.html',
                      {'form': form, 'id': id})


@login_required()
def vendre_portable(request, id, type):
    port = get_object_or_404(Portable, pk=id)
    if request.method == 'POST':
        form = VendreForm(request.POST)
        if form.is_valid():
            prix_de_vendre = form.cleaned_data.get('prix_de_vendre')
            quantite = form.cleaned_data.get('quantite')
            note = form.cleaned_data.get('note')
            v = Vendre(item=port.marque + ' ' + port.model,
                       type=port.type,
                       prix_de_gros=port.prix_de_gros,
                       prix_de_vendre=prix_de_vendre,
                       quantite=quantite, note=note,
                       user=request.user.username, image=port.image,
                       port=port
                       )
            v.save()
            port.quantite = port.quantite - quantite
            port.save()

            if type == '1':
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre  Telephon/Nouveaux <a href="/portables/vendre_port/{2}/" >{1}</a> .'.format(
                    request.user.username, port.marque + '-' + port.model, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('nouveau'))
            else:
                adding = u' <span class="glyphicon glyphicon-usd"></span> <b>{0}</b> Vendre  Telephon/Occasion <a href="/portables/vendre_port/{2}/" >{1}</a> .'.format(
                    request.user.username, port.marque + '-' + port.model, v.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('occasion'))

        return render(request, 'portables/vendre.html',
                      {'form': form, 'port': port, 'id': id})

    else:
        form = VendreForm()
        return render(request, 'portables/vendre.html',
                      {'form': form, 'port': port, 'id': id})
