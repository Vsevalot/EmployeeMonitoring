<template>
    <header>
      <nav class="navbar navbar-expand-md navbar-dark blue">
        <div class="container">
          <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav me-auto mb-2 mb-md-0 backtest raz">
              <li class="nav-item">
                <a class="nav-link buttontest text" to="/">©ФГАОУ ВО «УрФУ имени первого Президента России Б.Н. Ельцина»</a>
              </li>

              <close class="nav-item" style="display: flex; width: 700px;">
                <div style="display: inline;">
                  <a class="nav-link buttontest text">Федорова Алена Эдуардовна</a>
                  <img src="https://urfu.ru/fileadmin/_processed_/2/6/csm_40980d7e59f6a7d06b2fff0e944bfb36_94bff0a278.jpg">
                </div>

                <div style="display: inline;margin-left: 100px;">
                  <a class="nav-link buttontest text">Морохов Никита Дмитриевич</a>
                  <a class="nav-link buttontest text">+79221546763, n.morohov@yandex.ru</a>
                </div>
              </close>
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
    name: 'Footer',
    data() {
    return {
      seen: true,
      code: ""
    };
  },
    computed: {
      isLoggedIn: function() {
        console.log(this.$store.getters.isAuthenticated)
        return this.$store.getters.isAuthenticated;
      }
    },
    methods: {
      ...mapActions(['sendMeRequest']),
      async logout () {
        await this.$store.dispatch('logOut');
        this.$router.push('/login');
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
    background: rgb(56, 59, 63);
  }
  .logo {
    margin-right: 50px;
  }
  .code {
    margin-left: auto;
    margin-right: auto;
  } 

  .backtest {
    width: 100%;
  }
  .text {
    color: rgb(250, 246, 246);
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