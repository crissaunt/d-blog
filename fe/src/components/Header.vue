<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'
import Login from './Login.vue'
import Register from './Register.vue'
import CreatePost from './CreatePost.vue'

defineProps<{
  currentView?: 'home' | 'admin'
}>()

const emit = defineEmits(['postCreated', 'navigate'])
const { currentUser, isLoggedIn, logout } = useAuth()

const handleLogout = async () => {
  await logout()
  emit('navigate', 'home')
}

const showModal = ref<'login' | 'register' | 'create-post' | null>(null)

const openLogin = () => {
  showModal.value = 'login'
}

const openRegister = () => {
  showModal.value = 'register'
}

const openCreatePost = () => {
  showModal.value = 'create-post'
}

const closeModal = () => {
  showModal.value = null
}

const handleAuthSuccess = () => {
  closeModal()
}

const handlePostCreated = (post: any) => {
  closeModal()
  emit('postCreated', post)
}
</script>

<template>
  <div class="flex items-center justify-between p-4 border-b">
    <h1 class="text-xl font-bold cursor-pointer" @click="emit('navigate', 'home')">Logo</h1>

    <div class="flex gap-4 items-center">
      <button
        type="button"
        @click="emit('navigate', 'home')"
        
      >
        Home
      </button>
      <a href="#">About</a>
      <a href="#">Contact</a>

      <template v-if="isLoggedIn">
    

        <button
          type="button"
          @click="openCreatePost"
          class="bg-blue-500 p-2 text-white rounded cursor-pointer"
        >
          + Create Post
        </button>

        <button
          type="button"
          @click="handleLogout"
          class="bg-red-500 p-2 text-white rounded cursor-pointer"
        >
          Logout
        </button>
      </template>

      <template v-else>
        <button
          type="button"
          @click="openRegister"
          class="bg-blue-500 p-2 text-white rounded cursor-pointer"
        >
          Sign Up
        </button>
        <button
          type="button"
          @click="openLogin"
          class="bg-blue-500 p-2 text-white rounded cursor-pointer"
        >
          Login
        </button>
      </template>
    </div>
  </div>

  <div
    v-if="showModal"
    class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
    @click.self="closeModal"
  >
    <div class="bg-white p-6 rounded shadow-lg max-w-lg w-full relative">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-bold">
          {{
            showModal === 'login'
              ? 'Login'
              : showModal === 'register'
              ? 'Register'
              : 'Create Blog Post'
          }}
        </h2>
        <button
          type="button"
          @click="closeModal"
          class="text-gray-500 hover:text-black font-bold text-xl cursor-pointer"
        >
          &times;
        </button>
      </div>

      <Login v-if="showModal === 'login'" @success="handleAuthSuccess" />

      <Register v-if="showModal === 'register'" @success="handleAuthSuccess" />

      <CreatePost
        v-if="showModal === 'create-post'"
        @created="handlePostCreated"
        @close="closeModal"
      />

  

    </div>
  </div>
</template>

<style scoped>
</style>
