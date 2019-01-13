<template>
  <div class="home">
    <UserInfo/>
  </div>
</template>

<script>
// @ is an alias to /src
import UserInfo from '@/components/UserInfo.vue'

export default {
  name: 'home',
  components: {
    UserInfo
  }
}
</script>
