import SystemList from '@/components/admin/systems/List'
import SystemNew from '@/components/admin/systems/New'


const Admin = {
  template: `
    <div class="admin">
      <b-navbar toggleable="md" type="dark" variant="primary">
        <b-navbar-nav>
          <b-nav-item-dropdown text="Systems">
            <b-dropdown-item to="/admin/systems">List</b-dropdown-item>
            <b-dropdown-item to="/admin/systems/new">New</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-navbar>
      <router-view></router-view>
    </div>
  `
}

export default {
  path: '',
  component: Admin,
  children: [
    {
      path: 'systems',
      name: 'SystemList',
      component: SystemList
    },
    {
      path: 'systems/new',
      name: 'SystemNew',
      component: SystemNew
    }
  ]
}
