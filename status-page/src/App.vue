<template>
  <nav>
    <Button value="Log in" @click="() => login_window = !login_window" v-if="!logged_token" />
    <Button value="Add category" @click="() => addcategory_view = !addcategory_view" v-if="logged_try && logged_token" />
    <Button value="Log out" @click="tryLogout" v-if="logged_try && logged_token" />
  </nav>
  <PopupForm
    :style="{ display: login_window ? 'flex' : 'none' }"
    title="Log in"
    :fields="[
      {
        id: 'token',
        label: 'Token',
        type: 'text',
        placeholder: 'Token'
      }
    ]"
    SubmitText="Login"
    @submit="(results) => tryLogin(results['token'])"
    @close="() => login_window = !login_window"
  />
  <PopupForm
    :style="{ display: addcategory_view ? 'flex' : 'none' }"
    title="Add category"
    :fields="[
      {
        id: 'name',
        label: 'Name',
        type: 'text',
        placeholder: 'Name'
      }
    ]"
    SubmitText="Add"
    @submit="(results) => addCategory(results['name'])"
    @close="() => addcategory_view = !addcategory_view"
  />
  <main>
    <h1>Status Page</h1>
    <div class="loading" v-if="!categories">
      <p>Loading categories...</p>
    </div>
    <Category
      v-bind:style="{ order: category.order }"
      v-for="category in categories"
      :id="category.id"
      :name="category.name"
      :admin="admin"
    />
  </main>
</template>

<script>
import Category from './components/Category.vue'
import Button from './components/Button.vue'
import PopupForm from './components/PopupForm.vue'

export default {
  name: 'App',
  components: {
    Category,
    Button,
    PopupForm
  },
  data() {
    return {
      categories: [],
      login_window: false,
      addcategory_view: false,
      logged_token: "",
      logged_try: false
    }
  },
  computed: {
    admin() {
      return this.logged_try && Boolean(this.logged_token)
    }
  },
  methods: {
    getAllCategories() {
      fetch('https://status.sserve.work/api/category', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(async res => {
        this.categories = await res.json()
      }).catch(error => {
        console.log(error)
      })
    },
    tryLogin(cookie_value) {
      document.cookie = 'token=' + cookie_value + ';'
      window.location.reload()
    },
    tryLogout() {
      document.cookie = "token=a;EXPIRES="+new Date(0).toUTCString()
      window.location.reload()
    },
    addCategory(name) {
      fetch(`https://status.sserve.work/api/category?cookie=${/token=([^;]*)/.exec(document.cookie)[1]}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          order: this.categories.length
        })
      }).then(async res => {
        if (res.status === 200) {
          this.getAllCategories()
        } else {
          console.log(await res.json())
        }
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mounted() {
    this.getAllCategories()

    if (document.cookie.includes("token=")) {
      fetch(`https://status.sserve.work/api/auth?cookie=${/token=([^;]*)/.exec(document.cookie)[1]}`, {
        method: 'GET'
      }).then(async res => {
        if (res.status === 200) {
          this.logged_try = true
          this.logged_token = /token=([^=]*)/.exec(document.cookie)[1]
        } else {
          this.logged_try = true
        }
      })
    }
  }
}
</script>

<style>
/*dark theme*/
/*with pretendard font*/

/*noinspection CssUnknownTarget*/
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.6/dist/web/static/pretendard.css");

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,body {
  margin: 0;
  padding: 0;
  font-family: 'Pretendard', sans-serif;
  font-size: 16px;
  background-color: #1e1e1e;
  color: #ffffff;
  overflow-x: hidden;
  overflow-y: auto;
}

html,body,#app {
  width: 100vw;
  height: 100vh;
}

nav {
  background-color: #1e1e1e;
  color: #fff;
  padding: 1rem;
  display: flex;
  justify-content: flex-end;
}

main {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

main h1 {
  font-size: 2rem;
  margin-bottom: 1rem;
}

main h2 {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}
</style>
