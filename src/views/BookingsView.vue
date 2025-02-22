<template>
  <div class="bookings">
    <h1>Booking Management</h1>
    <div class="booking-controls">
      <button class="btn-add" @click="$router.push('/bookings/new')">Add New Booking</button>
      <select v-model="filterStatus">
        <option value="all">All Bookings</option>
        <option value="active">Active</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
      </select>
    </div>

    <div class="bookings-list">
      <div v-for="booking in filteredBookings" :key="booking.id" class="booking-card">
        <div class="booking-header">
          <h3>Booking ID: {{ booking.id }}</h3>
          <span :class="['status', booking.status]">{{ booking.status }}</span>
        </div>
        <div class="booking-details">
          <p>Guest: {{ booking.first_name }} {{ booking.last_name }}</p>
          <p>Room: {{ booking.number }} - {{ booking.type }}</p>
          <p>Check-in: {{ booking.check_in }}</p>
          <p>Check-out: {{ booking.check_out }}</p>
        </div>
        <div class="booking-actions">
          <button @click="editBooking(booking)">Edit</button>
          <button @click="deleteBooking(booking)" class="delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { bookingService } from '@/services/api'

export default {
  name: 'BookingsView',
  data() {
    return {
      bookings: [],
      filterStatus: 'all'
    }
  },
  computed: {
    filteredBookings() {
      if (this.filterStatus === 'all') return this.bookings;
      return this.bookings.filter(booking => booking.status === this.filterStatus);
    }
  },
  async created() {
    await this.fetchBookings();
  },
  methods: {
    async fetchBookings() {
      try {
        const response = await bookingService.getAll();
        console.log('Fetched bookings:', response.data); // Debugging line
        this.bookings = response.data;
      } catch (error) {
        console.error('Error fetching bookings:', error);
      }
    },
    editBooking(booking) {
      this.$router.push(`/bookings/${booking.id}/edit`);
    },
    async deleteBooking(booking) {
      if (confirm('Are you sure you want to delete this booking?')) {
        try {
          await bookingService.delete(booking.id);
          await this.fetchBookings();
        } catch (error) {
          console.error('Error deleting booking:', error);
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.bookings {
  padding: 2rem;

  .booking-controls {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;

    .btn-add {
      background-color: #42b983;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 4px;
      cursor: pointer;
    }
  }

  .bookings-list {
    display: grid;
    gap: 1rem;
  }

  .booking-card {
    background-color: #fff;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);

    .booking-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;

      .status {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;

        &.upcoming {
          background-color: #3498db;
          color: white;
        }

        &.active {
          background-color: #42b983;
          color: white;
        }

        &.completed {
          background-color: #95a5a6;
          color: white;
        }

        &.cancelled {
          background-color: #e74c3c;
          color: white;
        }
      }
    }

    .booking-details {
      margin-bottom: 1rem;

      p {
        margin: 0.5rem 0;
      }
    }

    .booking-actions {
      display: flex;
      gap: 0.5rem;

      button {
        flex: 1;
        padding: 0.5rem;
        border: 1px solid #ddd;
        border-radius: 4px;
        background-color: #f8f9fa;
        cursor: pointer;

        &:hover {
          background-color: #e9ecef;
        }
      }
    }
  }
}
</style>