# Task Tracker — Vue 3 + Django REST Framework

Um aplicativo **Full-Stack** simples e funcional de Gerenciamento de Tarefas (CRUD), desenvolvido para demonstrar a integração entre um frontend reativo em **Vue 3** e uma API REST em **Python (Django)**.

---

## 🚀 Tecnologias Utilizadas

### **Backend**
* [Python](https://www.python.org/)
* [Django Framework](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/) — Criação da API REST
* [Django CORS Headers](https://github.com/adamchainz/django-cors-headers) — Comunicação segura com o Frontend

### **Frontend**
* [Vue 3](https://vuejs.org/) — Composition API (`<script setup>`)
* [Vite](https://vitejs.dev/) — Build tool rápida para desenvolvimento
* [Axios](https://axios-http.com/) — Cliente HTTP para requisições à API
* HTML5 / CSS3

---

## 🛠️ Funcionalidades

- [x] **Listar Tarefas:** Busca e exibe as tarefas salvas no banco de dados.
- [x] **Criar Tarefa:** Adiciona novas tarefas à lista via formulário.
- [x] **Atualizar Status:** Alterna o estado da tarefa entre concluída e pendente.
- [x] **Excluir Tarefa:** Remove permanentemente uma tarefa do banco.

---

## 💻 Como Rodar o Projeto Localmente

### **Pré-requisitos**
* Node.js (v18+)
* Python (v3.10+)
* Git

---

### **1. Clonar o Repositório**

```bash
git clone https://github.com/SEU_USUARIO/task_traker.git
cd task_traker
```

---

### **2. Configurar o Backend (Django)**

1. Acesse o diretório do backend:
   ```bash
   cd backend
   ```

2. Crie e ative um ambiente virtual:
   * **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **Linux/macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Instale as dependências:
   ```bash
   pip install django djangorestframework django-cors-headers
   ```

4. Execute as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```

5. Inicie o servidor da API:
   ```bash
   python manage.py runserver
   ```
   > A API estará rodando em: `http://127.0.0.1:8000/api/tasks/`

---

### **3. Configurar o Frontend (Vue 3)**

1. Abra um **novo terminal**, vá para a raiz do projeto e acesse o diretório do frontend:
   ```bash
   cd task_traker/frontend
   ```

2. Instale as dependências:
   ```bash
   npm install
   ```

3. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev
   ```
   > O app estará disponível no seu navegador em: `http://localhost:5173`

---

## 📂 Estrutura de Pastas

```text
task_traker/
├── backend/                  # Código-fonte da API Django
│   ├── core/                 # Configurações do projeto Django (settings, urls)
│   ├── tasks/                # App de tarefas (models, views, serializers, urls)
│   ├── manage.py
│   └── db.sqlite3            # Banco de dados SQLite local
│
└── frontend/                 # Código-fonte da aplicação Vue 3
    ├── src/
    │   ├── services/
    │   │   └── api.js        # Configuração do Axios para se conectar à API
    │   ├── App.vue           # Componente principal e interface
    │   └── main.js
    └── package.json
```

#Projeto para fins de estudo