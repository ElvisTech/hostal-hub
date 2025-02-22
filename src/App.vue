<template>
  <div id="app">
    <nav class="navbar">
      <router-link to="/" class="nav-brand">HostalHub</router-link>
      <div class="nav-links">
        <router-link to="/">Home</router-link>
        <router-link to="/rooms">Rooms</router-link>
        <router-link to="/bookings">Bookings</router-link>
        <router-link to="/guests">Guests</router-link>
      </div>
    </nav>
    <router-view/>
  </div>
</template>

<style lang="scss">
.navbar {
  padding: 1rem 2rem;
  background-color: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .nav-brand {
    font-size: 1.5rem;
    font-weight: bold;
    color: white;
    text-decoration: none;
  }

  .nav-links {
    a {
      color: white;
      text-decoration: none;
      margin-left: 1rem;
      
      &.router-link-active {
        color: #42b983;
      }
    }
  }
}

#app {
  font-family: 'Arial', sans-serif;
}
</style>