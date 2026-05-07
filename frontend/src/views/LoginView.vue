<template>
  <main class="min-h-screen bg-[#050816] text-slate-100 overflow-hidden">
    <div class="relative min-h-screen grid lg:grid-cols-[1.15fr_0.85fr]">
      <!-- Background accents -->
      <div class="pointer-events-none absolute inset-0">
        <div class="absolute -top-32 -left-24 h-96 w-96 rounded-full bg-sky-500/10 blur-3xl"></div>
        <div class="absolute bottom-0 right-0 h-96 w-96 rounded-full bg-indigo-500/10 blur-3xl"></div>
        <div class="absolute inset-0 bg-[linear-gradient(to_right,rgba(148,163,184,0.06)_1px,transparent_1px),linear-gradient(to_bottom,rgba(148,163,184,0.06)_1px,transparent_1px)] bg-[size:56px_56px]"></div>
      </div>

      <!-- Left brand panel -->
      <section class="relative hidden lg:flex flex-col justify-between border-r border-white/10 px-12 py-10">
        <div>
          <div class="flex items-center gap-3">
            <div class="flex h-11 w-11 items-center justify-center rounded-2xl bg-sky-500/15 border border-sky-400/30">
              <span class="text-sky-300 font-black">N</span>
            </div>
            <div>
              <h1 class="text-xl font-bold tracking-tight">AI-NIPS</h1>
              <p class="text-xs text-slate-400">Crypto-Ransomware Defense Console</p>
            </div>
          </div>

          <div class="mt-24 max-w-2xl">
            <p class="mb-4 inline-flex rounded-full border border-sky-400/20 bg-sky-400/10 px-4 py-2 text-xs font-medium text-sky-200">
              Network Intrusion Prevention System
            </p>

            <h2 class="text-5xl font-bold leading-tight tracking-tight">
              Monitor threats.
              <span class="block text-sky-300">Block ransomware traffic.</span>
            </h2>

            <p class="mt-6 max-w-xl text-base leading-7 text-slate-400">
              A controlled security dashboard for traffic analysis, alert triage,
              model status, and prevention actions.
            </p>
          </div>
        </div>

        
      </section>

      <!-- Login panel -->
      <section class="relative flex items-center justify-center px-5 py-10">
        <div class="w-full max-w-md">
          <div class="mb-8 lg:hidden">
            <h1 class="text-2xl font-bold">AI-NIPS</h1>
            <p class="text-sm text-slate-400">Crypto-Ransomware Defense </p>
          </div>

          <div class="rounded-[2rem] border border-white/10 bg-slate-900/80 p-7 shadow-2xl shadow-black/30 backdrop-blur-xl">
            <div class="mb-7">
              
              <h2 class="mt-2 text-3xl font-bold tracking-tight text-white">
                Sign in to console
              </h2>
              
            </div>

            <div
              v-if="warningMessage"
              class="mb-4 rounded-2xl border border-yellow-400/30 bg-yellow-400/10 p-4 text-sm text-yellow-300"
            >
              {{ warningMessage }}
            </div>

            <form @submit.prevent="submitLogin" class="space-y-5">
              <div>
                <label class="mb-2 block text-sm font-medium text-slate-300" for="username">
                  Username
                </label>
                <input
                  id="username"
                  v-model.trim="form.username"
                  type="text"
                  required
                  autocomplete="username"
                  placeholder="admin"
                  class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 text-white placeholder:text-slate-600 outline-none transition focus:border-sky-400 focus:ring-4 focus:ring-sky-400/10"
                />
              </div>

              <div>
                <div class="mb-2 flex items-center justify-between">
                  <label class="block text-sm font-medium text-slate-300" for="password">
                    Password
                  </label>
                  
                </div>

                <div class="relative">
                  <input
                    id="password"
                    v-model="form.password"
                    :type="showPassword ? 'text' : 'password'"
                    required
                    autocomplete="current-password"
                    placeholder="••••••••"
                    class="w-full rounded-2xl border border-white/10 bg-slate-950/80 px-4 py-3 pr-24 text-white placeholder:text-slate-600 outline-none transition focus:border-sky-400 focus:ring-4 focus:ring-sky-400/10"
                  />

                  <button
                    type="button"
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 rounded-xl px-3 py-1 text-xs text-slate-400 hover:bg-white/5 hover:text-white"
                  >
                    {{ showPassword ? 'Hide' : 'Show' }}
                  </button>
                </div>
              </div>

              <button
                type="submit"
                :disabled="submitting"
                class="group flex w-full items-center justify-center rounded-2xl bg-sky-400 px-4 py-3 font-semibold text-slate-950 transition hover:bg-sky-300 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <span>{{ submitting ? 'Signing in...' : 'Sign in' }}</span>

              </button>
            </form>

            <p v-if="error" class="mt-4 rounded-2xl border border-red-400/30 bg-red-400/10 p-3 text-sm text-red-300">
              {{ error }}
            </p>

            <div class="mt-6 flex items-center justify-between border-t border-white/10 pt-5 text-xs text-slate-500">
              
              
            </div>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../services/api';

const router = useRouter();

const error = ref('');
const warningMessage = ref('');
const submitting = ref(false);
const showPassword = ref(false);

const form = reactive({
  username: '',
  password: '',
});

onMounted(() => {
  const storedWarning = sessionStorage.getItem('authWarning');

  if (storedWarning) {
    warningMessage.value = storedWarning;
    sessionStorage.removeItem('authWarning');
  }

  localStorage.removeItem('access_token');
  sessionStorage.removeItem('access_token');
});

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

    const token = response.data?.access_token;

    if (!token) {
      error.value = 'No access token received.';
      return;
    }

    localStorage.setItem('access_token', token);
    sessionStorage.removeItem('authWarning');

    await router.push({ name: 'dashboard' });
  } catch (err) {
    console.error('Login error:', err);

    const detail = err.response?.data;

    if (detail?.error) {
      error.value = detail.error;
    } else if (detail?.detail?.error) {
      error.value = detail.detail.error;
    } else if (detail?.message) {
      error.value = detail.message;
    } else {
      error.value = 'Invalid credentials or backend is offline.';
    }
  } finally {
    submitting.value = false;
  }
};
</script>