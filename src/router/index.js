import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/rooms',
    name: 'rooms',
    component: () => import('../views/RoomsView.vue')
  },
  {
    path: '/rooms/new',
    name: 'room-new',
    component: () => import('../views/RoomFormView.vue')
  },
  {
    path: '/rooms/:id/edit',
    name: 'room-edit',
    component: () => import('../views/RoomFormView.vue')
  },
  {
    path: '/bookings',
    name: 'bookings',
    component: () => import('../views/BookingsView.vue')
  },
  {
    path: '/bookings/new',
    name: 'booking-new',
    component: () => import('../views/BookingFormView.vue')
  },
  {
    path: '/bookings/:id/edit',
    name: 'booking-edit',
    component: () => import('../views/BookingFormView.vue')
  },
  {
    path: '/guests',
    name: 'guests',
    component: () => import('../views/GuestsView.vue')
  },
  {
    path: '/guests/new',
    name: 'guest-new',
    component: () => import('../views/GuestFormView.vue')
  },
  {
    path: '/guests/:id/edit',
    name: 'guest-edit',
    component: () => import('../views/GuestFormView.vue')
  }
]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router