<script setup lang="ts">
import { ref, onMounted } from 'vue'

export interface BlogPost {
  id: number
  title: string
  slug: string
  author: {
    id: number
    username: string
  }
  summary?: string
  content: string
  status: string
  created_at: string
}

const posts = ref<BlogPost[]>([])
const isLoading = ref(false)
const error = ref('')

const fetchPosts = async () => {
  isLoading.value = true
  error.value = ''
  try {
    const response = await fetch('http://localhost:8000/api/blogs/')
    if (!response.ok) {
      throw new Error('Failed to fetch blog posts.')
    }
    const data = await response.json()
    posts.value = Array.isArray(data) ? data : data.results || []
  } catch (err: any) {
    error.value = err.message || 'Error loading posts.'
  } finally {
    isLoading.value = false
  }
}

defineExpose({ fetchPosts })

onMounted(() => {
  fetchPosts()
})
</script>

<template>
  <div class="p-4">
    <h2 class="text-xl font-bold mb-4">Blog Posts</h2>

    <p v-if="isLoading">Loading posts...</p>
    <p v-if="error" style="color: red;">{{ error }}</p>

    <div v-if="!isLoading && posts.length === 0">
      <p>No blog posts found. Log in to create the first post!</p>
    </div>

    <div v-for="post in posts" :key="post.id" class="border p-4 my-3 rounded">
      <h3 class="text-lg font-bold">{{ post.title }}</h3>
      <p class="text-sm text-gray-600">
        By {{ post.author?.username || 'Anonymous' }} | {{ new Date(post.created_at).toLocaleDateString() }} | Status: {{ post.status }}
      </p>
      <p v-if="post.summary" class="italic my-1 text-gray-700">{{ post.summary }}</p>
      <p class="mt-2">{{ post.content }}</p>
    </div>
  </div>
</template>

<style scoped>
</style>
