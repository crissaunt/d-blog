<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuth } from '../composables/useAuth'

interface Stats {
  total_posts: number
  published_posts: number
  draft_posts: number
  total_users: number
  total_categories: number
}

interface UserItem {
  id: number
  username: string
  email: string
  role: string
  is_staff: boolean
  date_joined: string
}

interface CategoryItem {
  id: number
  name: string
  slug: string
  description?: string
  created_at: string
}

interface PostItem {
  id: number
  title: string
  slug: string
  author: {
    id: number
    username: string
  }
  category?: {
    id: number
    name: string
  } | null
  created_at: string
}

const emit = defineEmits(['navigate'])
const { accessToken, currentUser } = useAuth()

const activeTab = ref<'overview' | 'posts' | 'categories' | 'users'>('overview')
const stats = ref<Stats | null>(null)
const posts = ref<PostItem[]>([])
const categories = ref<CategoryItem[]>([])
const users = ref<UserItem[]>([])

const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const newCategoryName = ref('')
const newCategoryDescription = ref('')
const isCreatingCategory = ref(false)

const getAuthHeaders = () => {
  return {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken.value}`,
  }
}

const fetchStats = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/admin/stats/', {
      headers: getAuthHeaders(),
    })
    if (res.ok) {
      stats.value = await res.json()
    }
  } catch (e: any) {
    console.error(e)
  }
}

const fetchPosts = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/blogs/', {
      headers: getAuthHeaders(),
    })
    if (res.ok) {
      const data = await res.json()
      posts.value = Array.isArray(data) ? data : data.results || []
    }
  } catch (e: any) {
    console.error(e)
  }
}

const fetchCategories = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/categories/', {
      headers: getAuthHeaders(),
    })
    if (res.ok) {
      const data = await res.json()
      categories.value = Array.isArray(data) ? data : data.results || []
    }
  } catch (e: any) {
    console.error(e)
  }
}

const fetchUsers = async () => {
  try {
    const res = await fetch('http://localhost:8000/api/admin/users/', {
      headers: getAuthHeaders(),
    })
    if (res.ok) {
      const data = await res.json()
      users.value = Array.isArray(data) ? data : data.results || []
    }
  } catch (e: any) {
    console.error(e)
  }
}

const loadDashboardData = async () => {
  isLoading.value = true
  errorMessage.value = ''
  try {
    await Promise.all([
      fetchStats(),
      fetchPosts(),
      fetchCategories(),
      fetchUsers(),
    ])
  } catch (err: any) {
    errorMessage.value = err.message || 'Failed to load dashboard data.'
  } finally {
    isLoading.value = false
  }
}

const deletePost = async (slug: string) => {
  if (!confirm('Are you sure you want to delete this post?')) return
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(`http://localhost:8000/api/blogs/${slug}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    })
    if (!res.ok) {
      throw new Error('Failed to delete post.')
    }
    successMessage.value = 'Post deleted successfully.'
    posts.value = posts.value.filter((p) => p.slug !== slug)
    fetchStats()
  } catch (e: any) {
    errorMessage.value = e.message || 'Error deleting post.'
  }
}

const handleCreateCategory = async () => {
  if (!newCategoryName.value.trim()) return
  errorMessage.value = ''
  successMessage.value = ''
  isCreatingCategory.value = true
  try {
    const res = await fetch('http://localhost:8000/api/categories/', {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify({
        name: newCategoryName.value.trim(),
        description: newCategoryDescription.value.trim(),
      }),
    })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.name?.[0] || data.detail || 'Failed to create category.')
    }
    successMessage.value = 'Category created successfully.'
    newCategoryName.value = ''
    newCategoryDescription.value = ''
    await fetchCategories()
    fetchStats()
  } catch (e: any) {
    errorMessage.value = e.message || 'Error creating category.'
  } finally {
    isCreatingCategory.value = false
  }
}

const deleteUser = async (userId: number) => {
  if (!confirm('Are you sure you want to delete this user?')) return
  errorMessage.value = ''
  successMessage.value = ''
  try {
    const res = await fetch(`http://localhost:8000/api/admin/users/${userId}/`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    })
    if (!res.ok) {
      throw new Error('Failed to delete user.')
    }
    successMessage.value = 'User deleted successfully.'
    users.value = users.value.filter((u) => u.id !== userId)
    fetchStats()
  } catch (e: any) {
    errorMessage.value = e.message || 'Error deleting user.'
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<template>
  <div class="p-6 max-w-7xl mx-auto font-sans">
    <!-- Top Header -->
    <div class="border-b border-black pb-4 mb-6 flex justify-between items-center">
      <div>
        <h1 class="text-2xl font-bold tracking-tight">Admin Dashboard</h1>
        <p class="text-sm">System administration and content management</p>
      </div>
      <div class="flex gap-2">
        <button
          type="button"
          @click="loadDashboardData"
          class="border border-black px-3 py-1 text-sm bg-white hover:bg-gray-100 cursor-pointer"
        >
          Refresh Data
        </button>
        <button
          type="button"
          @click="emit('navigate', 'home')"
          class="border border-black px-3 py-1 text-sm bg-black text-white hover:bg-gray-800 cursor-pointer"
        >
          Back to Site
        </button>
      </div>
    </div>

    <!-- Feedback messages -->
    <div v-if="errorMessage" class="border border-black p-3 mb-4 text-sm">
      Error: {{ errorMessage }}
    </div>
    <div v-if="successMessage" class="border border-black p-3 mb-4 text-sm">
      Success: {{ successMessage }}
    </div>

    <!-- Navigation Tabs -->
    <div class="flex border-b border-black mb-6">
      <button
        type="button"
        @click="activeTab = 'overview'"
        class="px-4 py-2 text-sm font-medium border-t border-l border-r border-black -mb-[1px] cursor-pointer"
        :class="activeTab === 'overview' ? 'bg-black text-white' : 'bg-white text-black hover:bg-gray-100'"
      >
        Overview
      </button>
      <button
        type="button"
        @click="activeTab = 'posts'"
        class="px-4 py-2 text-sm font-medium border-t border-l border-r border-black -mb-[1px] ml-1 cursor-pointer"
        :class="activeTab === 'posts' ? 'bg-black text-white' : 'bg-white text-black hover:bg-gray-100'"
      >
        Posts ({{ posts.length }})
      </button>
      <button
        type="button"
        @click="activeTab = 'categories'"
        class="px-4 py-2 text-sm font-medium border-t border-l border-r border-black -mb-[1px] ml-1 cursor-pointer"
        :class="activeTab === 'categories' ? 'bg-black text-white' : 'bg-white text-black hover:bg-gray-100'"
      >
        Categories ({{ categories.length }})
      </button>
      <button
        type="button"
        @click="activeTab = 'users'"
        class="px-4 py-2 text-sm font-medium border-t border-l border-r border-black -mb-[1px] ml-1 cursor-pointer"
        :class="activeTab === 'users' ? 'bg-black text-white' : 'bg-white text-black hover:bg-gray-100'"
      >
        Users ({{ users.length }})
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="py-8 text-center text-sm">
      Loading dashboard...
    </div>

    <!-- TAB 1: OVERVIEW -->
    <div v-else-if="activeTab === 'overview'" class="space-y-6">
      <!-- Stats Cards -->
      <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div class="border border-black p-4">
          <div class="text-xs uppercase tracking-wider">Total Posts</div>
          <div class="text-3xl font-bold mt-1">{{ stats?.total_posts ?? posts.length }}</div>
        </div>
        <div class="border border-black p-4">
          <div class="text-xs uppercase tracking-wider">Published</div>
          <div class="text-3xl font-bold mt-1">{{ stats?.published_posts ?? 0 }}</div>
        </div>
        <div class="border border-black p-4">
          <div class="text-xs uppercase tracking-wider">Drafts</div>
          <div class="text-3xl font-bold mt-1">{{ stats?.draft_posts ?? 0 }}</div>
        </div>
        <div class="border border-black p-4">
          <div class="text-xs uppercase tracking-wider">Total Users</div>
          <div class="text-3xl font-bold mt-1">{{ stats?.total_users ?? users.length }}</div>
        </div>
        <div class="border border-black p-4">
          <div class="text-xs uppercase tracking-wider">Categories</div>
          <div class="text-3xl font-bold mt-1">{{ stats?.total_categories ?? categories.length }}</div>
        </div>
      </div>

      <!-- Quick Summary Tables -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Recent Posts Summary -->
        <div class="border border-black p-4">
          <div class="flex justify-between items-center mb-3 border-b border-black pb-2">
            <h2 class="font-bold text-base">Recent Posts</h2>
            <button
              type="button"
              @click="activeTab = 'posts'"
              class="text-xs underline cursor-pointer"
            >
              View All
            </button>
          </div>
          <div v-if="posts.length === 0" class="text-sm">No posts found.</div>
          <ul v-else class="divide-y divide-gray-300">
            <li v-for="post in posts.slice(0, 5)" :key="post.id" class="py-2 text-sm flex justify-between items-center">
              <div>
                <span class="font-medium">{{ post.title }}</span>
                <span class="block text-xs">By {{ post.author?.username }}</span>
              </div>
              <span class="text-xs">{{ new Date(post.created_at).toLocaleDateString() }}</span>
            </li>
          </ul>
        </div>

        <!-- Recent Users Summary -->
        <div class="border border-black p-4">
          <div class="flex justify-between items-center mb-3 border-b border-black pb-2">
            <h2 class="font-bold text-base">Registered Users</h2>
            <button
              type="button"
              @click="activeTab = 'users'"
              class="text-xs underline cursor-pointer"
            >
              View All
            </button>
          </div>
          <div v-if="users.length === 0" class="text-sm">No users found.</div>
          <ul v-else class="divide-y divide-gray-300">
            <li v-for="u in users.slice(0, 5)" :key="u.id" class="py-2 text-sm flex justify-between items-center">
              <div>
                <span class="font-medium">{{ u.username }}</span>
                <span class="block text-xs">{{ u.email }} | Role: {{ u.role }}</span>
              </div>
              <span class="text-xs">{{ new Date(u.date_joined).toLocaleDateString() }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- TAB 2: POSTS MANAGEMENT -->
    <div v-else-if="activeTab === 'posts'" class="space-y-4">
      <div class="flex justify-between items-center">
        <h2 class="font-bold text-lg">All Blog Posts</h2>
        <span class="text-sm">Showing {{ posts.length }} posts</span>
      </div>

      <div class="border border-black overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="border-b border-black bg-gray-100">
              <th class="p-3 font-bold border-r border-black">ID</th>
              <th class="p-3 font-bold border-r border-black">Title</th>
              <th class="p-3 font-bold border-r border-black">Author</th>
              <th class="p-3 font-bold border-r border-black">Category</th>
              <th class="p-3 font-bold border-r border-black">Created</th>
              <th class="p-3 font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="posts.length === 0">
              <td colspan="6" class="p-4 text-center">No posts found.</td>
            </tr>
            <tr
              v-for="post in posts"
              :key="post.id"
              class="border-b border-gray-300 hover:bg-gray-50"
            >
              <td class="p-3 border-r border-gray-300">{{ post.id }}</td>
              <td class="p-3 font-medium border-r border-gray-300">{{ post.title }}</td>
              <td class="p-3 border-r border-gray-300">{{ post.author?.username || 'Unknown' }}</td>
              <td class="p-3 border-r border-gray-300">{{ post.category?.name || '-' }}</td>
              <td class="p-3 border-r border-gray-300">{{ new Date(post.created_at).toLocaleDateString() }}</td>
              <td class="p-3 space-x-2">
                <button
                  type="button"
                  @click="deletePost(post.slug)"
                  class="border border-black px-2 py-1 text-xs bg-white hover:bg-gray-100 cursor-pointer"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 3: CATEGORIES MANAGEMENT -->
    <div v-else-if="activeTab === 'categories'" class="space-y-6">
      <!-- Create Category Form -->
      <div class="border border-black p-4">
        <h2 class="font-bold text-base mb-3">Add New Category</h2>
        <form @submit.prevent="handleCreateCategory" class="flex flex-col md:flex-row gap-3 items-end">
          <div class="flex-1 w-full">
            <label class="block text-xs font-bold mb-1">Category Name</label>
            <input
              v-model="newCategoryName"
              type="text"
              required
              placeholder="e.g. Technology"
              class="w-full border border-black p-2 text-sm bg-white"
            />
          </div>
          <div class="flex-1 w-full">
            <label class="block text-xs font-bold mb-1">Description (Optional)</label>
            <input
              v-model="newCategoryDescription"
              type="text"
              placeholder="Short description"
              class="w-full border border-black p-2 text-sm bg-white"
            />
          </div>
          <button
            type="submit"
            :disabled="isCreatingCategory"
            class="border border-black bg-black text-white px-4 py-2 text-sm hover:bg-gray-800 cursor-pointer whitespace-nowrap"
          >
            {{ isCreatingCategory ? 'Adding...' : 'Add Category' }}
          </button>
        </form>
      </div>

      <!-- Categories Table -->
      <div class="border border-black overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="border-b border-black bg-gray-100">
              <th class="p-3 font-bold border-r border-black">ID</th>
              <th class="p-3 font-bold border-r border-black">Name</th>
              <th class="p-3 font-bold border-r border-black">Slug</th>
              <th class="p-3 font-bold border-r border-black">Description</th>
              <th class="p-3 font-bold">Created Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="categories.length === 0">
              <td colspan="5" class="p-4 text-center">No categories found.</td>
            </tr>
            <tr
              v-for="cat in categories"
              :key="cat.id"
              class="border-b border-gray-300 hover:bg-gray-50"
            >
              <td class="p-3 border-r border-gray-300">{{ cat.id }}</td>
              <td class="p-3 font-medium border-r border-gray-300">{{ cat.name }}</td>
              <td class="p-3 border-r border-gray-300">{{ cat.slug }}</td>
              <td class="p-3 border-r border-gray-300">{{ cat.description || '-' }}</td>
              <td class="p-3">{{ new Date(cat.created_at).toLocaleDateString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- TAB 4: USERS MANAGEMENT -->
    <div v-else-if="activeTab === 'users'" class="space-y-4">
      <div class="flex justify-between items-center">
        <h2 class="font-bold text-lg">All Registered Users</h2>
        <span class="text-sm">Total: {{ users.length }}</span>
      </div>

      <div class="border border-black overflow-x-auto">
        <table class="w-full text-left text-sm border-collapse">
          <thead>
            <tr class="border-b border-black bg-gray-100">
              <th class="p-3 font-bold border-r border-black">ID</th>
              <th class="p-3 font-bold border-r border-black">Username</th>
              <th class="p-3 font-bold border-r border-black">Email</th>
              <th class="p-3 font-bold border-r border-black">Role</th>
              <th class="p-3 font-bold border-r border-black">Staff</th>
              <th class="p-3 font-bold border-r border-black">Joined</th>
              <th class="p-3 font-bold">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="users.length === 0">
              <td colspan="7" class="p-4 text-center">No users found.</td>
            </tr>
            <tr
              v-for="u in users"
              :key="u.id"
              class="border-b border-gray-300 hover:bg-gray-50"
            >
              <td class="p-3 border-r border-gray-300">{{ u.id }}</td>
              <td class="p-3 font-medium border-r border-gray-300">{{ u.username }}</td>
              <td class="p-3 border-r border-gray-300">{{ u.email }}</td>
              <td class="p-3 border-r border-gray-300 uppercase text-xs">{{ u.role }}</td>
              <td class="p-3 border-r border-gray-300">{{ u.is_staff ? 'Yes' : 'No' }}</td>
              <td class="p-3 border-r border-gray-300">{{ new Date(u.date_joined).toLocaleDateString() }}</td>
              <td class="p-3">
                <button
                  v-if="u.id !== currentUser?.id"
                  type="button"
                  @click="deleteUser(u.id)"
                  class="border border-black px-2 py-1 text-xs bg-white hover:bg-gray-100 cursor-pointer"
                >
                  Delete
                </button>
                <span v-else class="text-xs text-gray-500">Current User</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
