# -*- encoding: utf-8 -*-

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
ERROR_CANCELING_ORDER = "Encomenda que foi rejeitada não pode ser cancelada."
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