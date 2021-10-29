from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User  # Classe padrão do django para usuários no banco de dados.
from django.contrib import auth, messages
from receitas.models import Receita


# Rota de cadastro e validações básicas:
def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        if campo_vazio(nome):
            messages.error(request, 'Campo não pode ficar em branco!')
            return redirect('cadastro')
        if campo_vazio(email):
            messages.error(request, 'Campo não pode ficar em branco!')
            return redirect('cadastro')
        if verifica_senha(senha, senha2):
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('cadastro')
        if User.objects.filter(username=nome).exists():
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('cadastro')
        user = User.objects.create_user(username=nome, email=email, password=senha)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


# Rota de Login com validações e autenticações:
def login(request):
    # validação dos campos preenchidos
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']
        if campo_vazio(email) or campo_vazio(senha):
            messages.error(request, 'Campos não podem estar vazios!')
            return redirect('login')

        # Validação da autenticação de usuário:
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha inválida!')
                return redirect('login')
        else:
            messages.error(request, 'Usuário não cadastrado!')
    return render(request, 'usuarios/login.html')


# Rota de logout(sair):
def logout(request):
    auth.logout(request)
    messages.success(request, 'Até breve!')
    return redirect('login')


# Rota Dashboard do Usuário:
def dashboard(request):
    # Confirma se o usuário está logado para envio do template adequado:
    if request.user.is_authenticated:
        id = request.user.id
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        dados = {
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


# Funções de validação de campos:
def campo_vazio(campo):
    return not campo.strip()


def verifica_senha(senha, senha2):
    return senha != senha2
