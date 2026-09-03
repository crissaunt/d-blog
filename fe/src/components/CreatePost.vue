<script setup lang="ts">
import { ref } from 'vue'
import { useAuth } from '../composables/useAuth'

const emit = defineEmits(['created', 'close'])
const { accessToken } = useAuth()

const title = ref('')
const summary = ref('')
const content = ref('')
const status = ref('published')
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
        summary: summary.value,
        content: content.value,
        status: status.value,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || JSON.stringify(data))
    }

    message.value = 'Blog post created successfully!'
    title.value = ''
    summary.value = ''
    content.value = ''
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

      <div>
        <label for="post-summary">Summary / Excerpt:</label>
        <textarea
          id="post-summary"
          v-model="summary"
          rows="2"
        ></textarea>
      </div>

      <div>
        <label for="post-content">Content:</label>
        <textarea
          id="post-content"
          v-model="content"
          rows="6"
          required
        ></textarea>
      </div>

      <div>
        <label for="post-status">Status:</label>
        <select id="post-status" v-model="status">
          <option value="draft">Draft</option>
          <option value="published">Published</option>
        </select>
      </div>

      <button type="submit" :disabled="isLoading">
        {{ isLoading ? 'Creating...' : 'Publish Post' }}
      </button>
    </form>

    <p v-if="message" style="color: green;">{{ message }}</p>
    <p v-if="error" style="color: red;">{{ error }}</p>
  </div>
</template>
