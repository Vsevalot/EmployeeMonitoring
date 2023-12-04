<template>
  <div class="home" style="text-align:center">
    <HelloWorld msg="Приложение для мониторинга состояния сотрудников на рабочем месте."/>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  },
  computed : {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
  created() {
    if (!this.isLoggedIn) {
      this.$router.push('/login');
    }
  }
}
</script>
