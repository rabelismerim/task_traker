<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import api from '../services/api';

const emit = defineEmits(['logout']);

// Estados de dados
const tasks = ref([]);
const title = ref('');
const priority = ref('Média');
const category = ref('');
const dueDate = ref('');

// Filtros
const search = ref('');
const filterStatus = ref('');
const filterPriority = ref('');

// Controles de Paginação
const currentPage = ref(1);
const itemsPerPage = ref(5); // Defina quantas tarefas exibir por página

// Estado de Edição
const editingTaskId = ref(null);

// Feedback
const isFetching = ref(false);
const isCreating = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

const handleApiError = (error, defaultMsg) => {
  if (error.response && error.response.data) {
    const data = error.response.data;
    if (typeof data === 'object') {
      const messages = Object.entries(data).map(([field, errs]) => {
        const detail = Array.isArray(errs) ? errs.join(', ') : errs;
        return `${field}: ${detail}`;
      });
      return messages.join(' | ');
    }
  }
  return defaultMsg;
};

const fetchTasks = async () => {
  isFetching.value = true;
  try {
    const response = await api.get('tasks/');
    // Se o backend usar paginação nativa do Django, os dados virão em response.data.results
    tasks.value = Array.isArray(response.data) ? response.data : (response.data.results || []);
  } catch (error) {
    errorMessage.value = handleApiError(error, 'Erro ao carregar a lista de tarefas.');
  } finally {
    isFetching.value = false;
  }
};

// --- LÓGICA DE FILTRAGEM E PAGINAÇÃO NO FRONTEND ---

const filteredTasks = computed(() => {
  return tasks.value.filter(task => {
    const matchesSearch = !search.value || 
      task.title.toLowerCase().includes(search.value.toLowerCase()) ||
      (task.category && task.category.toLowerCase().includes(search.value.toLowerCase()));

    const matchesStatus = !filterStatus.value || 
      (filterStatus.value === 'completed' && task.completed) ||
      (filterStatus.value === 'pending' && !task.completed);

    const mappedPriority = task.priority ? task.priority.toLowerCase() : '';
    const selectedPriority = filterPriority.value.toLowerCase();
    const matchesPriority = !filterPriority.value || mappedPriority.includes(selectedPriority);

    return matchesSearch && matchesStatus && matchesPriority;
  });
});

// Reseta para a página 1 se o usuário mudar algum filtro ou busca
watch([search, filterStatus, filterPriority], () => {
  currentPage.value = 1;
});

const totalPages = computed(() => {
  return Math.ceil(filteredTasks.value.length / itemsPerPage.value) || 1;
});

const paginatedTasks = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredTasks.value.slice(start, end);
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};

const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};

// --- OPERAÇÕES CRUD ---

const priorityMap = { 'Baixa': 'low', 'Média': 'medium', 'Alta': 'high' };
const priorityUnmap = { 'low': 'Baixa', 'medium': 'Média', 'high': 'Alta' };

const saveTask = async () => {
  if (!title.value.trim()) return;

  isCreating.value = true;
  errorMessage.value = '';
  successMessage.value = '';

  const payload = {
    title: title.value,
    priority: priorityMap[priority.value] || 'medium',
    category: category.value || null,
    due_date: dueDate.value ? dueDate.value : null
  };

  try {
    if (editingTaskId.value) {
      await api.put(`tasks/${editingTaskId.value}/`, payload);
      successMessage.value = 'Tarefa atualizada com sucesso!';
    } else {
      await api.post('tasks/', payload);
      successMessage.value = 'Tarefa criada com sucesso!';
    }

    cancelEdit();
    await fetchTasks();

    setTimeout(() => { successMessage.value = ''; }, 3000);
  } catch (error) {
    errorMessage.value = handleApiError(error, 'Erro ao salvar a tarefa.');
  } finally {
    isCreating.value = false;
  }
};

const startEdit = (task) => {
  editingTaskId.value = task.id;
  title.value = task.title;
  priority.value = priorityUnmap[task.priority] || task.priority || 'Média';
  category.value = task.category || '';
  dueDate.value = task.due_date || '';
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const cancelEdit = () => {
  editingTaskId.value = null;
  title.value = '';
  category.value = '';
  dueDate.value = '';
  priority.value = 'Média';
};

const deleteTask = async (id) => {
  if (!confirm('Tem certeza que deseja remover esta tarefa?')) return;

  try {
    await api.delete(`tasks/${id}/`);
    successMessage.value = 'Tarefa removida com sucesso!';
    await fetchTasks();
    setTimeout(() => { successMessage.value = ''; }, 3000);
  } catch (error) {
    errorMessage.value = handleApiError(error, 'Erro ao excluir a tarefa.');
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('refreshToken');
  emit('logout');
};

onMounted(() => {
  fetchTasks();
});
</script>

<template>
  <div class="dashboard-container">
    <header class="navbar">
      <div class="nav-brand">
        <div class="brand-icon">
          <svg xmlns="http://www.w3.org/2000/svg" class="icon-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2>Task Tracker</h2>
      </div>
      <button @click="handleLogout" class="btn-logout">Sair</button>
    </header>

    <main class="main-content">
      <!-- Banners de Notificação -->
      <transition name="fade">
        <div v-if="errorMessage" class="alert-banner alert-error">
          <span>⚠️ {{ errorMessage }}</span>
          <button @click="errorMessage = ''" class="btn-close">&times;</button>
        </div>
      </transition>

      <transition name="fade">
        <div v-if="successMessage" class="alert-banner alert-success">
          <span>✅ {{ successMessage }}</span>
          <button @click="successMessage = ''" class="btn-close">&times;</button>
        </div>
      </transition>

      <!-- Formulário -->
      <section class="card-section">
        <h3>{{ editingTaskId ? 'Editar Tarefa' : 'Nova Tarefa' }}</h3>
        <form @submit.prevent="saveTask" class="task-form">
          <div class="form-grid">
            <input v-model="title" type="text" placeholder="O que precisa de ser feito? *" required :disabled="isCreating" class="input-field" />
            
            <select v-model="priority" :disabled="isCreating" class="input-field">
              <option value="Baixa">Baixa Prioridade</option>
              <option value="Média">Média Prioridade</option>
              <option value="Alta">Alta Prioridade</option>
            </select>

            <input v-model="category" type="text" placeholder="Categoria (ex: Trabalho)" :disabled="isCreating" class="input-field" />
            <input v-model="dueDate" type="date" :disabled="isCreating" class="input-field" />
          </div>

          <div class="form-actions">
            <button type="submit" :disabled="isCreating" class="btn-primary">
              <span v-if="isCreating" class="spinner"></span>
              <span>{{ isCreating ? 'Salvando...' : (editingTaskId ? 'Atualizar Tarefa' : 'Criar Tarefa') }}</span>
            </button>
            <button v-if="editingTaskId" type="button" @click="cancelEdit" class="btn-secondary">
              Cancelar
            </button>
          </div>
        </form>
      </section>

      <!-- Tabela de Tarefas com Paginação -->
      <section class="card-section">
        <div class="section-header">
          <h3>Suas Tarefas</h3>
          <div class="filters-container">
            <input v-model="search" type="text" placeholder="Buscar..." class="input-field input-search" />
            <select v-model="filterStatus" class="input-field">
              <option value="">Todos Status</option>
              <option value="pending">Pendente</option>
              <option value="completed">Concluída</option>
            </select>
            <select v-model="filterPriority" class="input-field">
              <option value="">Todas Prioridades</option>
              <option value="Baixa">Baixa</option>
              <option value="Média">Média</option>
              <option value="Alta">Alta</option>
            </select>
          </div>
        </div>

        <div class="table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Status</th>
                <th>Tarefa</th>
                <th>Prioridade</th>
                <th>Categoria</th>
                <th>Vencimento</th>
                <th class="text-right">Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="isFetching">
                <td colspan="6" class="state-message">
                  <div class="loading-state">
                    <span class="spinner dark"></span>
                    <span>Carregando tarefas...</span>
                  </div>
                </td>
              </tr>
              <tr v-else-if="paginatedTasks.length === 0">
                <td colspan="6" class="state-message">Nenhuma tarefa encontrada.</td>
              </tr>
              <tr v-else v-for="task in paginatedTasks" :key="task.id">
                <td>
                  <span class="status-badge" :class="task.completed ? 'status-completed' : 'status-pending'">
                    {{ task.completed ? 'Concluída' : 'Pendente' }}
                  </span>
                </td>
                <td class="font-medium">{{ task.title }}</td>
                <td>
                  <span class="priority-badge" :class="task.priority ? task.priority.toLowerCase() : ''">
                    {{ task.priority || 'Média' }}
                  </span>
                </td>
                <td>{{ task.category || '-' }}</td>
                <td>{{ task.due_date || '-' }}</td>
                <td class="text-right">
                  <div class="action-buttons">
                    <button @click="startEdit(task)" class="btn-icon edit" title="Editar Tarefa">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="icon-action">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button @click="deleteTask(task.id)" class="btn-icon delete" title="Remover Tarefa">
                      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="icon-action">
                        <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Controles de Paginação -->
        <div v-if="filteredTasks.length > 0" class="pagination-footer">
          <div class="pagination-info">
            Mostrando <strong>{{ paginatedTasks.length }}</strong> de <strong>{{ filteredTasks.length }}</strong> tarefas
          </div>
          
          <div class="pagination-controls">
            <button 
              @click="prevPage" 
              :disabled="currentPage === 1" 
              class="btn-pagination"
              title="Página Anterior"
            >
              &laquo; Anterior
            </button>
            
            <span class="page-indicator">Página {{ currentPage }} de {{ totalPages }}</span>
            
            <button 
              @click="nextPage" 
              :disabled="currentPage === totalPages" 
              class="btn-pagination"
              title="Próxima Página"
            >
              Próxima &raquo;
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
/* Estilos Base */
.dashboard-container { min-height: 100vh; background-color: #f8fafc; font-family: system-ui, -apple-system, sans-serif; color: #334155; }
.navbar { background-color: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; }
.nav-brand { display: flex; align-items: center; gap: 0.75rem; }
.brand-icon { width: 36px; height: 36px; background-color: #2563eb; color: #ffffff; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.icon-svg { width: 20px; height: 20px; }
.nav-brand h2 { font-size: 1.25rem; font-weight: 700; color: #0f172a; margin: 0; }
.btn-logout { padding: 0.5rem 1rem; background-color: #f1f5f9; color: #475569; border: 1px solid #cbd5e1; border-radius: 8px; font-weight: 600; font-size: 0.875rem; cursor: pointer; }

.main-content { max-width: 1100px; margin: 2rem auto; padding: 0 1.5rem; display: flex; flex-direction: column; gap: 1.5rem; }

/* Banners */
.alert-banner { padding: 0.875rem 1.25rem; border-radius: 10px; font-size: 0.875rem; font-weight: 500; display: flex; align-items: center; justify-content: space-between; }
.alert-error { background-color: #fef2f2; border: 1px solid #fecaca; color: #991b1b; }
.alert-success { background-color: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
.btn-close { background: none; border: none; font-size: 1.25rem; cursor: pointer; color: inherit; }

.card-section { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 1.5rem 2rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03); }
.card-section h3 { margin: 0 0 1.25rem 0; font-size: 1.125rem; color: #0f172a; }

.task-form { display: flex; flex-direction: column; gap: 1.25rem; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; }
.input-field { padding: 0.65rem 0.85rem; font-size: 0.875rem; background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px; outline: none; }

.form-actions { display: flex; gap: 0.75rem; }
.btn-primary { display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.65rem 1.25rem; background-color: #2563eb; color: #ffffff; font-weight: 600; font-size: 0.875rem; border: none; border-radius: 8px; cursor: pointer; }
.btn-secondary { padding: 0.65rem 1.25rem; background-color: #f1f5f9; color: #475569; font-weight: 600; font-size: 0.875rem; border: 1px solid #cbd5e1; border-radius: 8px; cursor: pointer; }

/* Spinners */
.spinner { width: 14px; height: 14px; border: 2px solid rgba(255, 255, 255, 0.3); border-top-color: #ffffff; border-radius: 50%; animation: spin 0.8s linear infinite; }
.spinner.dark { border: 2px solid rgba(0, 0, 0, 0.1); border-top-color: #2563eb; width: 18px; height: 18px; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Tabela e Filtros */
.section-header { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; margin-bottom: 1.25rem; }
.filters-container { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 0.875rem; }
.data-table th { background-color: #f8fafc; color: #64748b; font-weight: 600; padding: 0.75rem 1rem; border-bottom: 1px solid #e2e8f0; text-transform: uppercase; font-size: 0.75rem; }
.data-table td { padding: 1rem; border-bottom: 1px solid #f1f5f9; }
.state-message { text-align: center; color: #94a3b8; padding: 2.5rem !important; }
.loading-state { display: flex; align-items: center; justify-content: center; gap: 0.5rem; color: #475569; }
.text-right { text-align: right; }
.font-medium { font-weight: 500; color: #0f172a; }

/* Badges */
.status-badge { display: inline-block; padding: 0.25rem 0.6rem; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; }
.status-completed { background-color: #dcfce7; color: #166534; }
.status-pending { background-color: #fef3c7; color: #92400e; }
.priority-badge { font-weight: 600; font-size: 0.8125rem; }
.priority-badge.high, .priority-badge.alta { color: #dc2626; }
.priority-badge.medium, .priority-badge.media { color: #d97706; }
.priority-badge.low, .priority-badge.baixa { color: #16a34a; }

/* Botões de Ação */
.action-buttons { display: flex; justify-content: flex-end; gap: 0.5rem; }
.btn-icon { background: transparent; border: none; padding: 0.35rem; border-radius: 6px; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; transition: background-color 0.2s ease; }
.icon-action { width: 18px; height: 18px; }
.btn-icon.edit { color: #2563eb; }
.btn-icon.edit:hover { background-color: #eff6ff; }
.btn-icon.delete { color: #dc2626; }
.btn-icon.delete:hover { background-color: #fef2f2; }

/* --- ESTILOS DA PAGINAÇÃO --- */
.pagination-footer { display: flex; justify-content: space-between; align-items: center; margin-top: 1.25rem; padding-top: 1rem; border-top: 1px solid #e2e8f0; flex-wrap: wrap; gap: 1rem; }
.pagination-info { font-size: 0.875rem; color: #64748b; }
.pagination-controls { display: flex; align-items: center; gap: 0.75rem; }
.page-indicator { font-size: 0.875rem; font-weight: 500; color: #475569; }
.btn-pagination { padding: 0.4rem 0.85rem; font-size: 0.875rem; font-weight: 500; background-color: #ffffff; border: 1px solid #cbd5e1; color: #334155; border-radius: 6px; cursor: pointer; transition: all 0.2s ease; }
.btn-pagination:hover:not(:disabled) { background-color: #f1f5f9; color: #0f172a; border-color: #94a3b8; }
.btn-pagination:disabled { opacity: 0.5; cursor: not-allowed; }

/* Animações */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }
</style>