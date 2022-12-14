<template>
<article class="site">
  <h3>{{name}}</h3>
  <Button
      v-if="admin"
      value="Delete"
      @click="deleteSite"
  />
  <div class="response">
    <div
        v-for="res in filteredResponses"
        :data-code="res.code"
        :data-restime="res.response_time"
        :class="{ 'success': res.success, 'fail': !res.success, 'no': res.code === 0 }"
    />
  </div>
</article>
</template>

<script>
import Button from './Button.vue'

export default {
  name: "Site",
  props: {
    id: Number,
    name: String,
    admin: Boolean,
  },
  components: {
    Button,
  },
  data() {
    return {
      responses: [],
      intervals: [['24h', 480], ['7d', 3360]],
      interval_selection: 0
    }
  },
  methods: {
    getResponses() {
      fetch(`http://localhost:3000/api/site/${this.$props.id}/response?limit=${this.intervals[this.interval_selection][1]}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(async response => {
        this.responses = await response.json()
      }).catch(error => {
        console.log(error)
      })
    },
    deleteSite() {
      fetch(`http://localhost:3000/api/site/${this.$props.id}?cookie=${/ token=([^;]*)/.exec(document.cookie)[1]}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(async response => {
        window.location.reload()
      }).catch(error => {
        console.log(error)
      })
    }
  },
  computed: {
    filteredResponses() {
      let filter = this.responses.filter((response, index) => {
        if (this.intervals[this.interval_selection][0] === '24h') {
          return index % 48 === 0
        } else if (this.intervals[this.interval_selection][0] === '7d') {
          return index % 336 === 0
        }
      })

      while (filter.length < 10) {
        for (let i = 0; i < 10 - filter.length; i++) {
          filter.unshift({
            code: 0,
            success: false,
            response_time: 0
          })
        }
      }

      return filter
    }
  },
  mounted() {
    this.getResponses()
  },
}
</script>

<style scoped>
article.site {
  width: 80%;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  margin: 0 0 0.5rem 0;
  padding: 1.5rem 1rem;
  border-radius: 0.5rem;
  background-color: #0f0f0f;
}

@media screen and (max-width: 400px) {
  article.site {
    width: 100%;
  }
}

article.site div.response {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  gap: 4px;
}

article.site div.response div {
  position: relative;
  width: 8px;
  height: 20px;
  border-radius: 10px;

  transition: width 0.2s ease-in-out;
}

article.site div.response div:hover {
  cursor: pointer;
  width: 12px;

  transition: width 0.2s ease-in-out;
}

article.site div.response div::after {
  content: attr(data-code) " | " attr(data-restime) "ms";
  position: absolute;
  top: 20px;
  left: 0;
  width: 10px;
  background-color: #fff;
  color: #000;
  padding: 0.5rem;
  border-radius: 10px;
  opacity: 0;
  font-family: "Pretendard", sans-serif;
  font-size: 14px;
  font-weight: 600;
  white-space: nowrap;
  transition: 0.2s ease-in-out;
}

article.site div.response div:hover::after {
  opacity: 1;
  width: 120px;
  transition: 0.1s ease-in-out;
}

article.site div.response div.no {
  background-color: #000000 !important;
}

article.site div.response div.success {
  background-color: #00ff00;
}

article.site div.response div.fail {
  background-color: #ff0000;
}
</style>