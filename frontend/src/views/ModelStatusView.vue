<template>
  <section>
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-white">ML Model Status</h2>
      <p class="text-slate-400">
        Detection model performance and deployment status
      </p>
    </div>

    <div v-if="loading" class="text-slate-400">
      Loading model status...
    </div>

    <div
      v-else-if="error"
      class="bg-red-500/10 border border-red-500/30 text-red-400 p-4 rounded-xl"
    >
      {{ error }}
    </div>

    <div v-else>
      <div class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-6">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Accuracy</p>
          <h3 class="text-3xl font-bold mt-2 text-green-400">
            {{ model.accuracy }}%
          </h3>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Precision</p>
          <h3 class="text-3xl font-bold mt-2">
            {{ model.precision }}%
          </h3>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">Recall</p>
          <h3 class="text-3xl font-bold mt-2">
            {{ model.recall }}%
          </h3>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5">
          <p class="text-slate-400 text-sm">F1 Score</p>
          <h3 class="text-3xl font-bold mt-2">
            {{ model.f1Score }}%
          </h3>
        </div>
      </div>

      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-6">
        <h3 class="text-xl font-bold mb-5">Current Model Information</h3>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <InfoRow label="Model Name" :value="model.modelName" />
          <InfoRow label="Version" :value="model.version" />
          <InfoRow label="Dataset" :value="model.dataset" />

          <div class="flex justify-between border-b border-slate-800 pb-3">
            <span class="text-slate-400">Status</span>
            <span class="text-green-400">{{ model.status }}</span>
          </div>

          <InfoRow label="Last Trained" :value="model.lastTrained" />

          <div class="flex justify-between border-b border-slate-800 pb-3">
            <span class="text-slate-400">Prediction Mode</span>
            <span class="text-yellow-400">{{ model.predictionMode }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { defineComponent, h, onMounted, ref } from "vue";
import api from "../services/api";

const loading = ref(true);
const error = ref("");

const model = ref({
  modelName: "",
  version: "",
  dataset: "",
  accuracy: 0,
  precision: 0,
  recall: 0,
  f1Score: 0,
  lastTrained: "",
  status: "",
  predictionMode: "",
});

const InfoRow = defineComponent({
  props: {
    label: String,
    value: [String, Number],
  },
  setup(props) {
    return () =>
      h("div", { class: "flex justify-between border-b border-slate-800 pb-3" }, [
        h("span", { class: "text-slate-400" }, props.label),
        h("span", null, props.value),
      ]);
  },
});

const loadModelStatus = async () => {
  try {
    loading.value = true;
    error.value = "";

    const response = await api.get("/api/model/status");
    model.value = response.data;
  } catch (err) {
    error.value = "Failed to fetch model status. Make sure backend is running.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(loadModelStatus);
</script>