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
                       
    url(r'^$', 'mistrael.views.login_view.login'), 
    url(r'^logout/$', 'mistrael.views.login_view.logout'),           
    url(r'^cadastrar/$', 'mistrael.views.register_new_user_view.register'),          
    url(r'^recuperarsenha/$', 'mistrael.views.recover_password_view.recover'),
    url(r'^mudarsenha/(?P<id>\d+)/(?P<code>[0-9a-fA-F]{56})/$', 
        'mistrael.views.recover_password_view.change_password'),    
    url(r'^ativarconta/(?P<id>\d+)/(?P<code>[0-9a-fA-F]{56})/$', 
        'mistrael.views.register_new_user_view.activate_account'), 
    url(r'^desativarconta/(?P<id>\d+)/(?P<code>[0-9a-fA-F]{56})/$', 
        'mistrael.views.register_new_user_view.disable_account'),
                       
    url(r'^perfil/$', 'mistrael.views.profile_view.index'),
    url(r'^perfil/removerlivrofavorito/(?P<id>\d+)/$', 
        'mistrael.views.profile_view.remove_favorite_book'), 
    url(r'^perfil/alterarstatus/$', 'mistrael.views.profile_view.change_status'),
    url(r'^perfil/editar/$', 'mistrael.views.profile_view.edit'),
    url(r'^perfil/conta/$', 'mistrael.views.edit_account_view.index'), 
    url(r'^perfil/conta/editar/$', 'mistrael.views.edit_account_view.edit'), 
    url(r'^perfil/conta/excluir/$', 'mistrael.views.edit_account_view.exclude'), 
                                              
    url(r'^gerenciarlivraria/$', 'mistrael.views.manage_bookstore_view.index'),                         
    url(r'^gerenciarlivraria/cadastrarautor/$', 
        'mistrael.views.manage_bookstore_view.register_author'),
    url(r'^gerenciarlivraria/cadastrareditora/$', 
        'mistrael.views.manage_bookstore_view.register_publisher'),  
    url(r'^gerenciarlivraria/cadastrardistribuidora/$', 
        'mistrael.views.manage_bookstore_view.register_distributor'),   
    url(r'^gerenciarlivraria/cadastrarlivro/$', 
        'mistrael.views.manage_bookstore_view.register_book'),                        
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

    url(r'^gerenciarbiblioteca/$', 'mistrael.views.manage_library_view.index'),                         
    url(r'^gerenciarbiblioteca/livrosemprestados/listar/$', 
        'mistrael.views.manage_library_view.list_loans'),
    url(r'^gerenciarbiblioteca/emprestarlivro/$', 
        'mistrael.views.manage_library_view.borrow_book'),
    url(r'^gerenciarbiblioteca/receberlivro/$', 
        'mistrael.views.manage_library_view.receive_book'),
    url(r'^gerenciarbiblioteca/informacoes/usuario/(?P<id>\d+)/$', 
        'mistrael.views.manage_library_view.show_user_informations'),
    url(r'^gerenciarbiblioteca/informacoes/livro/$', 
        'mistrael.views.manage_library_view.show_book_informations'),
                                                                         
    url(r'^biblioteca/$', 'mistrael.views.library_view.index'),  
    url(r'^biblioteca/pesquisarlivros/$', 'mistrael.views.library_view.search_books'), 
    url(r'^biblioteca/meusemprestimos/listar/$', 'mistrael.views.library_view.list_loans'),                                 
)
