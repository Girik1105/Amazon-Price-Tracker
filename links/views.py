from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from . import models, forms 

# Create your views here.
@login_required
def index(request):

    prices = models.Link.objects.filter(user=request.user)
    all_products = prices.count()
    form = forms.AddLinkForm()


    context = {
        'prices':prices,
        'all_items_count':all_products,
    
        'form':form,
    }

    if prices.count() > 0:
        discount = []
        for item in prices:
            if item.old_price != None and item.price_difference != None:
                if item.price_difference>0:
                    discount.append(item)
            discount_length = len(discount)   

        context['discounted_items']= discount
        context['discount_count']=  discount_length

    if request.method == 'POST':
        form = forms.AddLinkForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            form.instance.user = request.user
            form.save()
            
            return redirect(reverse('index'))

        
    return render(request, 'index.html', context)

@login_required
def delete_item(request, pk):
    item = models.Link.objects.get(pk=pk)
    
    if item.user == request.user:
        item.delete()
        return redirect(reverse_lazy('index'))
    else:
        return redirect(reverse('index'))

@login_required()
def update(request):
    qs = models.Link.objects.filter(user=request.user)
    for link in qs:
        link.save()
    return redirect('index')