<template>
<section class="category">
  <div class="head">
    <h2>{{ name }}</h2>
    <Button value="Add Robot" @click="() => addsite_view = !addsite_view" v-if="admin" />
  </div>
  <PopupForm
    :style="{ display: addsite_view ? 'flex' : 'none' }"
    title="Add Robot"
    :fields="[
      {
        id: 'site-name',
        label: 'Name',
        type: 'text',
        placeholder: 'Name'
      },
      {
        id: 'url',
        label: 'URL',
        type: 'text',
        placeholder: 'URL'
      }
    ]"
    SubmitText="Add"
    @submit="(results) => addSite(results['site-name'], results['url'])"
    @close="() => addsite_view = !addsite_view"
  />
  <Site
    v-for="site in sites"
    :id="site.id"
    :name="site.name"
    :admin="admin"
    v-bind:style="{ order: site.order }"
  />
</section>
</template>

<script>
import Site from './Site.vue'
import Button from './Button.vue'
import PopupForm from './PopupForm.vue'

export default {
  name: "Category",
  components: {
    Site,
    Button,
    PopupForm
  },
  props: {
    id: Number,
    name: String,
    admin: Boolean,
  },
  emits: ['addsite'],
  data() {
    return {
      sites: [],
      addsite_view: false
    }
  },
  methods: {
    getSites() {
      fetch(`https://status.sserve.work/api/category/${this.id}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(async response => {
        this.sites = await response.json()
      }).catch(error => {
        console.log(error)
      })
    },
    addSite(name, url) {
      console.log(name, url)
      fetch(`https://status.sserve.work/api/site?cookie=${/ token=([^;]*)/.exec(document.cookie)[1]}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: name,
          url: url,
          category_id: this.id,
          order: this.sites.length,
          is_active: true
        })
      }).then(async response => {
        if (response.status === 200) {
          this.getSites()
        } else if (response.status === 401) {
          alert("You are not logged in!")
        } else {
          alert("Something went wrong!")
        }
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

section.category .head {
  width: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  border-bottom: 1px solid #eaeaea;
  margin-bottom: 0.5rem;
}

@media screen and (max-width: 400px) {
  section.category {
    width: 100%;
  }

  section.category .head {
    width: 100%;
  }
}
</style>