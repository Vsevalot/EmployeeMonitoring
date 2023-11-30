<template>
    <section class="container">
      <form @submit.prevent="submit">
        <div class="mb-3 inline-container">
          <input type="text" name="first_name" required placeholder="Имя" v-model="form.first_name" class="form-control inline-item" />
        </div>
        
        <div class="mb-3 inline-container">
          <input type="text" name="last_name" required placeholder="Фамилия" v-model="form.last_name" class="form-control inline-item" />
        </div>
        
        <div class="mb-3 inline-container">
          <input type="text" name="surname" required placeholder="Отчество" v-model="form.surname" class="form-control inline-item" />
        </div>
      
        <div class="mb-3 inline-container">
          <input placeholder="Дата рождения" required onfocus="(this.type='date')" name="birthdate" v-model="form.birthdate" class="form-control inline-item" />
        </div>
        
        <div class="mb-3 inline-container">
          <input type="text" name="phone" required placeholder="Телефон" v-model="form.phone" class="form-control inline-item" />
        </div>
        
        <div class="mb-3 inline-container">
          <input type="text" name="position" required placeholder="Должность" v-model="form.position" class="form-control inline-item" />
        </div>
        
        <div class="mb-3 inline-container">
          <input type="text" name="email" required placeholder="Почта" v-model="form.email" class="form-control inline-item" />
        </div>
        
        <div class="mb-3 inline-container">
          <input type="password" name="password" required placeholder="Пароль" v-model="form.password" class="form-control inline-item"/>
        </div>
        
        <div class="mb-3 inline-container">
          <input type="password" name="repeat_password" required placeholder="Повторите пароль" v-model="form.repeat_password" class="form-control inline-item"/>
        </div>

        <div class="mb-3 inline-container">
          <input type="text" name="company" required placeholder="Организация" v-model="form.company" class="form-control inline-item" />
        </div>

        <div class="mb-3 inline-container">
          <input type="text" name="department" required placeholder="Отдел" v-model="form.department" class="form-control inline-item" />
        </div>
        <button style="text-align:center" type="submit" class="btn btn-primary">Зарегистрироваться</button>
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
          first_name: '',
          last_name: '',
          surname: '',
          birthdate: '',
          phone: '',
          position:'',
          email: '',
          password: '',
          personal_data_confirmed: true,
          company: '',
          department: '',
        }
      };
    },
    methods: {
      ...mapActions(['register']),
      async submit() {
        if (this.form.password != this.form.repeat_password) {
          alert("Пароли не совпадают!")
          return
        }
        try {
          const User = new FormData();
          User.append('first_name', this.form.first_name);
          User.append('last_name', this.form.last_name);
          User.append('surname', this.form.surname);
          User.append('birthdate', this.form.birthdate);
          User.append('phone', this.form.phone);
          User.append('position', this.form.position);
          User.append('email', this.form.email);
          User.append('password', this.form.password);
          User.append('personal_data_confirmed', this.form.personal_data_confirmed);
          User.append('company', this.form.company);
          User.append('department', this.form.department);
          await this.register(User);
          this.$router.push('/');
        } catch {
          alert("Проверьте все данные на корректность! Возможно такой login уже существует")
        }
      },
    }
  });
  </script>

  <style>
  .inline-container {
    text-align: center; /* выравнивание по центру */
    margin-bottom: 20px;
    width: 100%; /* отступ снизу */
}

.inline-item {
    vertical-align:top;
    display: inline-block; /* отобразить элементы в строку */
    width: 25%; /* ширина блока */
    height: 45%; /* высота блока */
    margin-left: 2px; /* промежутки между блоками */
}
.inline-title {
    vertical-align:top;
    display: inline-block; /* отобразить элементы в строку */
    width: 10%; /* ширина блока */
    height: 10%; /* высота блока */
    margin-left: 2px; /* промежутки между блоками */
}
</style>