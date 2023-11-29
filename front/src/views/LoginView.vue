<template>
    <section class="container">
      <form @submit.prevent="submit">
        <div class="mb-3">
          <label for="email" class="form-label">Почта / Логин:</label>
          <input type="text" name="email" v-model="form.email" class="form-control" />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Пароль:</label>
          <input type="password" name="password" v-model="form.password" class="form-control" />
        </div>
        <button type="submit" class="btn btn-primary">Войти</button>
      </form>
    </section>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import { mapActions } from 'vuex';
  
  export default defineComponent({
    name: 'Login',
    data() {
      return {
        form: {
          email: '',
          password:'',
        }
      };
    },
    methods: {
      ...mapActions(['logIn']),
      async submit() {
        try {
          const User = new FormData();
          User.append('email', this.form.email);
          User.append('password', this.form.password);
          debugger
          const response = await this.logIn(User);
          this.$router.push('/participants');
        } catch {
          alert("Не верный логин или пароль!")
        }
      }
    }
  });
  </script>