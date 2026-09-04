<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

const emit = defineEmits(['success'])
const { setAuth } = useAuth()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const role = ref('user')
const message = ref('')
const error = ref('')
const isLoading = ref(false)

const handleRegister = async () => {
  error.value = ''
  message.value = ''

  if (password.value !== passwordConfirm.value) {
    error.value = 'Passwords do not match.'
    return
  }

  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/auth/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username.value,
        email: email.value,
        password: password.value,
        password_confirm: passwordConfirm.value,
        role: role.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      let errorMessage = 'Registration failed.'
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

    if (data.tokens && data.user) {
      setAuth(data.user, data.tokens.access, data.tokens.refresh)
    }

    message.value = 'Registration successful!'
    emit('success')
  } catch (err: any) {
    error.value = err.message || 'Registration failed.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <h2>Register</h2>

    <form @submit.prevent="handleRegister" class="flex flex-col gap-4">
      <div class="flex ">
        <label for="reg-username">Username:</label>
        <input class="border border-black w-full"
          id="reg-username"
          v-model="username"
          type="text"
          required
        />
      </div>

      <div>
        <label for="reg-email">Email:</label>
        <input class="border border-black w-full"
          id="reg-email"
          v-model="email"
          type="email"
          required
        />
      </div>

      <div>
        <label for="reg-password">Password:</label>
        <input class="border border-black w-full"
          id="reg-password"
          v-model="password"
          type="password"
          required
        />
      </div>

      <div>
        <label for="reg-password-confirm">Confirm Password:</label>
        <input class="border border-black w-full"
          id="reg-password-confirm"
          v-model="passwordConfirm"
          type="password"
          required
        />
      </div>

      <div>
        <label for="reg-role">Role:</label>
        <select id="reg-role" v-model="role" class="border border-black w-full">
          <option value="user">User</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <button type="submit" :disabled="isLoading" class="bg-blue-500 text-white">
        {{ isLoading ? 'Registering...' : 'Register' }}
      </button>
    </form>

    <p v-if="message" style="color: green;">{{ message }}</p>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>
