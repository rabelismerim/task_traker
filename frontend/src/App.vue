<script setup>
import { ref, onMounted } from 'vue';
import api from './services/api';

const tasks = ref([]);
const newTaskTitle = ref('');

const fetchTasks = async () => {
  try {
    const response = await api.get('tasks/');
    tasks.value = response.data;
  } catch (error) {
    console.error('Erro ao procurar tarefas:', error);
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
    tasks.value = tasks.value.filter(task => task.id !== id);
  } catch (error) {
    console.error('Erro ao eliminar tarefa:', error);
  }
};

onMounted(fetchTasks);
</script>

<template>
  <main class="container">
    <h1>Gerenciador de Tarefas</h1>

    <form @submit.prevent="addTask" class="form">
      <input v-model="newTaskTitle" placeholder="Digite uma nova tarefa..." required />
      <button type="submit">Adicionar</button>
    </form>

    <ul class="task-list">
      <li v-for="task in tasks" :key="task.id" :class="{ completed: task.completed }">
        <span @click="toggleTask(task)">{{ task.title }}</span>
        <button @click="deleteTask(task.id)">Eliminar</button>
      </li>
    </ul>
  </main>
</template>

<style scoped>
.container {
  max-width: 500px;
  margin: 2rem auto;
  font-family: sans-serif;
  padding: 0 1rem; /* Adiciona um pequeno padding nas laterais para mobile */
}

h1 {
  text-align: center;      /* Centraliza o título */
  line-height: 1.2;        /* CORREÇÃO: Aumenta o espaçamento entre as linhas para não sobrepor */
  margin-bottom: 2rem;     /* Aumenta o espaço entre o título e o formulário */
  word-wrap: break-word;   /* Garante que palavras longas quebrem se necessário */
}

.form {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;     /* Aumenta o espaço entre o formulário e a lista */
}

input {
  flex: 1;
  padding: 0.75rem;        /* Aumenta o padding interno para ficar mais bonito */
  border: 1px solid #ccc;
  border-radius: 4px;      /* Arredonda levemente as bordas */
}

button[type="submit"] {
  padding: 0.75rem 1.5rem; /* Aumenta o botão */
  background-color: #4caf50; /* Cor verde para o botão Adicionar */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}

button[type="submit"]:hover {
  background-color: #45a049; /* Efeito hover mais escuro */
}

.task-list {
  list-style: none;
  padding: 0;
}

li {
  display: flex;
  justify-content: space-between;
  align-items: center;    /* Alinha o texto e o botão verticalmente */
  padding: 1rem 0;        /* Aumenta o espaçamento entre as tarefas */
  border-bottom: 1px solid #eee; /* Linha mais sutil */
}

li:last-child {
  border-bottom: none;    /* Remove a linha da última tarefa */
}

span {
  cursor: pointer;
  flex: 1;                /* Faz o texto ocupar o espaço disponível */
}

.completed span {
  text-decoration: line-through;
  color: #888;
}

/* Estilo para o botão Eliminar */
li button {
  padding: 0.5rem 1rem;
  background-color: #f44336; /* Vermelho para eliminar */
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 1rem;
}

li button:hover {
  background-color: #d32f2f;
}
</style>