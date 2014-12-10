from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from reparations.forms import *
from reparations.models import *
from reports.models import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime
from django.contrib.auth.decorators import login_required
from feeds.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum


@login_required()
def terminer(request):

    terminers = Reparation.objects.filter(status="T")
    paginator = Paginator(terminers, 5)
    page = request.GET.get('page')
    try:
        terminer = paginator.page(page)
    except PageNotAnInteger:
        terminer = paginator.page(1)
    except EmptyPage:
        terminer = paginator.page(paginator.num_pages)

    return render(request, 'reparations/terminer.html',
                  {'terminer': terminer})


@login_required()
def encour(request):
    encours = Reparation.objects.filter(status="E")
    paginator = Paginator(encours, 5)
    page = request.GET.get('page')
    try:
        encour = paginator.page(page)
    except PageNotAnInteger:
        encour = paginator.page(1)
    except EmptyPage:
        encour = paginator.page(paginator.num_pages)
    return render(request, 'reparations/encour.html',
                  {'encour': encour})


@login_required()
def reparation(request, id):
    reparation = get_object_or_404(Reparation, pk=id)
    factures = Piece.objects.filter(reparation__id=id)
    mainouvres = MainOuevre.objects.filter(reparation__id=id)

    total1 = factures.aggregate(total1=Sum('prix', field="prix*quantite"))
    total2 = mainouvres.aggregate(total2=Sum('prix'))
    if total1['total1'] and total2['total2']:
        total = total1['total1'] + total2['total2']
    elif total1['total1'] is None:
        total = total2['total2']
    elif total2['total2'] is None:
        total = total1['total1']

    return render(request, 'reparations/reparation.html',
                  {'reparation': reparation, 'factures': factures,
                   'mainouvres': mainouvres, 'total': total})


@login_required()
def change_status(request, id):
    reparation = get_object_or_404(Reparation, pk=id)
    if reparation.status == "E":
        reparation.status = "T"
        reparation.date_finish = datetime.now()
        reparation.finish_user = request.user.username
        reparation.save()
        adding = u' <span class="glyphicon glyphicon-edit"></span> {0} change status de  <a href="/reparations/reparation/{2}/" > {1} </a>  a termine.'.format(
            request.user.username,  reparation.item, reparation.id)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
    else:
        reparation.status = "E"
        reparation.save()
        adding = u' <span class="glyphicon glyphicon-edit"></span> {0} change status de  <a href="/reparations/reparation/{2}/" > {1} </a>  a en cours.'.format(
            request.user.username,  reparation.item, reparation.id)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
    return redirect('encour')


@login_required()
def edite_reparation(request, id):
    reparation = get_object_or_404(Reparation, pk=id)
    if request.POST:
        form = ReparationForm(request.POST, instance=reparation)
        if form.is_valid():
            form.save()
            adding = u' <span class="glyphicon glyphicon-edit"></span> {0} modifie une reparation : <a href="/reparations/reparation/{2}/" > {1} </a>.'.format(
                request.user.username, reparation.item, reparation.id)
            feed = Feed(user=request.user.username, post=adding)
            feed.save()
            return redirect('reparation', id=id)

    else:
        form = ReparationForm(instance=reparation)
    return render(request, 'reparations/edit_reparations.html', {'form': form})


@login_required()
def delete_reparation(request, id):
    if id:
        reparation = get_object_or_404(Reparation, pk=id)
        reparation.delete()
    if reparation.status == 'E':
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime Reparation/En cours : <b>{1} </b>.'.format(
            request.user.username, reparation.item)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return redirect('encour')
    else:
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime Reparation/Termine : <b>{1} </b>.'.format(
            request.user.username, reparation.item)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()
        return redirect('terminer')


@login_required()
def edite_piece(request, id):
    piece = get_object_or_404(Piece, pk=id)
    if request.POST:
        form = FactureForm(request.POST)
        if form.is_valid():
            form.save(piece_id=id)
            adding = u' <span class="glyphicon glyphicon-edit"></span> <b>{0}</b> modifier une piece <b>{1}</b> de reparatin  : <a href="/reparations/reparation/{2}/" >{3}</a>.'.format(
                request.user.username, piece.item, piece.reparation.id, piece.reparation.item)
            feed = Feed(user=request.user.username, post=adding)
            feed.save()
            return redirect('reparation', id=piece.reparation.id)

    else:
        data = {'item': piece.item,
                'prix_de_gros': piece.prix_de_gros,
                'prix': piece.prix,
                'description': piece.description,
                'quantite': piece.quantite}

        form = FactureForm(data)
    return render(request, 'reparations/edit_piece.html', {'form': form,
                                                           'piece_id': piece.id})


@login_required()
def delete_piece(request, id):
    if id:
        piece = get_object_or_404(Piece, pk=id)
        piece.delete()
        adding = u' <span class="glyphicon glyphicon-remove-circle"></span> <b>{0}</b> supprime une piece <b>{1}</b> de reparatin : <a href="/reparations/reparation/{2}/" >{3}</a>.'.format(
            request.user.username, piece.item, piece.reparation.id, piece.reparation.item)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()

    return redirect('reparation', id=piece.reparation.id)


@login_required()
def add_reparation(request, id):
    if request.method == 'POST':
        form = ReparationForm(request.POST)
        if form.is_valid():
            pk = form.save()
            pk .add_user = request.user.username
            pk.save()
            if id == '1':
                adding = u' <span class="glyphicon glyphicon-pencil"></span> {0} ajoute une reparation en cours : <a href="/reparations/reparation/{2}/" > {1} .'.format(
                    request.user.username, form.cleaned_data.get('item'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('encour'))
            else:
                adding = u' <span class="glyphicon glyphicon-pencil"></span> {0} ajoute une reparation termine : <a href="/reparations/reparation/{2}/" > {1} .'.format(
                    request.user.username, form.cleaned_data.get('item'), pk.id)
                feed = Feed(user=request.user.username, post=adding)
                feed.save()
                return HttpResponseRedirect(reverse('terminer'))

        return render(request, 'reparations/add_reparations.html',
                      {'form': form, 'id': id})
    else:
        form = ReparationForm()
        return render(request, 'reparations/add_reparations.html',
                      {'form': form, 'id': id})


@login_required()
def add_facture(request, id):

    if request.method == 'POST':
        form = FactureForm(request.POST)
        if form.is_valid():
            reparation = get_object_or_404(Reparation, pk=id)
            item = form.cleaned_data.get('item')
            prix_de_gros = form.cleaned_data.get('prix_de_gros')
            prix = form.cleaned_data.get('prix')
            quantite = form.cleaned_data.get('quantite')
            description = form.cleaned_data.get('description')

            facture = Piece(reparation=reparation, item=item, prix=prix,
                            prix_de_gros=prix_de_gros, quantite=quantite,
                            description=description)
            facture.save()

            adding = u' <span class="glyphicon glyphicon-pencil"></span> {0} ajoute piece {1} au reparation <a href="/reparations/reparation/{3}/" > {2}</a>  .'.format(
                request.user.username, item, reparation.item, reparation.pk)
            feed = Feed(user=request.user.username, post=adding,)
            feed.save()

            return redirect('reparation', id=id)

        return render(request, 'reparations/add_facture.html',
                      {'form': form, 'id': id})
    else:
        form = FactureForm()
        return render(request, 'reparations/add_facture.html',
                      {'form': form, 'id': id})


@login_required()
def add_mainouvre(request, id):

    if request.method == 'POST':
        form = MainOuevreForm(request.POST)
        if form.is_valid():
            reparation = get_object_or_404(Reparation, pk=id)
            prix = form.cleaned_data.get('prix')
            description = form.cleaned_data.get('description')

            mainouvre = MainOuevre(reparation=reparation,  prix=prix,
                                   description=description)
            mainouvre.save()
            adding = u" <span class='glyphicon glyphicon-pencil'></span> {0} ajoute main d'ouvre au reparation <a href='/reparations/reparation/{2}/' >{1}</a>  .".format(
                request.user.username, reparation.item, reparation.pk)
            feed = Feed(user='admin', post=adding,)
            feed.save()
            return redirect('reparation', id=id)

        return render(request, 'reparations/add_mainouvre.html',
                      {'form': form, 'id': id})
    else:
        form = MainOuevreForm()
        return render(request, 'reparations/add_mainouvre.html',
                      {'form': form, 'id': id})


@login_required()
def edite_main(request, id):
    main = get_object_or_404(MainOuevre, pk=id)
    if request.POST:
        form = MainOuevreForm(request.POST)
        if form.is_valid():
            form.save(main_id=id)
            adding = u" <span class='glyphicon glyphicon-edit'></span> {0} modifie main d'ouvre de reparation <a href='/reparations/reparation/{1}/' >{2}</a>  .".format(
                request.user.username, main.reparation.id, main.reparation.item)
            feed = Feed(user=request.user.username, post=adding)
            feed.save()
            return redirect('reparation', id=main.reparation.id)

    else:
        data = {'prix': main.prix,
                'description': main.description, }
        form = MainOuevreForm(data)

    return render(request, 'reparations/edit_main.html', {'form': form,
                                                          'main_id': main.id})


@login_required()
def delete_main(request, id):
    if id:
        main = get_object_or_404(MainOuevre, pk=id)
        main.delete()
        adding = u"<span class='glyphicon glyphicon-remove-circle'></span> {0} supprime main d'ouvre de reparation <a href='/reparations/reparation/{1}/' >{2}</a>  .".format(
            request.user.username, main.reparation.id, main.reparation.item)
        feed = Feed(user=request.user.username, post=adding)
        feed.save()

    return redirect('reparation', id=main.reparation.id)


@login_required()
def paye(request, id):
    reparation = get_object_or_404(Reparation, pk=id)
    factures = Piece.objects.filter(reparation__id=id)
    mainouvres = MainOuevre.objects.filter(reparation__id=id)

    total1 = factures.aggregate(total1=Sum('prix', field="prix*quantite"))
    total2 = mainouvres.aggregate(total2=Sum('prix'))
    if total1['total1'] and total2['total2']:
        total = total1['total1'] + total2['total2']
    elif total1['total1'] is None:
        total = total2['total2']
    elif total2['total2'] is None:
        total = total1['total1']

    totalgros = factures.aggregate(total1=Sum('prix',
                                              field="prix_de_gros*quantite"))

    if totalgros['total1'] == None :
        totalgros['total1'] = 0

    if total == None :
        total = 0

    username = request.user.username
    v = Vendre(item=reparation.item, type='R',
               prix_de_gros=totalgros['total1'],
               prix_de_vendre=total, quantite=1, user=username,
               reparation=reparation.id)
    v.save()
    reparation.status = 'P'
    reparation.save()

    adding = u' <span class="glyphicon glyphicon-usd"></span>  reparation <a href="/reparations/reparation/{2}/" >{1}</a> est payee a <b>{0}</b> .'.format(
        request.user.username, reparation.item, reparation.id)
    feed = Feed(user=request.user.username, post=adding)
    feed.save()
    return redirect('terminer')
