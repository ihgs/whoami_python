<template>
  <div>
    New system
    <b-alert variant="success" :show="showSuccess">Success</b-alert>
    <b-form>
      <b-card>
        <vue-form-generator :schema="schema" :model="system" :options="formOptions" @validated="onValidated"></vue-form-generator>
      </b-card>
      <b-btn @click="save" :disabled="invalid">Create</b-btn>
    </b-form>
  </div>
</template>

<script>
import axios from 'axios'
import schema from './schema'

export default {
  name: 'SystemNew',
  data: function () {
    return {
      schema: schema.system,
      system: {},
      formOptions: {
        validateAfterLoad: false,
        validateAfterChanged: true
      },
      invalid: true,
      showSuccess: false
    }
  },
  methods: {
    save: function () {
      console.log(this.system)
      axios
        .post('/api/v1/systems', this.system)
        .then( () => {
          this.system = {}
          this.$router.push('/admin/systems')
        })
    },
    onValidated (isValid, errors) {
      this.invalid = !isValid
    }
  }
}
</script>

<style>

</style>
