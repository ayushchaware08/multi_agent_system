import axios from 'axios'

// Make sure this matches your backend URL
// const API_BASE_URL = 'http://localhost:8000'|| 'http://127.0.0.1:8000/'
const API_BASE_URL = 'http://localhost:8000'|| 'http://127.0.0.1:8000/'||'https://multi-agent-backend-n3bp.onrender.com/'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Normalize errors so UI shows useful messages
const getApiErrorMessage = (error) => {
  if (error.response?.data?.detail) {
    return typeof error.response.data.detail === 'string'
      ? error.response.data.detail
      : JSON.stringify(error.response.data.detail)
  }
  if (error.response?.data?.message) return error.response.data.message
  if (error.code === 'ECONNABORTED') return 'Request timed out'
  if (error.message === 'Network Error') return 'Cannot reach backend server'
  return error.message || 'Unexpected API error'  
}

api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.data)
    return response
  },
  (error) => {
    const normalizedMessage = getApiErrorMessage(error)
    console.error('API Error:', normalizedMessage)
    return Promise.reject(new Error(normalizedMessage))
  }
)

// Backend expects "text", not "query"
export const submitQuery = async (query) => {
  console.log('Sending query:', query)
  const response = await api.post('/ask', { text: query })
  return response.data
}

export const uploadPDF = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const healthCheck = async () => {
  const response = await api.get('/health')
  return response.data
}

export default api
