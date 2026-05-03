<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-950 text-slate-100 px-4">
    <div class="w-full max-w-md bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-xl">
      <h1 class="text-3xl font-bold mb-6 text-white">Login</h1>

      <!-- Warning message (e.g., session expired, forbidden) -->
      <div
        v-if="warningMessage"
        class="mb-4 bg-yellow-500/10 border border-yellow-500/30 text-yellow-400 p-4 rounded-xl"
      >
        ⚠️ {{ warningMessage }}
      </div>

      <!-- Login form -->
      <form @submit.prevent="submitLogin" class="space-y-5">
        <div>
          <label class="block text-slate-300 mb-2" for="username">Username</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            required
            autocomplete="username"
            class="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-sky-500"
          />
        </div>

        <div>
          <label class="block text-slate-300 mb-2" for="password">Password</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            required
            autocomplete="current-password"
            class="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-sky-500"
          />
        </div>

        <button
          type="submit"
          :disabled="submitting"
          class="w-full rounded-2xl bg-sky-500 px-4 py-3 text-sm font-semibold text-slate-950 transition hover:bg-sky-400 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ submitting ? 'Signing in...' : 'Sign in' }}
        </button>
      </form>

      <!-- Error message (login failure) -->
      <p v-if="error" class="mt-4 text-sm text-red-400">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();
const error = ref('');
const warningMessage = ref('');
const submitting = ref(false);

const form = reactive({
  username: '',
  password: '',
});

// --- Check for warning from previous auth failure ---
onMounted(() => {
  const storedWarning = sessionStorage.getItem('authWarning');
  if (storedWarning) {
    warningMessage.value = storedWarning;
    sessionStorage.removeItem('authWarning');
  }
  // Clear any stale token before showing login page
  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
});

// --- Login submission ---
const submitLogin = async () => {
  if (submitting.value) return;

  error.value = '';
  warningMessage.value = '';
  submitting.value = true;

  try {
    const response = await api.post('/api/v1/login', {
      username: form.username,
      password: form.password,
    });

    // Store token using the same key used by other components
    const token = response.data.access_token;
    if (token) {
      localStorage.setItem('access_token', token);
      // Also clear any warning that might have been left
      sessionStorage.removeItem('authWarning');
      await router.push({ name: 'dashboard' });
    } else {
      error.value = 'Login succeeded but no access token received.';
    }
  } catch (err) {
    console.error('Login error:', err);
    // Extract error message from various possible response shapes
    const detail = err.response?.data;
    if (detail?.error) {
      error.value = detail.error;
    } else if (detail?.detail?.error) {
      error.value = detail.detail.error;
    } else if (detail?.message) {
      error.value = detail.message;
    } else if (err.message) {
      error.value = err.message;
    } else {
      error.value = 'Login failed. Please check credentials and try again.';
    }
  } finally {
    submitting.value = false;
  }
};
</script>