from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gilbi.views.home', name='home'),
    # url(r'^gilbi/', include('gilbi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(.*)$', 'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),    
                       
    url(r'^$', 'apps.user_profiles.views.login.login'), 
    url(r'^logout/$', 'apps.user_profiles.views.login.logout'),           
    url(r'^cadastrar/$', 'apps.user_profiles.views.register_new_user.register'),          
    url(r'^recuperarsenha/$', 'apps.user_profiles.views.recover_password.recover'),
    url(r'^mudarsenha/(?P<id>\d+)/(?P<code>[0-9a-fA-F]{56})/$', 
        'apps.user_profiles.views.recover_password.change_password'),    
    url(r'^ativarconta/(?P<id>\d+)/(?P<code>[0-9a-fA-F]{56})/$', 
        'apps.user_profiles.views.register_new_user.activate_account'), 
    url(r'^desativarconta/(?P<id>\d+)/(?P<code>[0-9a-fA-F]{56})/$', 
        'apps.user_profiles.views.register_new_user.disable_account'),
                       
    url(r'^perfil/$', 'apps.user_profiles.views.profile.index'),
    url(r'^perfil/removerlivrofavorito/(?P<id>\d+)/$', 
        'apps.user_profiles.views.profile.remove_favorite_book'), 
    url(r'^perfil/alterarstatus/$', 'apps.user_profiles.views.profile.change_status'),
    url(r'^perfil/editar/$', 'apps.user_profiles.views.profile.edit'),
    url(r'^perfil/conta/$', 'apps.user_profiles.views.edit_account.index'), 
    url(r'^perfil/conta/editar/$', 'apps.user_profiles.views.edit_account.edit'), 
    url(r'^perfil/conta/excluir/$', 'apps.user_profiles.views.edit_account.exclude'), 
                                              
    url(r'^gerenciarlivraria/$', 'mistrael.views.manage_bookstore_view.index'),                         
    url(r'^gerenciarlivraria/cadastrarautor/$', 
        'apps.books.views.register_author'),
    url(r'^gerenciarlivraria/cadastrareditora/$', 
        'apps.books.views.register_publisher'),  
    url(r'^gerenciarlivraria/cadastrardistribuidora/$', 
        'mistrael.views.manage_bookstore_view.register_distributor'),   
    url(r'^gerenciarlivraria/cadastrarlivro/$', 
        'apps.books.views.register_book'),                        
    url(r'^gerenciarlivraria/cadastrarfuncionario/$', 
        'mistrael.views.register_employee_view.index'),  
    url(r'^gerenciarlivraria/cadastrarfuncionario/pesquisar/$', 
        'mistrael.views.register_employee_view.search'),    
    url(r'^gerenciarlivraria/cadastrarfuncionario/salvar/$', 
        'mistrael.views.register_employee_view.save'),    
                                                            
    url(r'^livraria/$', 'mistrael.views.bookstore_view.index'),   
    url(r'^livraria/pesquisar/$', 'mistrael.views.bookstore_view.search_books'),   
    url(r'^livraria/adicionarfavoritos/$', 'mistrael.views.bookstore_view.add_favorites'),
    url(r'^livraria/encomendarlivros/$', 'mistrael.views.bookstore_view.order_books'),  
    url(r'^livraria/encomendas/listar/$', 'mistrael.views.bookstore_view.list_orders'),    
    url(r'^livraria/encomendas/cancelar/$', 'mistrael.views.bookstore_view.cancel_orders'),  

    url(r'^gerenciarbiblioteca/$', 'apps.library.views.manage_library.index'),                         
    url(r'^gerenciarbiblioteca/livrosemprestados/listar/$', 
        'apps.library.views.manage_library.list_loans'),
    url(r'^gerenciarbiblioteca/emprestarlivro/$', 
        'apps.library.views.manage_library.borrow_book'),
    url(r'^gerenciarbiblioteca/receberlivro/$', 
        'apps.library.views.manage_library.receive_book'),
    url(r'^gerenciarbiblioteca/informacoes/usuario/(?P<id>\d+)/$', 
        'apps.library.views.manage_library.show_user_informations'),
    url(r'^gerenciarbiblioteca/informacoes/livro/$', 
        'apps.library.views.manage_library.show_book_informations'),
                                                                         
    url(r'^biblioteca/$', 'apps.library.views.library.index'),  
    url(r'^biblioteca/pesquisarlivros/$', 'apps.library.views.library.search_books'), 
    url(r'^biblioteca/meusemprestimos/listar/$', 'apps.library.views.library.list_loans'),  
    
    url(r'^vendas/$', 
        'mistrael.views.sell_books.index'), 
    url(r'^vendas/prateleira/venderlivro/$', 
        'mistrael.views.sell_books.sell_shelf_book'), 
    url(r'^vendas/prateleira/informacoes/livro/$', 
        'mistrael.views.sell_books.show_book_informations'), 
    url(r'^vendas/encomendas/procurarencomenda/$', 
        'mistrael.views.sell_books.search_user_orders'),   
    url(r'^vendas/encomendas/venderencomenda/$', 
        'mistrael.views.sell_books.sell_order_book'),                           
)
