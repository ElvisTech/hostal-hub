<template>
  <div class="booking-form">
    <h2>{{ isEditing ? 'Edit Booking' : 'New Booking' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="guest">Guest</label>
        <select id="guest" v-model="booking.guest_id" required>
          <option value="">Select a guest</option>
          <option v-for="guest in guests" :key="guest.id" :value="guest.id">
            {{ guest.first_name }} {{ guest.last_name }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="room">Room</label>
        <select id="room" v-model="booking.room_id" required>
          <option value="">Select a room</option>
          <option v-for="room in availableRooms" :key="room.id" :value="room.id">
            Room {{ room.number }} - {{ room.type }}
          </option>
        </select>
      </div>

      <div class="form-group">
        <label for="check_in">Check-in Date</label>
        <input 
          type="date" 
          id="check_in" 
          v-model="booking.check_in"
          :min="today"
          required
        >
      </div>

      <div class="form-group">
        <label for="check_out">Check-out Date</label>
        <input 
          type="date" 
          id="check_out" 
          v-model="booking.check_out"
          :min="booking.check_in"
          required
        >
      </div>

      <div class="form-actions">
        <button type="button" @click="$router.push('/bookings')">Cancel</button>
        <button type="submit">{{ isEditing ? 'Update' : 'Create' }}</button>
      </div>
    </form>
  </div>
</template>

<script>
import { bookingService, guestService, roomService } from '@/services/api'

export default {
  name: 'BookingFormView',
  data() {
    return {
      booking: {
        guest_id: '',
        room_id: '',
        check_in: '',
        check_out: '',
        status: 'active'
      },
      guests: [],
      availableRooms: []
    }
  },
  computed: {
    isEditing() {
      return this.$route.params.id !== undefined
    },
    today() {
      return new Date().toISOString().split('T')[0]
    }
  },
  async created() {
    await Promise.all([
      this.fetchGuests(),
      this.fetchAvailableRooms()
    ])
    
    if (this.isEditing) {
      await this.fetchBooking()
    }
  },
  methods: {
    async fetchGuests() {
      try {
        const response = await guestService.getAll()
        this.guests = response.data
      } catch (error) {
        console.error('Error fetching guests:', error)
      }
    },
    async fetchAvailableRooms() {
      try {
        const response = await roomService.getAvailable()
        this.availableRooms = response.data
      } catch (error) {
        console.error('Error fetching rooms:', error)
      }
    },
    async fetchBooking() {
      try {
        const response = await bookingService.getById(this.$route.params.id)
        this.booking = response.data
      } catch (error) {
        console.error('Error fetching booking:', error)
      }
    },
    async handleSubmit() {
      try {
        console.log('Submitting booking:', this.booking); // Debugging line
        if (this.isEditing) {
          await bookingService.update(this.$route.params.id, this.booking)
        } else {
          await bookingService.create(this.booking)
        }
        this.$router.push('/bookings')
      } catch (error) {
        console.error('Error saving booking:', error)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.booking-form {
  max-width: 600px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);

  h2 {
    margin-bottom: 2rem;
    color: #2c3e50;
  }

  .form-group {
    margin-bottom: 1.5rem;

    label {
      display: block;
      margin-bottom: 0.5rem;
      color: #2c3e50;
    }

    input, select {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      font-size: 1rem;

      &:focus {
        outline: none;
        border-color: #42b983;
      }
    }
  }

  .form-actions {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;

    button {
      padding: 0.5rem 1.5rem;
      border: none;
      border-radius: 4px;
      cursor: pointer;

      &[type="button"] {
        background-color: #6c757d;
        color: white;
      }

      &[type="submit"] {
        background-color: #42b983;
        color: white;
      }

      &:hover {
        opacity: 0.9;
      }
    }
  }
}
</style>