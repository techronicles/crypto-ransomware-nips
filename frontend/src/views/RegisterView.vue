<template>
  <section class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p class="text-sm font-medium text-sky-300">
          Admin / User Management
        </p>

        <h1 class="mt-2 text-3xl font-bold tracking-tight text-white">
          Manage Users
        </h1>

        <p class="mt-2 max-w-2xl text-sm text-slate-400">
          Create, view, and manage AI-NIPS console users.
        </p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row">
        <button
          @click="refreshUsers"
          :disabled="fetchingUsers"
          class="inline-flex items-center justify-center rounded-2xl border border-sky-400/20 bg-sky-400/10 px-5 py-3 text-sm font-semibold text-sky-300 transition hover:bg-sky-400 hover:text-slate-950 disabled:opacity-60"
        >
          {{ fetchingUsers ? 'Refreshing users...' : 'Refresh Users' }}
        </button>

        <RouterLink
          to="/dashboard"
          class="inline-flex items-center justify-center rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-slate-200 transition hover:bg-white/[0.08]"
        >
          Back to Dashboard
        </RouterLink>
      </div>
    </div>

    <!-- Create User Form -->
    <div class="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
      <div class="mb-5">
        <h2 class="text-xl font-bold text-white">
          Create User
        </h2>

        <p class="mt-1 text-sm text-slate-400">
          Add a new account. Activation can be controlled by the administrator.
        </p>
      </div>

      <form
        @submit.prevent="submitRegister"
        class="grid grid-cols-1 gap-5 md:grid-cols-2"
      >
        <!-- Full Name -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">
            Full Name
          </label>

          <input
            v-model.trim="form.full_name"
            type="text"
            required
            placeholder="e.g. Security Analyst"
            class="input-field"
          />
        </div>

        <!-- Username -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">
            Username
          </label>

          <input
            v-model.trim="form.username"
            type="text"
            required
            placeholder="e.g. analyst01"
            class="input-field"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">
            Email
          </label>

          <input
            v-model.trim="form.email"
            type="email"
            required
            placeholder="analyst@example.com"
            class="input-field"
          />
        </div>

        <!-- Role -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">
            Role
          </label>

          <select
            v-model="form.role"
            required
            class="input-field"
          >
            <option value="admin">Admin</option>
            <option value="analyst">Analyst</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>

        <!-- Password -->
        <div class="md:col-span-2">
          <label class="mb-2 block text-sm font-medium text-slate-300">
            Temporary Password
          </label>

          <div class="relative">
            <input
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              minlength="6"
              placeholder="Minimum 6 characters"
              class="input-field pr-24"
            />

            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-3 top-1/2 -translate-y-1/2 rounded-xl px-3 py-1 text-xs text-slate-400 transition hover:bg-white/5 hover:text-white"
            >
              {{ showPassword ? 'Hide' : 'Show' }}
            </button>
          </div>
        </div>

        <!-- Activation -->
        <div class="md:col-span-2 rounded-2xl border border-yellow-400/20 bg-yellow-400/10 p-4">
          <div class="flex items-start gap-3">
            <input
              id="actived"
              v-model="form.actived"
              type="checkbox"
              class="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-950"
            />

            <label for="actived" class="text-sm text-slate-300">
              Activate user immediately
              <span class="block text-xs text-slate-500">
                If unchecked, account remains inactive until approved.
              </span>
            </label>
          </div>
        </div>

        <!-- Actions -->
        <div class="md:col-span-2 flex flex-col gap-3 sm:flex-row">
          <button
            type="submit"
            :disabled="submitting"
            class="flex-1 rounded-2xl bg-green-700 px-4 py-3 font-semibold text-white transition hover:bg-green-600 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {{ submitting ? 'Creating user...' : 'Create User' }}
          </button>

          <button
            type="button"
            @click="resetForm"
            class="flex-1 rounded-2xl border border-white/10 bg-white/[0.04] px-4 py-3 font-semibold text-slate-200 transition hover:bg-white/[0.08]"
          >
            Clear Form
          </button>
        </div>
      </form>

      <div
        v-if="success"
        class="mt-5 rounded-2xl border border-emerald-400/30 bg-emerald-400/10 p-4 text-sm text-emerald-300"
      >
        {{ success }}
      </div>

      <div
        v-if="error"
        class="mt-5 rounded-2xl border border-red-400/30 bg-red-400/10 p-4 text-sm text-red-300"
      >
        {{ error }}
      </div>
    </div>

    <!-- Users Table -->
    <div class="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
      <div class="mb-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 class="text-xl font-bold text-white">
            System Users
          </h2>

          <p class="mt-1 text-sm text-slate-400">
            Users are loaded automatically from the backend user-management API.
          </p>
        </div>

        <span class="rounded-2xl border border-sky-400/20 bg-sky-400/10 px-4 py-2 text-sm text-sky-300">
          {{ pagination.total }} users
        </span>
      </div>

      <div v-if="fetchingUsers && users.length === 0" class="text-sm text-slate-400">
        Loading users...
      </div>

      <div
        v-else-if="users.length === 0"
        class="rounded-2xl border border-white/10 p-6 text-center text-slate-400"
      >
        No users found.
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-slate-900/80 text-slate-300">
            <tr>
              <th class="p-4 text-left">Username</th>
              <th class="p-4 text-left">Full Name</th>
              <th class="p-4 text-left">Email</th>
              <th class="p-4 text-left">Role</th>
              <th class="p-4 text-left">Status</th>
              <th class="p-4 text-left">Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="user in users"
              :key="user.username"
              class="border-t border-white/10 hover:bg-white/[0.03]"
            >
              <td class="p-4 font-medium text-slate-200">
                {{ user.username || '—' }}
              </td>

              <td class="p-4">
                {{ user.full_name || '—' }}
              </td>

              <td class="p-4">
                {{ user.email || '—' }}
              </td>

              <td class="p-4">
                <span class="rounded-full bg-sky-500/20 px-3 py-1 text-xs text-sky-300">
                  {{ user.role || '—' }}
                </span>
              </td>

              <td class="p-4">
                <span
                  class="rounded-full px-3 py-1 text-xs font-medium"
                  :class="isUserActive(user)
                    ? 'bg-emerald-500/20 text-emerald-300'
                    : 'bg-red-500/20 text-red-300'"
                >
                  {{ isUserActive(user) ? 'Active' : 'Inactive' }}
                </span>
              </td>

              <td class="p-4">
                <button
                  @click="toggleUserStatus(user)"
                  :disabled="updatingUsername === user.username"
                  class="rounded-xl border px-3 py-2 text-xs font-medium transition disabled:opacity-50"
                  :class="isUserActive(user)
                    ? 'border-red-400/20 bg-red-400/10 text-red-300 hover:bg-red-500 hover:text-white'
                    : 'border-emerald-400/20 bg-emerald-400/10 text-emerald-300 hover:bg-emerald-500 hover:text-white'"
                >
                  {{
                    updatingUsername === user.username
                      ? 'Updating...'
                      : isUserActive(user)
                        ? 'Disable'
                        : 'Activate'
                  }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Controls -->
        <div
          v-if="pagination.pages > 1"
          class="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between"
        >
          <p class="text-sm text-slate-400">
            Showing {{ users.length }} users on page
            {{ pagination.page }} of {{ pagination.pages }}
            · Total {{ pagination.total }}
          </p>

          <div class="flex items-center gap-2">
            <button
              @click="goToPage(pagination.page - 1)"
              :disabled="pagination.page === 1 || fetchingUsers"
              class="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 transition hover:bg-white/[0.08] disabled:opacity-40"
            >
              Previous
            </button>

            <button
              v-for="page in visiblePages"
              :key="page"
              @click="goToPage(page)"
              :disabled="fetchingUsers"
              :class="[
                'rounded-xl border px-4 py-2 text-sm transition disabled:opacity-40',
                page === pagination.page
                  ? 'border-sky-400/30 bg-sky-400 text-slate-950'
                  : 'border-white/10 bg-white/[0.04] text-slate-300 hover:bg-white/[0.08]'
              ]"
            >
              {{ page }}
            </button>

            <button
              @click="goToPage(pagination.page + 1)"
              :disabled="pagination.page === pagination.pages || fetchingUsers"
              class="rounded-xl border border-white/10 bg-white/[0.04] px-4 py-2 text-sm text-slate-300 transition hover:bg-white/[0.08] disabled:opacity-40"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue';
import api from '../services/api';

const submitting = ref(false);
const fetchingUsers = ref(false);
const updatingUsername = ref('');
const showPassword = ref(false);

const error = ref('');
const success = ref('');
const users = ref([]);

const currentPage = ref(1);
const itemsPerPage = ref(10);

const pagination = ref({
  page: 1,
  limit: 10,
  total: 0,
  pages: 1,
});

const form = reactive({
  username: '',
  password: '',
  full_name: '',
  email: '',
  role: 'analyst',
  actived: false,
});

const visiblePages = computed(() => {
  const total = pagination.value.pages || 1;
  const current = pagination.value.page || 1;
  const range = [];

  const start = Math.max(1, current - 1);
  const end = Math.min(total, current + 1);

  for (let page = start; page <= end; page += 1) {
    range.push(page);
  }

  return range;
});

const resetForm = () => {
  Object.assign(form, {
    username: '',
    password: '',
    full_name: '',
    email: '',
    role: 'analyst',
    actived: false,
  });

  error.value = '';
  success.value = '';
};

const getErrorMessage = (err) => {
  const detail = err.response?.data;

  if (detail?.error) return detail.error;
  if (detail?.detail?.error) return detail.detail.error;
  if (typeof detail?.detail === 'string') return detail.detail;
  if (detail?.message) return detail.message;

  return 'Request failed. Please verify the details and try again.';
};

const normalizeUser = (user) => ({
  username: user.username,
  full_name: user.full_name,
  email: user.email,
  role: user.role,
  is_active: user.is_active ?? user.active ?? user.actived ?? false,
});

const isUserActive = (user) => {
  return Boolean(user.is_active ?? user.active ?? user.actived);
};

const extractUsersPayload = (responseData) => {
  if (Array.isArray(responseData)) {
    return {
      users: responseData,
      pagination: {
        page: currentPage.value,
        limit: itemsPerPage.value,
        total: responseData.length,
        pages: 1,
      },
    };
  }

  const usersData =
    responseData?.data ||
    responseData?.users ||
    responseData?.results ||
    [];

  return {
    users: Array.isArray(usersData) ? usersData : [],
    pagination: responseData?.pagination || {
      page: currentPage.value,
      limit: itemsPerPage.value,
      total: Array.isArray(usersData) ? usersData.length : 0,
      pages: 1,
    },
  };
};

const fetchUsers = async () => {
  fetchingUsers.value = true;
  error.value = '';
  success.value = '';

  try {
    const response = await api.get('/api/v1/fetch_users', {
      params: {
        page: currentPage.value,
        limit: itemsPerPage.value,
      },
    });

    const payload = extractUsersPayload(response.data);

    users.value = payload.users.map(normalizeUser);
    pagination.value = payload.pagination;

    currentPage.value = pagination.value.page || currentPage.value;
  } catch (err) {
    console.error('Fetch users error:', err);
    error.value = getErrorMessage(err);
  } finally {
    fetchingUsers.value = false;
  }
};

const refreshUsers = async () => {
  currentPage.value = 1;
  await fetchUsers();
};

const goToPage = async (page) => {
  if (
    page < 1 ||
    page > pagination.value.pages ||
    page === pagination.value.page
  ) {
    return;
  }

  currentPage.value = page;
  await fetchUsers();
};

const submitRegister = async () => {
  if (submitting.value) return;

  error.value = '';
  success.value = '';
  submitting.value = true;

  try {
    await api.post('/api/v1/register_user', {
      username: form.username,
      password: form.password,
      full_name: form.full_name,
      email: form.email,
      role: form.role,
      actived: form.actived,
    });

    resetForm();
    success.value = 'User account created successfully.';

    currentPage.value = 1;
    await fetchUsers();
  } catch (err) {
    console.error('Registration error:', err);
    error.value = getErrorMessage(err);
  } finally {
    submitting.value = false;
  }
};

const toggleUserStatus = async (user) => {
  const username = user.username;

  if (!username) return;

  updatingUsername.value = username;
  error.value = '';
  success.value = '';

  try {
    const nextStatus = !isUserActive(user);

    await api.put('/api/v1/edit_user', {
      username,
      is_active: nextStatus,
    });

    success.value = `User ${username} ${nextStatus ? 'activated' : 'disabled'} successfully.`;

    users.value = users.value.map((item) =>
      item.username === username
        ? { ...item, is_active: nextStatus }
        : item
    );
  } catch (err) {
    console.error('Update user error:', err);
    error.value = getErrorMessage(err);
  } finally {
    updatingUsername.value = '';
  }
};

onMounted(() => {
  fetchUsers();
});
</script>

<style scoped>
.input-field {
  width: 100%;
  border-radius: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(2, 6, 23, 0.8);
  padding: 0.75rem 1rem;
  color: white;
  outline: none;
  transition: 0.2s ease;
}

.input-field:focus {
  border-color: rgb(56, 189, 248);
  box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.1);
}
</style>