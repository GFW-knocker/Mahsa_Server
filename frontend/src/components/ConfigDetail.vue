<template>
  <div class="m-4">
    <h2 class="text-xl font-semibold mb-4">Config Detail
      (<span v-if="config && config.is_verified">Verified</span>
      <span v-if="config && !config.is_verified">Pending Verification</span>)
    </h2>
    <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Error</strong>
      <span class="block sm:inline">{{ errorMessage }}</span>
    </div>
    <div v-if="config" class="bg-white shadow p-6 rounded">
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">UUID</label>
        <p class="text-gray-900">{{ config.uuid }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Protocol</label>
        <p class="text-gray-900">{{ config.protocol }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Config Link/URL</label>
        <code class="text-sm text-gray-800" style="overflow-wrap: break-word">
          <div class="group inline-block">
            <span class="blur group-hover:hidden" style="overflow-wrap: break-word">
              {{ config.url }}
            </span>
            <span class="hidden group-hover:inline-block" style="overflow-wrap: break-word">
              {{ config.url }}
            </span>
          </div>
        </code>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Ads URL</label>
        <p class="text-gray-900">{{ config.ads_url }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Created At</label>
        <p class="text-gray-900">{{ config.created_at }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Expired At</label>
        <p class="text-gray-900">{{ config.expired_at }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">XRay Result</label>
        <p class="text-gray-900">{{ config.xray_result }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Last XRay Run</label>
        <p class="text-gray-900">{{ config.last_xray_run }}</p>
      </div>
      <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Reports Count</label>
        <p class="text-gray-900">{{ config.reports_count }}</p>
      </div>
            <div class="mb-4">
        <label class="block text-gray-700 font-bold mb-2">Average Users Rating</label>
        <p class="text-gray-900">{{ config.average_users_rating }}</p>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';

interface Config {
  uuid: string,
  protocol: string;
  url: number;
  ads_url: number;
  is_verified: boolean,
  average_users_rating: number,
  reports_count: number,
  xray_result: any,
  last_xray_run: Date,
  created_at: Date,
  expired_at: Date,
}

export default {
  data() {
    return {
      config: null,
      error: null,
      errorMessage: null
    };
  },
  mounted() {
    this.getConfig();
  },
  methods: {
    async getConfig(): Config {
      try {
        const uuid = this.$route.params.uuid; // Get the UUID parameter from the route
        const response = await axios.get(`/backend/app/config/${uuid}/`); // Replace with your API endpoint

        this.config = response.data;
      } catch (error) {
        this.errorMessage = error.message;
        this.error = true;
        console.error(error);
      }
    },
  },
};
</script>