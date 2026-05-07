<template>
  <section class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col gap-3 lg:flex-row lg:items-center lg:justify-between">
      <div>
        <p class="text-sm font-medium text-sky-300">Admin / User Management</p>
        <h1 class="mt-2 text-3xl font-bold tracking-tight text-white">Add New User</h1>
        <p class="mt-2 max-w-2xl text-sm text-slate-400">
          Create a user account for AI-NIPS console access.
        </p>
      </div>
      <RouterLink
        to="/dashboard"
        class="inline-flex items-center justify-center rounded-2xl border border-white/10 bg-white/[0.04] px-5 py-3 text-sm font-semibold text-slate-200 transition hover:bg-white/[0.08]"
      >
        Back to Dashboard
      </RouterLink>
    </div>

    <!-- Endpoint not yet available warning -->
    <div
      v-if="endpointUnavailable"
      class="rounded-2xl border border-yellow-400/30 bg-yellow-400/10 p-4 text-sm text-yellow-300"
    >
      ⚠️ The <strong>/register_user</strong> endpoint is not yet available on the backend.
      Contact Samoh to confirm when it's ready.
    </div>

    <!-- Form Card -->
    <div class="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
      <form @submit.prevent="submitRegister" class="grid grid-cols-1 gap-5 md:grid-cols-2">
        <!-- Full Name -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">Full Name</label>
          <input v-model.trim="form.full_name" type="text" required placeholder="e.g. Security Analyst" class="input-field" />
        </div>

        <!-- Username -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">Username</label>
          <input v-model.trim="form.username" type="text" required placeholder="e.g. analyst01" class="input-field" />
        </div>

        <!-- Email -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">Email</label>
          <input v-model.trim="form.email" type="email" required placeholder="analyst@example.com" class="input-field" />
        </div>

        <!-- Role -->
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-300">Role</label>
          <select v-model="form.role" required class="input-field">
            <option value="admin">Admin</option>
            <option value="analyst">Analyst</option>
            <option value="viewer">Viewer</option>
          </select>
        </div>

        <!-- Password -->
        <div class="md:col-span-2">
          <label class="mb-2 block text-sm font-medium text-slate-300">Temporary Password</label>
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
            <input id="actived" v-model="form.actived" type="checkbox" class="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-950" />
            <label for="actived" class="text-sm text-slate-300">
              Activate user immediately
              <span class="block text-xs text-slate-500">If unchecked, account remains inactive until approved.</span>
            </label>
          </div>
        </div>

        <!-- Actions -->
        <div class="md:col-span-2 flex flex-col gap-3 sm:flex-row">
          <button
            type="submit"
            :disabled="submitting"
            class="flex-1 rounded-2xl bg-green-700 px-4 py-3 font-semibold text-white-950 transition hover:bg-green-600 disabled:cursor-not-allowed disabled:opacity-60"
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

      <div v-if="success" class="mt-5 rounded-2xl border border-emerald-400/30 bg-emerald-400/10 p-4 text-sm text-emerald-300">
        {{ success }}
      </div>
      <div v-if="error" class="mt-5 rounded-2xl border border-red-400/30 bg-red-400/10 p-4 text-sm text-red-300">
        {{ error }}
      </div>
    </div>

    
  </section>
</template>

<script setup>
import { reactive, ref } from 'vue';
import api from '../services/api';

const submitting = ref(false);
const showPassword = ref(false);
const error = ref('');
const success = ref('');
const endpointUnavailable = ref(false);

const form = reactive({
  username: '',
  password: '',
  full_name: '',
  email: '',
  role: 'analyst',
  actived: false,
});

const resetForm = () => {
  Object.assign(form, { username: '', password: '', full_name: '', email: '', role: 'analyst', actived: false });
  error.value = '';
  success.value = '';
};

const getErrorMessage = (err) => {
  if (err.response?.status === 404) {
    endpointUnavailable.value = true;
    return 'Endpoint /register_user not found. Backend may not have implemented it yet.';
  }
  const detail = err.response?.data;
  if (detail?.error) return detail.error;
  if (detail?.detail?.error) return detail.detail.error;
  if (typeof detail?.detail === 'string') return detail.detail;
  if (detail?.message) return detail.message;
  return 'Failed to create user. Please verify the details and try again.';
};

const submitRegister = async () => {
  if (submitting.value) return;
  error.value = '';
  success.value = '';
  endpointUnavailable.value = false;
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
    success.value = 'User account created successfully.';
    resetForm();
  } catch (err) {
    console.error('Registration error:', err);
    error.value = getErrorMessage(err);
  } finally {
    submitting.value = false;
  }
};
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