<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'
import { API_BASE_URL } from '../config/api'

const emit = defineEmits(['success'])
const { setAuth } = useAuth()

const username = ref('')
const password = ref('')
const message = ref('')
const error = ref('')
const isLoading = ref(false)

const handleLogin = async () => {
  error.value = ''
  message.value = ''
  isLoading.value = true

  try {
    const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      let errorMessage = 'Login failed.'
      if (typeof data === 'string') {
        errorMessage = data
      } else if (data.detail) {
        errorMessage = data.detail
      } else if (Array.isArray(data.non_field_errors) && data.non_field_errors.length > 0) {
        errorMessage = data.non_field_errors[0]
      } else if (typeof data === 'object') {
        const firstVal = Object.values(data)[0]
        errorMessage = Array.isArray(firstVal) ? firstVal[0] : String(firstVal)
      }
      throw new Error(errorMessage)
    }

    setAuth(data.user, data.access, data.refresh)

    message.value = `Login successful! Welcome ${data.user.username}.`
    emit('success')
  } catch (err: any) {
    error.value = err.message || 'Login failed.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <h2>Login</h2>

    <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
      <div>
        <label for="login-username">Username or Email:</label>
        <input class=" border border-black flex-1"
          id="login-username"
          v-model="username"
          type="text"
          required
        />
      </div>

      <div>
        <label for="login-password">Password:</label>
        <input class="border border-black "
          id="login-password"
          v-model="password"
          type="password"
          required
        />
      </div>

      <button type="submit" :disabled="isLoading" class="bg-blue-500 text-white">
        Login
      </button>
    </form>

    <p v-if="message" style="color: green;">{{ message }}</p>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>
