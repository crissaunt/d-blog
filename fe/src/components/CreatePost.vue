<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

const emit = defineEmits(['created', 'close'])
const { accessToken } = useAuth()

const title = ref('')

const message = ref('')
const error = ref('')
const isLoading = ref(false)

const handleCreatePost = async () => {
  error.value = ''
  message.value = ''

  if (!accessToken.value) {
    error.value = 'You must be logged in to create a post.'
    return
  }

  isLoading.value = true

  try {
    const response = await fetch('http://localhost:8000/api/blogs/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken.value}`,
      },
      body: JSON.stringify({
        title: title.value,
       
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || JSON.stringify(data))
    }

    message.value = 'Blog post created successfully!'
    title.value = ''

    emit('created', data)
  } catch (err: any) {
    error.value = err.message || 'Failed to create blog post.'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div>
    <h2>Create New Blog Post</h2>

    <form @submit.prevent="handleCreatePost">
      <div>
        <label for="post-title">Title:</label>
        <input
          id="post-title"
          v-model="title"
          type="text"
          required
        />
      </div>




      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Creating...' : 'Publish Post' }}
      </button>
    </form>

    <p v-if="message" style="color: green;">{{ message }}</p>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>
