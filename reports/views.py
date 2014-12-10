from django.shortcuts import render
from reports.models import *
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from datetime import date
from datetime import timedelta
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect


@login_required()
def all(request):
    vendes = Vendre.objects.all()
    total1 = vendes.aggregate(total=Sum('prix_de_vendre',
                                        field="prix_de_vendre*quantite"))

    total2 = vendes.aggregate(total=Sum('prix_de_gros',
                                        field="prix_de_gros*quantite"))

    if total1['total'] and total2['total']:
        gain = total1['total'] - total2['total']
    else:
        gain = None

    return render(request, 'reports/vendre.html',
                  {'vendes': vendes.order_by('-date'), 'active': 'all',
                   'total1': total1['total'], 'gain': gain})


@login_required()
def now(request):
    day_now = date.today()
    vendes = Vendre.objects.filter(date__day=day_now.day,
                                   date__year=day_now.year,
                                   date__month=day_now.month
                                   )

    total1 = vendes.aggregate(total=Sum('prix_de_vendre',
                                        field="prix_de_vendre*quantite"))

    total2 = vendes.aggregate(total=Sum('prix_de_gros',
                                        field="prix_de_gros*quantite"))

    if total1['total'] and total2['total']:
        gain = total1['total'] - total2['total']
    else:
        gain = None

    return render(request, 'reports/vendre.html',
                  {'vendes': vendes.order_by('-date'), 'active': 'now',
                   'total1': total1['total'], 'gain': gain})


@login_required()
def semain(request):
    weeksago = date.today() - timedelta(days=7)
    vendes = Vendre.objects.filter(date__gt=weeksago)
    total1 = vendes.aggregate(total=Sum('prix_de_vendre',
                                        field="prix_de_vendre*quantite"))

    total2 = vendes.aggregate(total=Sum('prix_de_gros',
                                        field="prix_de_gros*quantite"))

    if total1['total'] and total2['total']:
        gain = total1['total'] - total2['total']
    else:
        gain = None

    return render(request, 'reports/vendre.html',
                  {'vendes': vendes.order_by('-date'), 'active': 'semain',
                   'total1': total1['total'], 'gain': gain})


@login_required()
def delete_vendre(request,id):
  vendre = get_object_or_404(Vendre, pk=id)
  vendre.delete()
  return HttpResponseRedirect(reverse('all'))



@login_required()
def year(request):
    day_now = date.today()
    vendes = Vendre.objects.filter(date__year=day_now.year)
    total1 = vendes.aggregate(total=Sum('prix_de_vendre',
                                        field="prix_de_vendre*quantite"))

    total2 = vendes.aggregate(total=Sum('prix_de_gros',
                                        field="prix_de_gros*quantite"))

    if total1['total'] and total2['total']:
        gain = total1['total'] - total2['total']
    else:
        gain = None

    return render(request, 'reports/vendre.html',
                  {'vendes': vendes.order_by('-date'), 'active': 'year',
                   'total1': total1['total'], 'gain': gain})


@login_required()
def mois(request):
    day_now = date.today()
    vendes = Vendre.objects.filter(date__month=day_now.month,

                                   date__year=day_now.year)
    total1 = vendes.aggregate(total=Sum('prix_de_vendre',
                                        field="prix_de_vendre*quantite"))

    total2 = vendes.aggregate(total=Sum('prix_de_gros',
                                        field="prix_de_gros*quantite"))

    if total1['total'] and total2['total']:
        gain = total1['total'] - total2['total']
    else:
        gain = None

    return render(request, 'reports/vendre.html',
                  {'vendes': vendes.order_by('-date'), 'active': 'mois',
                   'total1': total1['total'], 'gain': gain})
# Create your views here.
