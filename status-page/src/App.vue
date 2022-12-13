<template>
  <nav>
    <Button value="Log in" />
  </nav>
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
    />
  </main>
</template>

<script>
import Category from './components/Category.vue'
import Button from './components/Button.vue'

export default {
  name: 'App',
  components: {
    Category,
    Button
  },
  data() {
    return {
      categories: []
    }
  },
  methods: {
    getAllCategories() {
      fetch('http://localhost:3000/api/category', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(async res => {
        this.categories = await res.json()
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mounted() {
    this.getAllCategories()
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
}

nav {
  background-color: #1e1e1e;
  color: #fff;
  padding: 1rem;
  display: flex;
  justify-content: flex-end;
}

nav button {
  background-color: #3f3f3f;
  color: #fff;
  border: 1px solid #fff;
  padding: 0.5rem;
  border-radius: 0.25rem;
  cursor: pointer;
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
