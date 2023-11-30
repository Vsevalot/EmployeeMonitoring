<template>
    <header>
      <nav class="navbar navbar-expand-md navbar-dark blue">
        <div class="container">
          <a href="https://urfu.ru/ru/" class="navbar-left logo"><img src="https://keys.urfu.ru/auth/resources/xry12/login/keycloak.v3/img/urfu_logo.svg"></a>
          <a class="navbar-brand buttontest text logo" href="/">Панель администратора</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul v-if="isLoggedIn" class="navbar-nav me-auto mb-2 mb-md-0 backtest raz">
              <li class="nav-item">
                <router-link class="nav-link buttontest text" to="/">Главная</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link buttontest text" to="/participants">Участники</router-link>
              </li>

              <li v-on:click="seen = !seen" v-if="seen" @click="getMe" class="nav-item code">
                  <a class="nav-link buttontest text">Показать код</a>
              </li>
              <li v-if="!seen" v-on:click="seen = !seen" class="nav-item code">
                <VTooltip>
                  <a class="nav-link text buttontest">{{code}} </a>
                  <template #popper>
                    Назовите данный код сотрудникам для их регистрации.
                  </template>
                </VTooltip>
              </li>

              <close class="nav-item">
                <a class="nav-link buttontest text" @click="logout">Выйти</a>
              </close>
            </ul>
            <ul v-else class="navbar-nav me-auto mb-2 mb-md-0 backtest raz">
              <li class="nav-item">
                <router-link class="nav-link buttontest text" to="/">Главная</router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link buttontest text" to="/register/managers">Зарегистрироваться</router-link>
              </li>
              <li class="nav-item logout">
                <router-link class="nav-link buttontest text" to="/login">Войти</router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  </template>
  
  <script>
  import { defineComponent } from 'vue';
  import { mapActions } from 'vuex';
  import 'floating-vue/dist/style.css'

  export default defineComponent({
    name: 'NavBar',
    data() {
    return {
      seen: true,
      code: "",
      isLoggedIn: false,
    };
  },
    created: async function() {
      this.isLoggedIn = await this.$store.getters.isAuthenticated;
    },
    methods: {
      ...mapActions(['sendMeRequest']),
      async logout () {
        await this.$store.dispatch('logOut');
        this.$router.go('/login');
        this.$forceUpdate();
      },
      async getMe () {
        const response = await this.sendMeRequest();
        this.code = response.data.result.code;
      },
    },
  });
  </script>
  
  <style scoped>
  a {
    cursor: pointer;
  }
  .blue {
    background: rgb(184, 193, 212);
  }
  .logo {
    margin-right: 50px;
  }
  .code {
    margin-left: auto;
    margin-right: auto;
  } 

  .logout {
    margin-left: auto;
  } 

  .backtest {
    width: 100%;
  }
  .text {
    color: black;
  }
  .buttontest:hover {
    color:rgb(192, 84, 84)
  }
  .buttontest:focus {
    color:rgb(192, 84, 84)
  }
  .raz close {
    margin-left: auto;
  }
  </style>