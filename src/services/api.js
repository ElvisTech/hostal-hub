import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
});

export const roomService = {
  getAll: () => api.get('/rooms'),
  getById: (id) => api.get(`/rooms/${id}`),
  create: (room) => api.post('/rooms', room),
  update: (id, room) => api.put(`/rooms/${id}`, room),
  delete: (id) => api.delete(`/rooms/${id}`),
  getAvailable: () => api.get('/rooms/available'),
  getStats: () => api.get('/rooms/stats')
};

export const guestService = {
  getAll: () => api.get('/guests'),
  getById: (id) => api.get(`/guests/${id}`),
  create: (guest) => api.post('/guests', guest),
  update: (id, guest) => api.put(`/guests/${id}`, guest),
  delete: (id) => api.delete(`/guests/${id}`)
};

export const bookingService = {
  getAll: () => api.get('/bookings'),
  getById: (id) => api.get(`/bookings/${id}`),
  create: (booking) => api.post('/bookings', booking),
  update: (id, booking) => api.put(`/bookings/${id}`, booking),
  delete: (id) => api.delete(`/bookings/${id}`),
  getTodayStats: () => api.get('/bookings/today')
};