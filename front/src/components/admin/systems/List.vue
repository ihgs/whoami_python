<template>
  <div class="systems">
    System listaaa
    <div v-if="systems">
      <b-table striped hover :items="systems" caption="Systems" :fields="fields" caption-top>
        <template slot="action" slot-scope="data">
          <div v-if="data.item.use">
            <b-button variant="danger" @click="unuse(data.item.id)">Unuse</b-button>
          </div>
          <div v-else>
            <b-button variant="primary" v-b-modal.useModal @click="setInfo(data.item)">Use</b-button>
          </div>
        </template>
      </b-table>
      <b-modal  id="useModal"
                title="Input your info for the system"
                @ok="handleOk"
                >
        <form>
          {{targetSystem.name}}
          <b-form-input type="text" placeholder="LoginId" v-model="targetSystem.loginId">
          </b-form-input>
        </form>
      </b-modal>
    </div>
    <div v-else>
      Now loading....
    </div>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
export default {
  name: 'AdminSystemList',
  data () {
    return {
      fields: ['name', 'action'],
      systems: null,
      targetSystem: {},
    }
  },
  methods: {
    setInfo: function (data) {
      Vue.set(this.targetSystem, 'loginId', null)
      Vue.set(this.targetSystem, 'id', data.id)
      Vue.set(this.targetSystem, 'name', data.name)
    },
    handleOk: function () {
      this.use(this.targetSystem.id, this.targetSystem.loginId)
    },
    reload () {
      this.systems = null
      axios
        .get('/api/v1/systems')
        .then( response => {
          this.systems = response.data
        })
    }
  },
  mounted () {
    this.reload()
  }
}
</script>

<style scoped>
</style>
