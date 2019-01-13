<template>
  <div class="userinfo">
    <div v-if="info">
      <h1>{{ info.userid }}</h1>
      <b-table striped hover :items="info.systems" caption="Systems" caption-top></b-table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserInfo',
  data () {
    return {
      info: null
    }
  },
  mounted () {
    axios
      .get('/api/v1/userinfo')
      .then( response => {
        this.info = response.data.userinfo
       })
  }
}
</script>

<style scoped>
</style>
