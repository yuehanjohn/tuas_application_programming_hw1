from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import BoardGame, Loan
from django.contrib.auth.models import User
from django.utils import timezone


def index(request):
    games = BoardGame.objects.all()
    return render(request, 'lending/index.html', {'games': games})

@login_required
def borrow_game(request, game_id):
    game = BoardGame.objects.get(id=game_id)
    if Loan.objects.filter(borrower=request.user, returned_at__isnull=True).count() >= 3:
        return render(request, 'lending/error.html', {'message': 'You cannot borrow more than 3 games simultaneously.'})
    Loan.objects.create(game=game, borrower=request.user)
    return redirect('index')

@login_required
def return_game(request, loan_id):
    loan = Loan.objects.get(id=loan_id)
    loan.returned_at = timezone.now()
    loan.save()
    return redirect('index')

@login_required
def add_game(request):
    if request.method == 'POST':
        form = BoardGameForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BoardGameForm()
    return render(request, 'lending/add_game.html', {'form': form})



from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

from django import forms
class BoardGameForm(forms.ModelForm):
    class Meta:
        model = BoardGame
        fields = ['title', 'description']