<template>
  <div class="about">
    <h1>This is an login page</h1>
  </div>
</template>


<script>
import axios from 'axios'
export default {
  name: 'login',
  mounted () {
    axios
      .get('/api/v1/auth/login')
      .then( response => {
        console.log(response)
       })
  }
}
</script>