<template>
  <div class="max-w-md mx-auto bg-white p-6 shadow-md rounded-md mt-4">
    <h2 class="text-xl font-semibold mb-4">Config Form</h2>
    <form v-if="!submitted" @submit.prevent="handleSubmit">
      <div class="mb-4">
        <label for="url" class="block text-gray-700 font-medium">Config URL/Link</label>
        <input type="text" id="url" v-model="form.url" required
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        <ul v-if="errors.url">
          <li class="bg-red-500 p-2 text-white mt-1 rounded-md" v-for="item in errors.url">{{ item }}</li>
        </ul>
      </div>
      <div class="mb-4">
        <label for="url" class="block text-gray-700 font-medium">Ads URL</label>
        <input type="text" id="ads" v-model="form.ads_url" required
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        <ul v-if="errors.ads_url">
          <li class="bg-red-500 p-2 text-white mt-1 rounded-md" v-for="item in errors.ads_url">{{ item }}</li>
        </ul>
      </div>

      <div class="mb-4">
        <label for="expired_at" class="block text-gray-700 font-medium">Expired At</label>
        <input type="date" id="expired_at" v-model="form.expired_at" required :min="minDate"
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        <ul v-if="errors.expired_at">
          <li class="bg-red-500 p-2 text-white mt-1 rounded-md" v-for="item in errors.expired_at">{{ item }}</li>
        </ul>
      </div>

      <div class="mb-4">
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" value="" class="sr-only peer" v-model="form.use_fragment">
          <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
          <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">Use Fragment</span>
        </label>
      </div>

      <div v-if="form.use_fragment" class="mb-4">
        <label for="num_fragment" class="block text-gray-700 font-medium">Fragment Number:</label>
        <input type="number" max="100" min="5" id="num_fragment" v-model="form.num_fragment"
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        <ul v-if="errors.num_fragment">
          <li class="bg-red-500 p-2 text-white mt-1 rounded-md" v-for="item in errors.num_fragment">{{ item }}</li>
        </ul>
      </div>

      <div class="mb-4">
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" value="" class="sr-only peer" v-model="form.use_cdn">
          <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
          <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">Use CDN</span>
        </label>
      </div>

      <div class="mb-4">
        <label class="relative inline-flex items-center cursor-pointer">
          <input type="checkbox" value="" class="sr-only peer" v-model="form.use_random_subdomain">
          <div class="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
          <span class="ml-3 text-sm font-medium text-gray-900 dark:text-gray-300">Use Random Subdomain</span>
        </label>
      </div>

      <div v-if="captchaImageUrl" class="mb-4">
        <label class="relative">
          <img class="mb-4" :src="captchaImageUrl" />
          <input type="text" placeholder="Captcha" id="captcha" v-model="form.captcha" required
          class="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        </label>
      </div>

      <ul class="mt-4 mb-4" v-if="errors.non_field_errors">
        <li class="bg-red-500 p-2 text-white mt-1 rounded-md" v-for="item in errors.non_field_errors">{{ item }}</li>
      </ul>

      <div v-if="isLoading" class="text-center mb-3">
          <div role="status">
              <svg aria-hidden="true" class="inline w-8 h-8 mr-2 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                  <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
              </svg>
              <span class="sr-only">Loading...</span>
          </div>
      </div>

      <button :disabled="isLoading" type="submit" class="w-full bg-blue-500 text-white rounded-md py-2 px-4 hover:bg-blue-600">
        <span v-if="isLoading">
          <i class="animate-spin mr-2 fas fa-spinner"></i>Submitting...
        </span>
          <span v-else>
            Submit
          </span>
      </button>
    </form>

    <div v-if="successMessage" class="max-w-md mx-auto bg-white">
      <div class="flex items-center justify-center">
        <svg class="w-12 h-12 text-green-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
        </svg>
        <h2 class="ml-2 text-xl font-semibold text-green-500">Success!</h2>
      </div>
      <p class="m-4 text-gray-600">
        UUID: <a class="text-blue-500 hover:text-blue-700" :href="`/config/${createdUUID}`" target="_blank">{{ createdUUID }}</a>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';

// Get the CSRF token from the cookie
const csrftoken = document.cookie
  .split('; ')
  .find(cookie => cookie.startsWith('csrftoken='))
  .split('=')[1];

// Set the CSRF token as a default header for all Axios requests
axios.defaults.headers.common['X-CSRFToken'] = csrftoken;
axios.defaults.headers.common['x-requested-with'] = 'XMLHttpRequest';

interface ConfigForm {
  protocol: string;
  url: number;
  ads_url: number;
  expired_at: Date,
  use_fragment: boolean,
  use_cdn: boolean,
  use_random_subdomain: boolean,
  num_fragment: number,
  captcha: string,
  captcha_key: string
}

export default {
  data() {
    return {
      form: {
        protocol: 'vm',
        url: '',
        ads_url: '',
        expired_at: '',
        num_fragment: 10,
        captcha: ''
      } as ConfigForm,
      errors: {},
      successMessage: '',
      submitted: false,
      createdUUID: '',
      captchaImageUrl: null,
      isLoading: false
    };
  },
  computed: {
    minDate() {
      const today = new Date();
      const year = today.getFullYear();
      let month: any = today.getMonth() + 1;
      let day: any = today.getDate();

      // Pad single-digit month/day with leading zero
      month = month < 10 ? `0${month}` : month;
      day = day < 10 ? `0${day}` : day;

      return `${year}-${month}-${day}`;
    }
  },
  mounted() {
    this.reloadCaptcha();
  },
  methods: {
    async reloadCaptcha() {
      try {
        const response = await axios.get(`/backend/captcha/refresh/`);
        this.captchaImageUrl = response.data['image_url'];
        this.form.captcha_key = response.data['key'];
      } catch (error) {
        this.errorMessage = error.message;
        this.error = true;
        console.error(error);
      }
    },
    async handleSubmit() {
      this.isLoading = true;
      this.errors = {};

      if (!this.form.protocol) {
        this.errors.protocol = 'Protocol is required.';
      }

      // Add more validation for other fields
      this.errors = {};
      if (Object.keys(this.errors).length === 0) {
        try {
          const response = await axios.post('/backend/app/config/', this.form);

          this.createdUUID = response.data;
          this.successMessage = "Thanks for submitting your form!"
          this.submitted = true;
          this.isLoading = false;
          // Handle successful response

        } catch (error) {
          this.reloadCaptcha();
          this.isLoading = false;
          // Handle backend errors in DRF format
          if (error.response && error.response.status === 400) {
            this.errors = error.response.data;
          } else {
            console.error(error);
            // Handle other types of errors
          }
        }
      }
    }
  }
};
</script>