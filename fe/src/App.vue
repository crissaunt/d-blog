<script setup lang="ts">
import { ref, watch } from 'vue'
import { useAuth } from './composables/useAuth'
import Header from './components/Header.vue'
import Home from './components/Home.vue'
import AdminDashboard from './components/AdminDashboard.vue'

const { currentUser, isLoggedIn } = useAuth()
const currentView = ref<'home' | 'admin'>(
  (currentUser.value?.role === 'admin' || currentUser.value?.is_staff) ? 'admin' : 'home'
)
const homeRef = ref<InstanceType<typeof Home> | null>(null)

watch(
  currentUser,
  (user) => {
    if (user && (user.role === 'admin' || user.is_staff)) {
      currentView.value = 'admin'
    } else if (!user) {
      currentView.value = 'home'
    }
  },
  { immediate: true }
)

const handleNavigate = (view: 'home' | 'admin') => {
  currentView.value = view
}

const handlePostCreated = () => {
  homeRef.value?.fetchPosts()
}
</script>

<template>
  <header>
    <Header
      :current-view="currentView"
      @post-created="handlePostCreated"
      @navigate="handleNavigate"
    />
  </header>

  <main>
    <AdminDashboard
      v-if="currentView === 'admin' && isLoggedIn && (currentUser?.role === 'admin' || currentUser?.is_staff)"
      @navigate="handleNavigate"
    />
    <Home v-else ref="homeRef" />
  </main>
</template>

<style scoped>
</style>
