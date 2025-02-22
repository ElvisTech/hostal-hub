<template>
  <div class="guest-form">
    <h2>{{ isEditing ? 'Edit Guest' : 'New Guest' }}</h2>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label for="firstName">First Name</label>
        <input 
          type="text" 
          id="firstName" 
          v-model="guest.first_name" 
          required
        >
      </div>

      <div class="form-group">
        <label for="lastName">Last Name</label>
        <input 
          type="text" 
          id="lastName" 
          v-model="guest.last_name" 
          required
        >
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input 
          type="email" 
          id="email" 
          v-model="guest.email" 
          required
        >
      </div>

      <div class="form-group">
        <label for="phone">Phone</label>
        <input 
          type="tel" 
          id="phone" 
          v-model="guest.phone" 
          required
        >
      </div>

      <div class="form-group">
        <label for="country">Country</label>
        <input 
          type="text" 
          id="country" 
          v-model="guest.country" 
          required
        >
      </div>

      <div class="form-group">
        <label for="documentId">Document ID</label>
        <input 
          type="text" 
          id="documentId" 
          v-model="guest.document_id" 
          required
        >
      </div>

      <div class="form-actions">
        <button type="button" @click="$router.push('/guests')">Cancel</button>
        <button type="submit">{{ isEditing ? 'Update' : 'Create' }}</button>
      </div>
    </form>
  </div>
</template>

<script>
import { guestService } from '@/services/api'

export default {
  name: 'GuestFormView',
  data() {
    return {
      guest: {
        first_name: '',
        last_name: '',
        email: '',
        phone: '',
        country: '',
        document_id: ''
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
      await this.fetchGuest()
    }
  },
  methods: {
    async fetchGuest() {
      try {
        const response = await guestService.getById(this.$route.params.id)
        this.guest = response.data
      } catch (error) {
        console.error('Error fetching guest:', error)
      }
    },
    async handleSubmit() {
      try {
        if (this.isEditing) {
          await guestService.update(this.$route.params.id, this.guest)
        } else {
          await guestService.create(this.guest)
        }
        this.$router.push('/guests')
      } catch (error) {
        console.error('Error saving guest:', error)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.guest-form {
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

    input {
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