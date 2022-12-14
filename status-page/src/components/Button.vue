<template>
<button>{{ value }}</button>
</template>

<script>
export default {
  name: "Button",
  props: {
    value: String
  }
}
</script>

<style scoped>
button {
  background-color: #1e1e1e;
  color: #fff;
  border: 1px solid #fff;
  border-radius: 0.5rem;
  padding: 0.5rem 1rem;
  font-family: "Pretendard", sans-serif;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-decoration: underline;
  max-height: 35px;
}
</style>