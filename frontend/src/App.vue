<script setup>

</script>

<template>
  <nav class="flex items-center justify-between flex-wrap bg-gray-800 p-6">
    <div class="flex items-center flex-shrink-0 text-white mr-6">
      <svg class="fill-current h-8 w-8 mr-2" width="54" height="54" viewBox="0 0 54 54" xmlns="http://www.w3.org/2000/svg"><path d="M13.5 22.1c1.8-7.2 6.3-10.8 13.5-10.8 10.8 0 12.15 8.1 17.55 9.45 3.6.9 6.75-.45 9.45-4.05-1.8 7.2-6.3 10.8-13.5 10.8-10.8 0-12.15-8.1-17.55-9.45-3.6-.9-6.75.45-9.45 4.05zM0 38.3c1.8-7.2 6.3-10.8 13.5-10.8 10.8 0 12.15 8.1 17.55 9.45 3.6.9 6.75-.45 9.45-4.05-1.8 7.2-6.3 10.8-13.5 10.8-10.8 0-12.15-8.1-17.55-9.45-3.6-.9-6.75.45-9.45 4.05z"/></svg>
      <span class="font-semibold text-xl tracking-tight">Mahsa Server</span>
    </div>
    <div class="block lg:hidden">
      <button class="flex items-center px-3 py-2 border rounded text-teal-200 border-teal-400 hover:text-white hover:border-white">
        <svg class="fill-current h-3 w-3" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><title>Menu</title><path d="M0 3h20v2H0V3zm0 6h20v2H0V9zm0 6h20v2H0v-2z"/></svg>
      </button>
    </div>
    <div class="w-full block flex-grow lg:flex lg:items-center lg:w-auto">
      <div class="text-sm lg:flex-grow">
          <a href="/" :class="{ 'selected': '/' === $route.path }" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium">Home</a>
          <a href="/config" :class="{ 'selected': '/config' === $route.path }" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium">Submit Config</a>
          <a href="/stats" :class="{ 'selected': '/stats' === $route.path }" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium">Stats</a>
          <a href="/about-us" :class="{ 'selected': '/about-us' === $route.path }" class="text-gray-300 hover:text-white px-3 py-2 text-sm font-medium">About Us</a>
      </div>
      <div>
        <a href="https://github.com/GFW-knocker/MahsaNG" class="inline-block text-sm px-4 py-2 leading-none border rounded text-white border-white hover:border-transparent hover:text-teal-500 hover:bg-white mt-4 lg:mt-0">
          Download MahsaNG
        </a>
      </div>
    </div>
  </nav>
  <div class="max-w-7xl mx-auto px-2 sm:px-6 lg:px-8">
    <router-view />
  </div>
</template>

<style scoped>
.selected {
  color: white;
  border-bottom: solid white 3px;
}
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>

<script type="ts">
import axios from "axios";

axios.defaults.headers.common['x-requested-with'] = 'XMLHttpRequest';
</script>