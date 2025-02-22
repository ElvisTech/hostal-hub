<template>
  <div class="guests">
    <h1>Guest Management</h1>

    <div class="guest-controls">
      <button class="btn-add" @click="$router.push('/guests/new')">Add New Guest</button>
      <div class="guest-search">
        <input type="text" 
               v-model="searchQuery" 
               placeholder="Search guests..."
               @input="searchGuests">
      </div>
    </div>

    <div class="guests-list">
      <div v-for="guest in filteredGuests" :key="guest.id" class="guest-card">
        <div class="guest-header">
          <h3>{{ guest.first_name }} {{ guest.last_name }}</h3>
          <span class="guest-id">ID: {{ guest.id }}</span>
        </div>
        <div class="guest-details">
          <p><i class="fas fa-envelope"></i> {{ guest.email }}</p>
          <p><i class="fas fa-phone"></i> {{ guest.phone }}</p>
          <p><i class="fas fa-map-marker"></i> {{ guest.country }}</p>
          <p><i class="fas fa-passport"></i> {{ guest.document_id }}</p>
        </div>
        <div class="guest-actions">
          <button @click="editGuest(guest)">Edit</button>
          <button @click="deleteGuest(guest)" class="delete">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { guestService } from '@/services/api'

export default {
  name: 'GuestsView',
  data() {
    return {
      guests: [],
      searchQuery: ''
    }
  },
  computed: {
    filteredGuests() {
      if (!this.searchQuery) return this.guests;
      
      const query = this.searchQuery.toLowerCase();
      return this.guests.filter(guest => 
        guest.first_name.toLowerCase().includes(query) ||
        guest.last_name.toLowerCase().includes(query) ||
        guest.email.toLowerCase().includes(query) ||
        guest.document_id.toLowerCase().includes(query)
      );
    }
  },
  async created() {
    await this.fetchGuests();
  },
  methods: {
    async fetchGuests() {
      try {
        const response = await guestService.getAll();
        this.guests = response.data;
      } catch (error) {
        console.error('Error fetching guests:', error);
      }
    },
    editGuest(guest) {
      this.$router.push(`/guests/${guest.id}/edit`);
    },
    async deleteGuest(guest) {
      if (confirm('Are you sure you want to delete this guest?')) {
        try {
          await guestService.delete(guest.id);
          await this.fetchGuests();
        } catch (error) {
          console.error('Error deleting guest:', error);
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.guests {
  padding: 2rem;

  .guest-controls {
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

      &:hover {
        background-color: #3aa876;
      }
    }

    .guest-search input {
      padding: 0.5rem;
      border: 1px solid #ddd;
      border-radius: 4px;
      width: 300px;
    }
  }

  .guests-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1rem;
  }

  .guest-card {
    background-color: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);

    .guest-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;

      h3 {
        margin: 0;
      }
    }

    .guest-details {
      margin-bottom: 1rem;

      p {
        margin: 0.5rem 0;
      }
    }

    .guest-actions {
      display: flex;
      gap: 0.5rem;

      button {
        padding: 0.25rem 0.75rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;

        &:first-child {
          background-color: #42b983;
          color: white;
        }

        &.delete {
          background-color: #dc3545;
          color: white;
        }

        &:hover {
          opacity: 0.9;
        }
      }
    }
  }
}
</style>