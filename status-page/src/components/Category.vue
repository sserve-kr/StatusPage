<template>
<section class="category">
  <h2>{{ name }}</h2>
  <Site
    v-for="site in sites"
    :id="site.id"
    :name="site.name"
    v-bind:style="{ order: site.order }"
  />
</section>
</template>

<script>
import Site from './Site.vue'

export default {
  name: "Category",
  components: {
    Site
  },
  props: {
    id: Number,
    name: String
  },
  data() {
    return {
      sites: []
    }
  },
  methods: {
    getSites() {
      fetch(`http://localhost:3000/api/category/${this.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(async response => {
        this.sites = await response.json()
      }).catch(error => {
        console.log(error)
      })
    }
  },
  mounted() {
    this.getSites()
  }
}
</script>

<style scoped>
section.category {
  width: 90%;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0 2rem 0;
}

section.category h2 {
  width: 80%;
  border-bottom: 1px solid #eaeaea;
}
</style>