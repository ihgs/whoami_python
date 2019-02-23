<template>
  <div class="about">
    <h1>Login page</h1>
    <b-form>
      <b-form-group
        id="useridGroup"
        label="userid">
        <b-form-input
          id="userid"
          v-model="form.userid">
        </b-form-input>
      </b-form-group>
      <b-form-group
        id="passwordGroup"
        label="password">
        <b-form-input
          id="password"
          type="password"
          v-model="form.password">
        </b-form-input>
        <b-button variant="primary" @click="onSubmit">Submit</b-button>
      </b-form-group>
    </b-form>
  </div>
</template>


<script>
import axios from 'axios'
export default {
  name: 'login',
  data() {
    return {
      form: {
        userid: '',
        password: ''
      }
    }
  },
  methods: {
    onSubmit: function(){
      console.log('aaa')
      axios.post('/api/v1/auth/login', this.form)
      .then( (response) => {
        console.log(response.headers['set-cookie'])
        this.$store.commit('login')
        this.$router.push(this.$route.query.redirect)
      })
    }
  }
}
</script>