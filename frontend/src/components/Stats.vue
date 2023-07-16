<template>
  <div class="max-w-lg mx-auto m-4">
    <div v-if="stats" class="bg-white shadow p-6 rounded">
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Total Free Configs:</label>
        <p class="text-gray-900">{{ stats.total_configs }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Total Reports:</label>
        <p class="text-gray-900">{{ stats.total_reports }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';

interface Stats {
  total_configs: number,
  total_reports: number
}

export default {
  data() {
    return {
      stats: null
    };
  },
  mounted() {
    this.getStats();
  },
  methods: {
    async getStats(): Stats {
      try {
        const response = await axios.get(`/backend/app/config/stats/`);
        this.stats = response.data;
      } catch (error) {
        this.errorMessage = error.message;
        this.error = true;
        console.error(error);
      }
    },
  },
};
</script>