<template>
  <div class="home">
    <h1>Welcome to HostalHub</h1>
    <div class="dashboard">
      <div class="stat-card">
        <h3>Available Rooms</h3>
        <p>{{ availableRooms }}</p>
      </div>
      <div class="stat-card">
        <h3>Today's Check-ins</h3>
        <p>{{ todayCheckins }}</p>
      </div>
      <div class="stat-card">
        <h3>Today's Check-outs</h3>
        <p>{{ todayCheckouts }}</p>
      </div>
    </div>

    <div class="quick-actions">
      <button @click="$router.push('/rooms/new')" class="action-btn">Add Room</button>
      <button @click="$router.push('/guests/new')" class="action-btn">New Guest</button>
      <button @click="$router.push('/bookings/new')" class="action-btn">Create Booking</button>
    </div>
  </div>
</template>

<script>
import { roomService, bookingService } from '@/services/api'

export default {
  name: 'HomeView',
  data() {
    return {
      availableRooms: 0,
      todayCheckins: 0,
      todayCheckouts: 0
    }
  },
  async created() {
    await this.fetchDashboardData()
  },
  methods: {
    async fetchDashboardData() {
      try {
        const [roomsResponse, bookingsResponse] = await Promise.all([
          roomService.getStats(),
          bookingService.getTodayStats()
        ])
        
        this.availableRooms = roomsResponse.data.available
        this.todayCheckins = bookingsResponse.data.checkins
        this.todayCheckouts = bookingsResponse.data.checkouts
      } catch (error) {
        console.error('Error fetching dashboard data:', error)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.home {
  padding: 2rem;

  .dashboard {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    margin-top: 2rem;
  }

  .stat-card {
    background-color: #f8f9fa;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    text-align: center;

    h3 {
      margin: 0 0 1rem 0;
      color: #2c3e50;
    }

    p {
      font-size: 2rem;
      margin: 0;
      color: #42b983;
    }
  }

  .quick-actions {
    margin-top: 2rem;
    display: flex;
    gap: 1rem;
    justify-content: center;

    .action-btn {
      padding: 0.75rem 1.5rem;
      border: none;
      border-radius: 4px;
      background-color: #42b983;
      color: white;
      cursor: pointer;
      font-weight: bold;
      transition: background-color 0.2s;

      &:hover {
        background-color: #3aa876;
      }
    }
  }
}
</style>