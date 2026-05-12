# 📋 Task Manager — Django + WhatsApp + Railway

Sistema web de gerenciamento de tarefas com alertas automáticos via WhatsApp, autenticação de usuários e deploy na nuvem.

---

## 🚀 Funcionalidades

- ✅ Cadastro e login de usuários
- ✅ Cada usuário tem suas próprias tarefas
- ✅ Cadastro de tarefas com título, descrição e data de vencimento
- ✅ Alerta automático via WhatsApp no dia do vencimento (08h)
- ✅ Botão de concluir que remove a tarefa
- ✅ Deploy na nuvem com URL pública gratuita

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Linguagem principal |
| Django 5 | Framework web |
| PostgreSQL | Banco de dados em produção |
| APScheduler | Agendamento dos alertas |
| CallMeBot API | Envio de mensagens WhatsApp |
| WhiteNoise | Arquivos estáticos em produção |
| Gunicorn | Servidor WSGI em produção |
| Railway | Hospedagem e deploy |

---

## 📁 Estrutura do Projeto

```
task_manager/
├── core/
│   ├── settings.py       # Configurações do Django
│   ├── urls.py           # URLs principais
│   └── wsgi.py           # Entry point + inicialização do scheduler
├── tasks/
│   ├── models.py         # Models: Task e Perfil
│   ├── views.py          # Views: lista, criar, concluir, login, registro
│   ├── urls.py           # URLs do app
│   ├── scheduler.py      # Job diário de alertas WhatsApp
│   ├── whatsapp.py       # Função de envio via CallMeBot
│   ├── apps.py           # Configuração do app
│   └── templates/
│       └── tasks/
│           ├── lista.html
│           ├── criar.html
│           ├── login.html
│           └── registro.html
├── manage.py
├── requirements.txt
├── Procfile
└── .env                  # Variáveis de ambiente (não subir no Git)
```

---

## ⚙️ Instalação Local

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/task-manager.git
cd task-manager
```

### 2. Crie o ambiente virtual e instale as dependências

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua_secret_key_aqui
DEBUG=True
CALLMEBOT_API_KEY=sua_api_key_aqui
```

### 4. Rode as migrações e inicie o servidor

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Acesse: **http://localhost:8000**

---

## 🌐 Deploy no Railway

### 1. Variáveis de ambiente no Railway

Configure em **Settings → Variables**:

| Variável | Valor |
|---|---|
| `SECRET_KEY` | Sua secret key do Django |
| `DEBUG` | `False` |
| `CALLMEBOT_API_KEY` | Sua API Key do CallMeBot |
| `DATABASE_URL` | Gerada automaticamente pelo PostgreSQL |

### 2. Start Command

Em **Settings → Deploy → Start Command**:

```
python manage.py migrate && gunicorn core.wsgi --bind 0.0.0.0:$PORT --log-file -
```

### 3. URL pública

Em **Settings → Networking → Generate Domain**, o Railway gera uma URL pública automaticamente.

---

## 📲 Configuração do CallMeBot (WhatsApp)

1. Adicione o número **+34 698 28 89 73** na sua agenda
2. Envie pelo WhatsApp: `I allow callmebot to send me messages`
3. Você receberá sua **API Key** por mensagem
4. Salve essa chave na variável `CALLMEBOT_API_KEY`

> O alerta é enviado automaticamente todo dia às **08h00** para tarefas com vencimento no dia.

---

## 👤 Como usar

1. Acesse a URL do sistema
2. Clique em **Cadastre-se** e informe usuário, senha e número do WhatsApp
3. Faça login
4. Clique em **+ Nova Tarefa** para cadastrar uma tarefa com data de vencimento
5. No dia do vencimento às 08h você receberá um alerta no WhatsApp
6. Clique em **✅ Concluir** para remover a tarefa quando finalizar

---

## 🔒 Segurança

- Senhas armazenadas com hash (Django `create_user`)
- CSRF protection ativo em todos os formulários
- Cada usuário acessa apenas suas próprias tarefas
- Variáveis sensíveis em variáveis de ambiente (nunca no código)
- `DEBUG=False` em produção

---

## 📄 Licença

Projeto pessoal — livre para uso e modificação.
