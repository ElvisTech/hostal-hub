<template>
  <div class="rooms">
    <h1>Rooms Management</h1>
    <div class="room-controls">
      <button class="btn-add" @click="$router.push('/rooms/new')">Add New Room</button>
      <select v-model="filterStatus">
        <option value="all">All Rooms</option>
        <option value="available">Available</option>
        <option value="occupied">Occupied</option>
        <option value="maintenance">Maintenance</option>
      </select>
    </div>

    <div class="rooms-list">
      <div v-for="room in filteredRooms" :key="room.id" class="room-card">
        <div class="room-header">
          <h3>Room {{ room.number }}</h3>
          <span :class="['status', room.status]">{{ room.status }}</span>
        </div>
        <div class="room-details">
          <p>Type: {{ room.type }}</p>
          <p>Capacity: {{ room.capacity }}</p>
          <p>Price: ${{ room.price }}/night</p>
        </div>
        <div class="room-actions">
          <button @click="editRoom(room)">Edit</button>
          <button @click="changeStatus(room, 'available')" 
                  v-if="room.status !== 'available'">Set Available</button>
          <button @click="changeStatus(room, 'occupied')" 
                  v-if="room.status === 'available'">Set Occupied</button>
          <button @click="changeStatus(room, 'maintenance')" 
                  v-if="room.status === 'available'">Set Maintenance</button>
          <button @click="deleteRoom(room)" class="delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { roomService } from '@/services/api'

export default {
  name: 'RoomsView',
  data() {
    return {
      rooms: [],
      filterStatus: 'all'
    }
  },
  computed: {
    filteredRooms() {
      if (this.filterStatus === 'all') return this.rooms;
      return this.rooms.filter(room => room.status === this.filterStatus);
    }
  },
  async created() {
    await this.fetchRooms();
  },
  methods: {
    async fetchRooms() {
      try {
        const response = await roomService.getAll();
        this.rooms = response.data;
      } catch (error) {
        console.error('Error fetching rooms:', error);
      }
    },
    async changeStatus(room, newStatus) {
      try {
        const updatedRoom = { ...room, status: newStatus };
        await roomService.update(room.id, updatedRoom);
        await this.fetchRooms();
      } catch (error) {
        console.error('Error updating room status:', error);
      }
    },
    editRoom(room) {
      this.$router.push(`/rooms/${room.id}/edit`);
    },
    async deleteRoom(room) {
      if (confirm('Are you sure you want to delete this room?')) {
        try {
          await roomService.delete(room.id);
          await this.fetchRooms();
        } catch (error) {
          console.error('Error deleting room:', error);
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.rooms {
  padding: 2rem;

  .room-controls {
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

  .room-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .room-card {
    background-color: #fff;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);

    .room-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;

      .status {
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.875rem;

        &.available {
          background-color: #42b983;
          color: white;
        }

        &.occupied {
          background-color: #e74c3c;
          color: white;
        }

        &.maintenance {
          background-color: #f39c12;
          color: white;
        }
      }
    }

    .room-details {
      margin-bottom: 1rem;

      p {
        margin: 0.5rem 0;
      }
    }

    .room-actions {
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