<template>
  <div class="room-form">
    <h2>{{ isEditing ? 'Edit Room' : 'Add New Room' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="number">Room Number</label>
        <input 
          type="text" 
          id="number" 
          v-model="room.number" 
          required
        >
      </div>

      <div class="form-group">
        <label for="type">Room Type</label>
        <select id="type" v-model="room.type" required>
          <option value="Standard">Standard</option>
          <option value="Deluxe">Deluxe</option>
          <option value="Suite">Suite</option>
        </select>
      </div>

      <div class="form-group">
        <label for="capacity">Capacity</label>
        <input 
          type="number" 
          id="capacity" 
          v-model="room.capacity" 
          min="1" 
          required
        >
      </div>

      <div class="form-group">
        <label for="price">Price per Night</label>
        <input 
          type="number" 
          id="price" 
          v-model="room.price" 
          min="0" 
          step="0.01" 
          required
        >
      </div>

      <div class="form-actions">
        <button type="button" @click="$router.push('/rooms')">Cancel</button>
        <button type="submit">{{ isEditing ? 'Update' : 'Create' }}</button>
      </div>
    </form>
  </div>
</template>

<script>
import { roomService } from '@/services/api'

export default {
  name: 'RoomFormView',
  data() {
    return {
      room: {
        number: '',
        type: 'Standard',
        capacity: 1,
        price: 0,
        status: 'available'
      }
    }
  },
  computed: {
    isEditing() {
      return this.$route.params.id !== undefined
    }
  },
  async created() {
    if (this.isEditing) {
      await this.fetchRoom()
    }
  },
  methods: {
    async fetchRoom() {
      try {
        const response = await roomService.getById(this.$route.params.id)
        this.room = response.data
      } catch (error) {
        console.error('Error fetching room:', error)
      }
    },
    async handleSubmit() {
      try {
        if (this.isEditing) {
          await roomService.update(this.$route.params.id, this.room)
        } else {
          await roomService.create(this.room)
        }
        this.$router.push('/rooms')
      } catch (error) {
        console.error('Error saving room:', error)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.room-form {
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