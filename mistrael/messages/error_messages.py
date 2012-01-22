# encoding: utf-8

#Cadastrar Usuário
ERROR_ALREADY_REGISTERED_LOGIN = "Já existe um usuário com esse login."   
ERROR_ALREADY_REGISTERED_EMAIL = "Já existe um usuário com esse e-mail." 
ERROR_DIFFERENT_PASSWORDS = "Senha de confirmação diferente da senha escolhida."
ERROR_REQUIRED_FIRST_NAME = "O campo Nome é obrigatório."
ERROR_REQUIRED_LAST_NAME = "O campo Sobrenome é obrigatório."
ERROR_REQUIRED_LOGIN = "O campo Login é obrigatório."
ERROR_REQUIRED_EMAIL = "O campo E-mail é obrigatório."
ERROR_REQUIRED_PASSWORD = "O campo Senha é obrigatório."
ERROR_REQUIRED_CONFIRMATION_PASSWORD = "O campo Confirmação da Senha é obrigatório."
ERROR_MIN_LENGTH_PASSWORD = "A senha deve ter no mínimo 8 caracteres."
ERROR_SENDING_REGISTER_EMAIL = "Não foi possível enviar uma confirmação para esse e-mail. \
Cadastro não realizado. Por favor, verifique se o e-mail informado é válido."
ERROR_SENDING_RECOVER_PASSWORD_EMAIL = "Não foi possível enviar uma recuperação de senha para esse e-mail. \
Por favor, verifique se o e-mail informado é válido."

#Recuperar senha
ERROR_EMAIL_NOT_REGISTERED = "Não existe um usuário cadastrado com esse e-mail." 

#Modificar senha
ERROR_REQUIRED_NEW_PASSWORD = "O campo Nova Senha é obrigatório."
ERROR_REQUIRED_NEW_CONFIRMATION_PASSWORD = "O campo Confirmação da Nova Senha é obrigatório."
ERROR_MIN_LENGTH_NEW_PASSWORD = "A nova senha deve ter no mínimo 8 caracteres."
ERROR_DIFFERENT_NEW_PASSWORDS = "Senha de confirmação diferente da nova senha escolhida."

#Login
ERROR_MANDATORY_FIELDS = "Preencha todos os campos."
ERROR_LOGIN_NOT_REGISTERED = "Não existe um usuário cadastrado com esse login." 
ERROR_INVALID_PASSWORD = "Senha inválida."
ERROR_INACTIVE_ACCOUNT = "Sua conta está inativa. Por favor verifique seu e-mail para ativá-la."
ERROR_INVALID_URL = "Essa url é inválida."

#Ativar conta
ERROR_ALREADY_ACTIVE_ACCOUNT = "Essa conta já está ativa."
ERROR_USER_NOT_REGISTERED = "Usuário não cadastrado."

#Cadastrar Author
ERROR_REQUIRED_AUTHOR_NAME = "O nome do autor é obrigatório."
ERROR_ALREADY_REGISTERED_AUTHOR = "Esse autor já está cadastrado."

#Cadastrar Distribuidora
ERROR_REQUIRED_DISTRIBUTOR_NAME = "O nome da distribuidora é obrigatório."
ERROR_ALREADY_REGISTERED_DISTRIBUTOR = "Essa distribuidora já está cadastrada."

#Cadastrar Editora
ERROR_REQUIRED_PUBLISHER_NAME = "O nome da editora é obrigatório."
ERROR_ALREADY_REGISTERED_PUBLISHER = "Essa editora já está cadastrada."

#Cadastrar Livro
ERROR_ALREADY_REGISTERED_BOOK = "Esse livro já está cadastrado."
ERROR_REQUIRED_BOOK_NAME = "O nome do livro é obrigatório."
ERROR_REQUIRED_ONE_AUTHOR_NAME = "Selecione pelo menos um autor no campo Autor(es)."
ERROR_SAME_PHYSICAL_SPIRITUAL_AUTHOR = "Os autores devem ser diferentes dos autores espirituais."


#Editar Perfil
ERROR_REQUIRED_GENDER = "O campo Gênero é obrigatório."
ERROR_INVALID_DATE = "A data de aniversário é inválida."

#Definir Status
ERROR_MAX_LENGTH_STATUS = "Tamanho máximo de 100 caracteres."

# Adicionar livro aos favoritos
ERROR_ADD_FAVORITE_BOOK = "Nenhum novo livro foi adicionado aos Favoritos."

# Adicionar encomendas
ERROR_INVALID_QUANTITY = "Forneça um valor numérico entre 1 e 20."

# Cancelar encomenda
ERROR_CANCELING_ORDER = "Essa encomenda não pode ser cancelada."
ERROR_ORDER_ALREADY_CANCELED = "Esta encomenda já foi cancelada."

#cadastro na biblioteca
ERROR_REQUIRED_PHONE = "É obrigatório preencher pelo menos um telefone ou celular."
ERROR_REQUIRED_STREET = "O campo Rua é obrigatório."
ERROR_REQUIRED_NUMBER = "O campo Número é obrigatório."
ERROR_REQUIRED_ZIPCODE = "O campo CEP é obrigatório."
ERROR_REQUIRED_NEIGHBORHOOD = "O campo Bairro é obrigatório."

ERROR_INVALID_DDD1 = "O DDD do Contato (1) é inválido."
ERROR_INVALID_DDD2 = "O DDD do Contato (2) é inválido."
ERROR_INVALID_DDD3 = "O DDD do Contato (3) é inválido."
ERROR_INVALID_DDD4 = "O DDD do Contato (4) é inválido."
ERROR_INVALID_PHONE1 = "O número do Contato (1) é inválido."
ERROR_INVALID_PHONE2 = "O número do Contato (2) é inválido."
ERROR_INVALID_PHONE3 = "O número do Contato (3) é inválido."
ERROR_INVALID_PHONE4 = "O número do Contato (4) é inválido."

ERROR_MINLENGTH_DDD1 = "O DDD do Contato (1) deve ter de 2 dígitos."
ERROR_MINLENGTH_DDD2 = "O DDD do Contato (2) deve ter de 2 dígitos."
ERROR_MINLENGTH_DDD3 = "O DDD do Contato (3) deve ter de 2 dígitos."
ERROR_MINLENGTH_DDD4 = "O DDD do Contato (4) deve ter de 2 dígitos."
ERROR_MINLENGTH_PHONE1 = "O número do Contato (1) deve ter de 8 dígitos."
ERROR_MINLENGTH_PHONE2 = "O número do Contato (2) deve ter de 8 dígitos."
ERROR_MINLENGTH_PHONE3 = "O número do Contato (3) deve ter de 8 dígitos."
ERROR_MINLENGTH_PHONE4 = "O número do Contato (4) deve ter de 8 dígitos."

# Emprestar Livros

ERROR_REQUIRED_BOOK_CODE = "O campo Código do Livro é obrigatório."
ERROR_REQUIRED_USER_LOGIN = "O campo Login do Usuário é obrigatório."
ERROR_INEXISTENT_LIBRARY_BOOK = "Não existe um livro, na Biblioteca, com esse código."
ERROR_INEXISTENT_LOGIN = "Não existe um usuário cadastrado com esse login."
ERROR_INVALID_LIBRARY_REGISTER = "O usuário não preencheu o cadastro pessoal na Biblioteca." 
ERROR_USER_ALREADY_BORROWED_A_BOOK = "Este usuário já possui um livro emprestado."
ERROR_BOOK_ALREADY_BORROW = "Este livro já está emprestado."
ERROR_BOOK_ALREADY_RENEWED = "O usuário já havia renovado este livro. Ele não poderá renovar novamente."

#Receber Livros

ERROR_BOOK_NOT_BORROWED = "Este livro não estava emprestado."
ERROR_BOOK_BORROWED_WITH_ANOTHER_USER = "Este livro não estava emprestado com esse usuário."

#Vender Encomenda de Usuário
ERROR_REQUIRED_ORDER_PRICE = "O campo Preço Total da Encomenda é obrigatório."
ERROR_INVALID_ORDER_PRICE = "O Preço Total da Encomenda é inválido. Digite um valor no formato R$ 999.99."
ERROR_NO_ORDER_ROW_SELECTED = "É obrigatório selecionar uma encomenda na tabela."
ERROR_INVALID_ORDER = "Essa encomenda não é válida."
ERROR_UNAVAILABLE_ORDER = "Essa encomenda não está disponível para compra."

#Vender Livro da Prateleira

ERROR_REQUIRED_BOOK_ID = "O campo Livro é obrigatório."
ERROR_REQUIRED_BOOK_PRICE = "O campo Preço do Livro é obrigatório."
ERROR_INVALID_BOOK_PRICE = "O Preço do Livro é inválido. Digite um valor no formato R$ 999.99."
ERROR_UNAVAILABLE_BOOK = "Não há exemplares disponíveis para venda. Caso existam, estão reservados."
ERROR_INVALID_BOOK = "Este livro não existe."

# Gerar Relatório de Contabilidade do Mês

ERROR_REQUIRED_MONTH = "O campo Mês é obrigatório."
ERROR_REQUIRED_YEAR = "O campo Ano é obrigatório."
ERROR_INVALID_MONTH = "Escolha um mês entre Janeiro e Dezembro."
ERROR_INVALID_YEAR = "Esse ano é inválido."
ERROR_INVALID_MONTH_YEAR = "O mês/ano escolhido é posterior ao mês/ano atual."
ERROR_MISSING_PREVIOUS_BALANCE = "Não existe contabilidade para o mês anterior. Realize primeiramente esse balanço."

# Gerar Relatório de Vendas

ERROR_REQUIRED_INITIAL_DATE = "O campo Data Inicial é obrigatório."
ERROR_REQUIRED_ENDING_DATE = "O campo Data Final é obrigatório."

# Pedido de Compra

ERROR_REQUIRED_BOOK = "O campo Livro é obrigatório."
ERROR_REQUIRED_BOOK_QUANTITY = "O campo quantidade é obrigatório."
ERROR_INVALID_INITIAL_DATE = "A Data Inicial é inválida. Forneça um valor no formato: 99/99/9999."
ERROR_INVALID_ENDING_DATE = "A Data Final é inválida. Forneça um valor no formato: 99/99/9999."
ERROR_REQUIRED_INVALID_DATES = "A Data Final deve ser maior que a Data Inicial."
ERROR_REQUIRED_DISTRIBUTOR = "O campo Distribuidora é obrigatório."

# Cadastrar Pagamento

ERROR_REQUIRED_INVOICE = "O campo Nota Fiscal é obrigatório."
ERROR_REQUIRED_DUPLICATE = "O campo Duplicata é obrigatório."
ERROR_INVALID_INVOICE_DUPLICATE = "Essa duplicata não pertence a essa nota fiscal."
ERROR_DUPLICATE_ALREADY_PAID = "O pagamento dessa duplicata já foi cadastrado."
ERROR_REQUIRED_PAYMENT_DATE = "O campo Data de Pagamento é obrigatório."
ERROR_INVALID_PAYMENT_DATE = "A Data de Pagamento é inválida."

# Cadastrar Nota Fiscal

ERROR_REQUIRED_PURCHASE_ORDER = "O campo Pedido de Compra é obrigatório."
ERROR_REQUIRED_INVOICE_NUMBER = "O campo Número da Nota Fiscal é obrigatório."
ERROR_REQUIRED_INVOICE_SERIES = "O campo Número de Série é obrigatório." 
ERROR_INVALID_INVOICE_NUMBER = "O Número da Nota Fiscal é inválido." 
ERROR_INVALID_INVOICE_SERIES = "O Número de Série é inválido."
ERROR_EXISTENT_INVOICE = "Já existe uma nota fiscal cadastrada para esse pedido de compra." 