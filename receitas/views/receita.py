from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from receitas.models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages


# Exibindo receitas na página inicial:
def index(request):
    receitas = Receita.objects.order_by('-data_receita').filter(publicada=True)
    dados = {
        'receitas' : receitas
    }
    return render(request, 'receitas/index.html', dados)


# Exibindo receitas cadastradas:
def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_exibir = {
        'receita':receita
    }
    return render(request, 'receitas/receita.html', receita_a_exibir)


# Rota da página de criação das Receitas:
def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        publicada = request.POST.get('publicada', False)
        foto_receita = request.FILES['foto_receita']

        # Criando Receitas no banco de dados com ORM:
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user,
                                         nome_receita=nome_receita,
                                         ingredientes=ingredientes,
                                         modo_de_preparo=modo_preparo,
                                         tempo_de_preparo=tempo_preparo,
                                         rendimento=rendimento,
                                         categoria=categoria,
                                         publicada=publicada,
                                         foto_receita=foto_receita)
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')


# Rota de edição de receitas:
def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = {'receita':receita}

    return render(request, 'receitas/edita_receita.html', receita_a_editar)


# Rota de Atualização de receitas:
def atualiza_receita(request):
    if request.method == "POST":
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.publicada = request.POST.get('publicada', False)
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES:
            r.foto_receita = request.FILES['foto_receita']
        r.save()

        return redirect('dashboard')


# Rota de exclusão de receitas:
def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

