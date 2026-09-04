import { ref, computed } from 'vue'
import { API_BASE_URL } from '../config/api'

export interface AuthUser {
  id: number
  username: string
  email: string
  role: string
  bio?: string | null
  profile_picture?: string | null
  is_staff?: boolean
}

const savedUser = localStorage.getItem('user')
const currentUser = ref<AuthUser | null>(savedUser ? JSON.parse(savedUser) : null)
const accessToken = ref<string | null>(localStorage.getItem('access_token'))
const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))

export function useAuth() {
  const isLoggedIn = computed(() => !!accessToken.value && !!currentUser.value)

  const setAuth = (user: AuthUser, access: string, refresh: string) => {
    currentUser.value = user
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('user', JSON.stringify(user))
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  const logout = async () => {
    const refresh = refreshToken.value
    const access = accessToken.value

    if (refresh && access) {
      try {
        await fetch(`${API_BASE_URL}/api/auth/logout/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${access}`,
          },
          body: JSON.stringify({ refresh }),
        })
      } catch (e) {
        console.error('Logout error:', e)
      }
    }

    currentUser.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return {
    currentUser,
    accessToken,
    refreshToken,
    isLoggedIn,
    setAuth,
    logout,
  }
}
