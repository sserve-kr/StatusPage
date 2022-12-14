<template>
<div class="form">
  <form>
    <div class="head">
      <h1>{{ title }}</h1>
      <Button @click="() => this.$emit('close')" value="close" />
    </div>
    <div class="form-control" v-for="field in fields">
      <label :for="field['id']">{{ field['label'] }}</label>
      <input :type="field['type']" :placeholder="field['placeholder']" :id="field['id']" />
    </div>
    <Button @click="submit" :value="SubmitText" class="submit" />
  </form>
</div>
</template>

<script>
import Button from './Button.vue'

export default {
  name: "PopupForm",
  components: {
    Button
  },
  props: {
    title: String,
    fields: Array,
    SubmitText: String,
  },
  emits: ["submit", "close"],
  methods: {
    submit(e) {
      e.preventDefault()
      new Promise((resolve, reject) => {
        let results = {}
        for (let field of this.fields) {
          results[field['id']] = document.getElementById(field['id']).value
        }
        resolve(results)
      }).then((results) => {
        this.$emit('submit', results)
      })
    },
  }
}
</script>

<style scoped>
div.form {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

div.form form {
  background-color: #1e1e1e;
  color: #fff;
  padding: 1rem;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 320px;
}

div.form form .head {
  margin-bottom: 1rem;
  width: 100%;

  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

div.form form .form-control {
  width: 100%;
  display: flex;
  flex-direction: column;
  margin: 0.5rem 0;
}

div.form form .form-control label {
  margin-bottom: 0.5rem;
}
div.form form .form-control input {
  padding: 0.5rem;
  border-radius: 0.5rem;
  border: none;
  background-color: #000000;
  color: #fff;
}

div.form form .submit {
  margin-top: 1rem;
}
</style>