from django.contrib import admin
from .models import Receita


# melhoria da interface do django admin
class ListandoReceitas(admin.ModelAdmin):
    list_display = ('id', 'nome_receita', 'categoria', 'publicada')  # mostra detalhes das receitas para edição
    list_display_links = ('id', 'nome_receita') # cria links para a edição das receitas
    search_fields = ('nome_receita', ) # cria campo de busca
    list_filter = ('categoria', ) # cria filtros de pesquisa
    list_per_page = 5 # paginação
    list_editable = ('publicada', )


admin.site.register(Receita, ListandoReceitas)

