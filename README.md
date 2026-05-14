# 💍 VouCasar - Lista de Casamento

Um sistema completo para gerenciamento de lista de casamento com frontend React e backend FastAPI.

## 📋 Estrutura do Projeto

```
voucasar/
├── frontend/                      # React + React Router + Tailwind
│   ├── src/
│   │   ├── App.tsx               # Componente principal com rotas
│   │   ├── main.tsx              # Entry point
│   │   ├── index.css             # Estilos globais
│   │   ├── lib/
│   │   │   ├── api.ts            # Configuração do Axios
│   │   │   └── services.ts       # APIs e tipos
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx   # Contexto de autenticação
│   │   ├── components/
│   │   │   ├── Header.tsx        # Cabeçalho com menu
│   │   │   └── ProtectedRoute.tsx # Rota protegida
│   │   └── pages/
│   │       ├── HomePage.tsx
│   │       ├── LoginPage.tsx
│   │       ├── DashboardPage.tsx
│   │       ├── PresentsPage.tsx
│   │       └── NotFoundPage.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── postcss.config.js
│
├── backend/
│   ├── data/
│   │   ├── model/                # Modelos de dados
│   │   │   ├── usuario.py
│   │   │   ├── casal.py
│   │   │   ├── presente.py
│   │   │   ├── fonte_compra.py
│   │   │   └── transacao_presente.py
│   │   ├── repo/                 # Repositórios (CRUD)
│   │   │   ├── usuario.py
│   │   │   ├── casal.py
│   │   │   ├── presente.py
│   │   │   ├── fonte_compra.py
│   │   │   └── transacao_presente.py
│   │   └── sql/                  # Queries SQL
│   │       ├── usuario_sql.py
│   │       ├── casal_sql.py
│   │       ├── presente_sql.py
│   │       ├── fonte_compra_sql.py
│   │       └── transacao_presente_sql.py
│   └── routers/                  # Rotas FastAPI
│       ├── usuario.py
│       ├── casal.py
│       ├── presente.py
│       ├── fonte_compra.py
│       └── transacao_presente.py
│
├── main.py                       # Aplicação FastAPI principal
└── requirements.txt             # Dependências Python
```

## 🚀 Como Executar

### Backend (FastAPI)

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Configurar variáveis de ambiente
cp .env.example .env  # Edite com suas configurações

# 3. Executar servidor
python main.py
# O servidor estará em http://localhost:8000
```

### Frontend (React)

```bash
# 1. Entrar no diretório do frontend
cd frontend

# 2. Instalar dependências
npm install

# 3. Executar servidor de desenvolvimento
npm run dev
# O frontend estará em http://localhost:5173
```

## 📱 Funcionalidades

### Dashboard
- 💾 Visualizar todos os casais cadastrados
- ➕ Criar novos casais
- 📅 Ver data do casamento
- 💳 Gerenciar chave PIX

### Presentes
- 🎁 Listar presentes por casal
- ✏️ Adicionar novos presentes
- 📊 Definir categoria e valor estimado
- 🏷️ Gerenciar status (disponível, reservado, comprado)
- 🔗 Adicionar fontes de compra (URLs)

### Autenticação
- 🔐 Login com email e senha
- 🔑 Sessão com autenticação via JWT
- 🚪 Logout
- 🛡️ Proteção de rotas

## 🔗 Rotas da API

### Usuários
- `POST /usuario` - Criar usuário
- `GET /usuario/{id}` - Buscar usuário por ID
- `PUT /usuario/{id}` - Atualizar usuário
- `GET /usuario` - Listar todos os usuários

### Casais
- `POST /casal` - Criar casal
- `GET /casal/{id}` - Buscar casal por ID
- `PUT /casal/{id}` - Atualizar casal
- `DELETE /casal/{id}` - Deletar casal
- `GET /casal` - Listar todos os casais

### Presentes
- `POST /presente` - Criar presente
- `GET /presente/{id}` - Buscar presente por ID
- `PUT /presente/{id}` - Atualizar presente
- `DELETE /presente/{id}` - Deletar presente
- `GET /presente/casal/{casal_id}` - Listar presentes por casal

### Fontes de Compra
- `POST /fonte-compra` - Criar fonte
- `GET /fonte-compra/{id}` - Buscar fonte por ID
- `PUT /fonte-compra/{id}` - Atualizar fonte
- `DELETE /fonte-compra/{id}` - Deletar fonte
- `GET /fonte-compra/presente/{presente_id}` - Listar fontes por presente

### Transações de Presente
- `POST /transacao-presente` - Criar transação
- `GET /transacao-presente/{id}` - Buscar transação por ID
- `PUT /transacao-presente/{id}` - Atualizar transação
- `DELETE /transacao-presente/{id}` - Deletar transação
- `GET /transacao-presente/casal/{casal_id}` - Listar por casal
- `GET /transacao-presente/convidado/{convidado_id}` - Listar por convidado

## 🛠️ Tecnologias

### Frontend
- **React 18** - Framework UI
- **React Router 6** - Roteamento
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização
- **Axios** - Cliente HTTP
- **Lucide React** - Ícones

### Backend
- **FastAPI** - Framework web
- **Python 3.9+** - Linguagem
- **MySQL/MariaDB** - Banco de dados
- **Pydantic** - Validação de dados
- **SQLAlchemy** (opcional) - ORM

## 📦 Dependências Python (requirements.txt)

```
fastapi==0.104.1
uvicorn==0.24.0
starlette==0.27.0
python-dotenv==1.0.0
mysql-connector-python==8.2.0
pydantic==2.5.0
pydantic-settings==2.1.0
```

## 🔐 Variáveis de Ambiente (.env)

```env
# Ambiente
ENVIRONMENT=development
FRONTEND_URL=http://localhost:5173

# Banco de Dados
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=voucasar

# Segurança
SECRET_KEY=sua-chave-secreta-aqui

# Servidor
PORT=8000
```

## 🎨 Fluxo de Uso

1. **Login**: Usuário acessa a tela de login
2. **Dashboard**: Visualiza todos os casais
3. **Seleciona um Casal**: Clica em um casal para ver presentes
4. **Gerencia Presentes**: Adiciona, edita ou remove presentes
5. **Adiciona Fontes**: Para cada presente, pode adicionar links de compra
6. **Acompanha Transações**: Vê quem vai comprar cada presente

## 📝 Notas Importantes

- Todas as rotas da API (exceto `/login`) requerem autenticação
- O frontend se conecta ao backend via CORS
- As sessões expiram após 30 minutos de inatividade
- Senhas devem ser hasheadas antes de serem armazenadas
- Use HTTPS em produção

## 🤝 Contribuindo

Para contribuir com melhorias:

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT.

## 👥 Suporte

Para suporte, envie um email para suporte@voucasar.com ou abra uma issue no repositório.

---

**Desenvolvido com ❤️ por VouCasar**
