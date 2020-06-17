from django.shortcuts import render
from .forms import PizzaForm, MultiplePizzaForm
from django.forms import formset_factory

def home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_form = MultiplePizzaForm()
    if request.method =='POST':
        filled_form = PizzaForm(request.POST)#, request.FILES for image request.
        if filled_form.is_valid():
            filled_form.save()
            note = 'Thanks for Ordering, your %s %s and %s pizza is on the way!' %(filled_form.cleaned_data['size'],
            filled_form.cleaned_data['topping1'],
            filled_form.cleaned_data['topping2'],)
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {'pizzaform':new_form, 'note':note, 'multiple_form': multiple_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {'pizzaform': form, 'multiple_form':multiple_form})

def pizzas(request):
    number_of_pizzas = 2
    filled_multiple_forms = MultiplePizzaForm(request.GET)
    if filled_multiple_forms.is_valid():
        number_of_pizzas = filled_multiple_forms.cleaned_data['number']
    PizzaFormSet=formset_factory(PizzaForm, extra=number_of_pizzas)
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST) 
        if filled_formset.is_valid():
            for form in filled_formset:
                print(form.cleaned_data['topping1'])
                note = 'Pizzas have been Ordered'
        else:
            note='Order was not created. Please try again'
        return render(request, 'pizza/pizzas.html', {'note': note, 'formset': formset})
    else:
        return render(request, 'pizza/pizzas.html', { 'formset': formset})               