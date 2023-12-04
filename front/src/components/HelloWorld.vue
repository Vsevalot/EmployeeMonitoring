<template>
  <div class="description" style="align-items: center;">
    <h2>{{ msg }}</h2>
    <p align="justify">
      Данное приложение отображает статистику по сотрудникам в виде графиков и диаграмм
    </p>
    <h2>Регистрация</h2>
    <p align="justify">
      Для начала необходимо зарегистрироваться в качестве руководителя.
      Для этого нужно нажать кнопку "Зарегистрироваться" и ввести все нужные данные.
    </p>
    <h2>Код для сотрудников</h2>
    <p align="justify">
      После авторизации будет доступен код, который необходимо сообщить сотрудникам для их регистрации.
      При регистрации сотрудником по коду, он будет привязан к руководителю, который его сообщил.
      Руководитель будет иметь возможность смотреть статискику по этому сотруднику.
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
.description {
  width: 40%;
  margin-left: auto;
  margin-right: auto;
}
</style>
