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
                                              
    url(r'^gerenciarlivraria/$', 'apps.bookstore.views.manage_bookstore.index'),                         
    url(r'^gerenciarlivraria/cadastrarautor/$', 
        'apps.books.views.register_author'),
    url(r'^gerenciarlivraria/cadastrareditora/$', 
        'apps.books.views.register_publisher'),  
    url(r'^gerenciarlivraria/cadastrardistribuidora/$', 
        'apps.bookstore.views.manage_bookstore.register_distributor'),   
    url(r'^gerenciarlivraria/cadastrarlivro/$', 
        'apps.books.views.register_book'),     
                                          
    url(r'^gerenciarlivraria/cadastrarfuncionario/$', 
        'apps.user_profiles.views.register_employee.index'),  
    url(r'^gerenciarlivraria/cadastrarfuncionario/pesquisar/$', 
        'apps.user_profiles.views.register_employee.search'),    
    url(r'^gerenciarlivraria/cadastrarfuncionario/salvar/$', 
        'apps.user_profiles.views.register_employee.save'),    
                                                            
    url(r'^livraria/$', 'apps.bookstore.views.bookstore.index'),   
    url(r'^livraria/pesquisar/$', 'apps.bookstore.views.bookstore.search_books'),   
    url(r'^livraria/adicionarfavoritos/$', 'apps.bookstore.views.bookstore.add_favorites'),
    url(r'^livraria/encomendarlivros/$', 'apps.bookstore.views.bookstore.order_books'),  
    url(r'^livraria/encomendas/listar/$', 'apps.bookstore.views.bookstore.list_orders'),    
    url(r'^livraria/encomendas/cancelar/$', 'apps.bookstore.views.bookstore.cancel_orders'),  

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
        'apps.bookstore.views.sell_books.index'), 
    url(r'^vendas/prateleira/venderlivro/$', 
        'apps.bookstore.views.sell_books.sell_shelf_book'), 
    url(r'^vendas/prateleira/informacoes/livro/$', 
        'apps.bookstore.views.sell_books.show_book_informations'), 
    url(r'^vendas/encomendas/procurarencomenda/$', 
        'apps.bookstore.views.sell_books.search_user_orders'),   
    url(r'^vendas/encomendas/venderencomenda/$', 
        'apps.bookstore.views.sell_books.sell_order_book'),  
                       
    url(r'^gerenciarlivraria/relatorios/contabilidade/$', 
        'apps.financial.views.generate_month_balance.index'), 
    url(r'^gerenciarlivraria/relatorios/contabilidade/gerar/$', 
        'apps.financial.views.generate_month_balance.generate'),
                          
    url(r'^gerenciarlivraria/relatorios/vendas/$', 
        'apps.financial.views.generate_sale_report.index'),                       
)
