<script setup>
import { ref, onMounted } from 'vue';
import api from './services/api';

const tasks = ref([]);
const newTaskTitle = ref('');
const isAuthenticated = ref(false);

// Dados do formulário de login
const username = ref('');
const password = ref('');
const loginError = ref('');
const isLoading = ref(false);

// Verifica se o utilizador já tem um token gravado
const checkAuth = () => {
  const token = localStorage.getItem('token');
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    isAuthenticated.value = true;
    fetchTasks();
  } else {
    isAuthenticated.value = false;
  }
};

// Processa o Login chamando a API do Django JWT
const handleLogin = async () => {
  if (!username.value || !password.value) return;
  
  isLoading.value = true;
  loginError.value = '';

  try {
    const response = await api.post('token/', {
      username: username.value,
      password: password.value
    });
    
    const accessToken = response.data.access;
    
    // 1. Salva os tokens no localStorage
    localStorage.setItem('token', accessToken);
    localStorage.setItem('refreshToken', response.data.refresh);
    
    // 2. Garante que as próximas requisições do axios levem o token imediatamente
    api.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    
    isAuthenticated.value = true;
    username.value = '';
    password.value = '';
    
    // 3. Busca as tarefas
    await fetchTasks();
  } catch (error) {
    loginError.value = 'Usuário ou senha incorretos.';
  } finally {
    isLoading.value = false;
  }
};
// Faz o Logout e limpa as credenciais
const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken');
  isAuthenticated.value = false;
  tasks.value = [];
};

// Procura as tarefas vinculadas ao usuário logado
const fetchTasks = async () => {
  try {
    const response = await api.get('tasks/');
    tasks.value = response.data;
  } catch (error) {
    if (error.response?.status === 401) {
      handleLogout();
    }
  }
};

const addTask = async () => {
  if (!newTaskTitle.value.trim()) return;
  try {
    const response = await api.post('tasks/', { title: newTaskTitle.value, completed: false });
    tasks.value.unshift(response.data);
    newTaskTitle.value = '';
  } catch (error) {
    console.error('Erro ao adicionar tarefa:', error);
  }
};

const toggleTask = async (task) => {
  try {
    const response = await api.patch(`tasks/${task.id}/`, { completed: !task.completed });
    task.completed = response.data.completed;
  } catch (error) {
    console.error('Erro ao atualizar tarefa:', error);
  }
};

const deleteTask = async (id) => {
  try {
    await api.delete(`tasks/${id}/`);
    tasks.value = tasks.value.filter(item => item.id !== id);
  } catch (error) {
    console.error('Erro ao eliminar tarefa:', error);
  }
};

onMounted(checkAuth);
</script>

<template>
  <main class="page-wrapper">
    <!-- 1. TELA DE LOGIN (Mostrada se não estiver autenticado) -->
    <div v-if="!isAuthenticated" class="auth-card">
      <div class="auth-header">
        <h2>Task Tracker</h2>
        <p>Acesse com a sua conta do Django</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="input-group">
          <label for="username">Usuário</label>
          <input 
            id="username"
            v-model="username" 
            type="text" 
            placeholder="Digite seu usuário..." 
            required 
          />
        </div>

        <div class="input-group">
          <label for="password">Senha</label>
          <input 
            id="password"
            v-model="password" 
            type="password" 
            placeholder="Digite sua senha..." 
            required 
          />
        </div>

        <p v-if="loginError" class="error-msg">{{ loginError }}</p>

        <button type="submit" :disabled="isLoading" class="btn-primary">
          {{ isLoading ? 'Entrando...' : 'Entrar' }}
        </button>
      </form>
    </div>

    <!-- 2. PAINEL DE TAREFAS (Mostrado quando autenticado) -->
    <div v-else class="app-card">
      <header class="app-header">
        <div>
          <h1>Minhas Tarefas</h1>
          <span class="badge">Sessão Ativa</span>
        </div>
        <button @click="handleLogout" class="btn-logout">Sair</button>
      </header>

      <form @submit.prevent="addTask" class="task-form">
        <input 
          v-model="newTaskTitle" 
          placeholder="O que precisa ser feito?" 
          required 
        />
        <button type="submit" class="btn-add">Adicionar</button>
      </form>

      <ul class="task-list">
        <li v-for="task in tasks" :key="task.id" :class="{ completed: task.completed }">
          <span @click="toggleTask(task)" class="task-title">
            {{ task.title }}
          </span>
          <button @click="deleteTask(task.id)" class="btn-delete">Eliminar</button>
        </li>
      </ul>

      <p v-if="tasks.length === 0" class="empty-msg">Nenhuma tarefa encontrada. Adicione uma acima!</p>
    </div>
  </main>
</template>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f4f6f8;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 1rem;
}

/* Card de Autenticação */
.auth-card {
  background: white;
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
}

.auth-header {
  text-align: center;
  margin-bottom: 2rem;
}

.auth-header h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 1.8rem;
}

.auth-header p {
  color: #7f8c8d;
  margin-top: 0.5rem;
  font-size: 0.9rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  text-align: left;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #34495e;
}

input {
  padding: 0.8rem 1rem;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: border-color 0.2s;
}

input:focus {
  outline: none;
  border-color: #3498db;
}

.btn-primary {
  padding: 0.85rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.error-msg {
  color: #e74c3c;
  font-size: 0.85rem;
  text-align: center;
  margin: 0;
}

/* Card da Aplicação de Tarefas */
.app-card {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 550px;
}

.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #edf2f7;
}

.app-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #2c3e50;
}

.badge {
  font-size: 0.75rem;
  background-color: #e8f8f5;
  color: #27ae60;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-weight: 600;
}

.btn-logout {
  padding: 0.5rem 1rem;
  background-color: #ecf0f1;
  color: #7f8c8d;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.btn-logout:hover {
  background-color: #bdc3c7;
  color: #2c3e50;
}

.task-form {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.task-form input {
  flex: 1;
}

.btn-add {
  padding: 0.8rem 1.5rem;
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}

.btn-add:hover {
  background-color: #27ae60;
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.9rem 0;
  border-bottom: 1px solid #f1f2f6;
}

.task-title {
  cursor: pointer;
  flex: 1;
  color: #2c3e50;
  font-size: 1rem;
}

.completed .task-title {
  text-decoration: line-through;
  color: #bdc3c7;
}

.btn-delete {
  padding: 0.4rem 0.8rem;
  background-color: #ff7675;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.btn-delete:hover {
  background-color: #d63031;
}

.empty-msg {
  text-align: center;
  color: #b2bec3;
  margin-top: 2rem;
}
</style>