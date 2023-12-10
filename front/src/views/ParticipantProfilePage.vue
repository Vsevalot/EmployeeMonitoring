<template>
  <div style="text-align:center">
    <h1>{{first_name}} {{ last_name }}</h1>
  </div>
  <div style="text-align:center">
    
    <div class="FormDate" style="display: inline-block">
        <input placeholder="Начало периода" required onfocus="(this.type='date')" name="start_date" v-model="form.start_date" class="form-control inline-item" />
    </div>
    <div class="FormDate" style="display: inline-block">
        <input placeholder="Конец периода" required onfocus="(this.type='date')" name="end_date" v-model="form.end_date" class="form-control inline-item" />
    </div>
  </div>
  
  <div style="text-align:center">
    <button class="btn btn-primary hover:bg-gray-800 mb-5 ms-4 me-4" @click="groupClick()">
      Применить
    </button>
  </div>
  
  <div style="text-align:center">
    <button v-if="loaded" class="btn btn-primary hover:bg-gray-800 mb-5 ms-4 me-4" @click="downloadClick()">
      Скачать
    </button>
  </div>

  <div class="inline-container" style="display: inline-block">
    <div class="charts-container">
      <Bar v-if="loaded" :data="barChartData" :options="barOptions"/>
      <Pie v-if="clicked" :data="pieChartData" :options="pieOptions"/>
    </div>
    <div class="recom-block" style="text-align:justify">
      <Line v-if="loaded" :data="chartData" :options="chartOptions" :type="line"/>

      <h3 style="margin-top: 200px; font-weight: bold;">{{ factor }}</h3>
      <h4>{{ recommendation }}</h4>
    </div>
  </div>
</template>
  
  <script>
  import { groupBy } from "core-js/actual/array/group-by";
  import axios from 'axios';
  import { mapActions } from 'vuex';
  import { Bar, Pie } from 'vue-chartjs';
  import { Line } from 'vue-chartjs';
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, PointElement, LineElement} from 'chart.js';

  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement, PointElement, LineElement);

  
  export default {
    props: ['id', 'first_name', 'last_name'],
    name: 'ParticipantCard',
    components: {
    Line,
    Bar,
    Pie
  },
  data() {
    return {
      form: {
        start_date: '',
        end_date: '',
      },
      description: "Тут будет какое-то описание\nТут будет какое-то описание\nТут будет какое-то описание\nТут будет какое-то описание\nТут будет какое-то описание\n",
      is_exists: true,
      first_name: "",
      pieClicked: false,
      tableValues: null,
      factor: "",
      recommendation: "",
      last_name: "",
      percent_lvl: 0,
      chartData: null,
      chartDataStore: null,
      barChartData: null,
      barOptions: {
        //responsive: true,
        //maintainAspectRatio: false,
        onClick: this.handleChartClick,
        plugins: {
          title: {
            display: true,
            text: "Количество голосов по категории",
            font: {
              size: 18
            }
          },
          legend: {
            display: false,
          },
        },
      },
      loaded: false,
      user: "",
      pieChartData: null,
      clicked: false,
      line: "line",
      pieOptions: {
        //responsive: true,
        //maintainAspectRatio: false,
        onClick: this.handlePieChartClick,
        scales: {
          yAxes: [{
            ticks: {
              fontSize: 400
            }
          }]
        },
        plugins: {
          legend: {
            labels: {
              font: {
                size: 18
              },
              generateLabels: function(chart, qwe) {
                const datasets = chart.data.datasets;
                return datasets[0].data.map((data, i) => ({
                  text: chart.data.labels[i].length < 23 ? chart.data.labels[i] : chart.data.labels[i].slice(0, 23) + '...',
                  fillStyle: datasets[0].backgroundColor[i],
                  index: i,
                  hidden: !chart.getDataVisibility(i),
                }))
              },
              boxWidth: 10,
              fullSize: false,
              display: true,
              position: 'right',
            },
            fullSize: false,
            fullSize: true,
            display: true,
            position: 'right',
            fullSize: true,
          },
          title: {
            display: true,
            text: "Факторы",
            font: {
              size: 18
            },
            padding: {
                top: 150
            }
          }
        },
      },
      chartOptions: {
        responsive: true,
        lineTension: 0.4,
        scales: {
          y: {
            min: 0,
            max: 400,
            ticks: {
              font: {
                size: 14
              },
              callback: function(value, index, values) {
                var yLabels = {
                    0: 'Все очень плохо', 100: 'Плохо', 200: 'Нормально', 300: 'Хорошо', 400: 'Все очень хорошо',
                }
                return yLabels[value];
              }
            }
          },
          x: {
            ticks: {
              maxRotation: 45,
              minRotation: 45,
              font: {
                size: 14
              }
            }
          }
        },
        plugins: {
          legend: {
            labels: {
              font: {
                size: 18
              }
            }
          },
          title: {
            display: true,
            text: "Динамика ответов по дням",
            font: {
              size: 18
            }
          },
        },
      }
    };
  },
    methods: {
      ...mapActions(['participantStats', 'sendGetUserRequest', 'getUserScore', 'downloadFileForOne']),

      handlePieChartClick(evt, array) {
        try {
          let factor = this.pieChartData.labels[array[0].index]
          let needed_id = this.pieChartData.datasets[0].ids_data[array[0].index]
          let recommendation = this.pieChartData.datasets[0].recommendation[array[0].index];
          this.factor = "Фактор - " + factor
          this.recommendation = "Рекомендация - " + recommendation
          this.tableValues = [{ factor: factor, recommendation: recommendation}];
          this.pieClicked = true;
        } catch {

        }
      },

      handleChartClick(evt, array) {
        try {
          let test = this.chartDataStore[array[0].index]["factors"]
          const colors = ["#A101A6", "#E20048", "#510FAD", "#CFF700", "#68006C", "#93002F", "#8144D6"]
          const unpacked_data = this.chartDataStore.filter(value => value.factor).map((value) => ({morning: value.morningm, evening: value.evening, date: value.date, factor_id: value.factor.id, factor_name: value.factor.name, factor_cat: value.factor.category, factor_recommendation: value.factor.recommendation}))
          const grouped_data = Object.entries(unpacked_data.groupBy(item => item.factor_name)).filter(value => value[1][0].factor_cat == this.barChartData.labels[array[0].index]).map((item, key) => ({
            factor_name: item[1][0].factor_name,
            voted_count: item[1].length,
            id: item[1][0].factor_id,
            recommendation: item[1][0].factor_recommendation
          }))
          this.pieOptions["plugins"]["title"]["text"] = this.barChartData["labels"][array[0].index]
          this.pieChartData = {
            labels: Object.entries(grouped_data).map((value) => value[1].factor_name),
            datasets: [
              {
                label: "Количество голосов по фактору",
                data: Object.entries(grouped_data).map((value) => value[1].voted_count),
                backgroundColor: colors,
                ids_data: grouped_data.map((value) => value["id"]),
                recommendation: grouped_data.map((value) => value["recommendation"]),
              }
            ]
          }
          this.clicked = true
        } catch {
          
        }
      },
      async downloadClick() {
        const Data = new FormData();
        Data.append('date_from', this.form.start_date);
        Data.append('date_to', this.form.end_date);
        Data.append('id', this.id);
        Data.append('fio', this.first_name + '_' + this.last_name);
        await this.downloadFileForOne(Data);
      },
      async groupClick() {
        const Data = new FormData();
        Data.append('date_from', this.form.start_date);
        Data.append('date_to', this.form.end_date);
        Data.append('id', this.id)
        this.$router.replace({ name: "current_participants", query: {date_from: this.form.start_date, date_to: this.form.end_date} })
        let response = null
        try {
          response = await this.participantStats(Data);
        } catch {
          alert("Введите корректные даты!")
          return
        }
        this.chartDataStore = response.data["result"]
        const dates = this.chartDataStore.map(item => item["date"])
        const morning = []
        const evening = []
        for (let i = 0; i < this.chartDataStore.length; i++) {
          if (this.chartDataStore[i]["morning"] == null) {
            morning.push(null)
          } else {
            morning.push(this.chartDataStore[i]["morning"]["value"])
          }
          if (this.chartDataStore[i]["evening"] == null) {
            evening.push(null)
          } else {
            evening.push(this.chartDataStore[i]["evening"]["value"])
          }
        }
        //const morning = this.chartDataStore.map(item => item["morning"]["value"])
        //const evening = this.chartDataStore.map(item => item["evening"]["value"])
        
        
        console.log(response)
        this.chartData = {
          labels: dates,
          datasets: [
            {
              label: 'Утро',
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: morning,
              borderColor: 'rgba(255, 56, 96, 0.5)',
              backgroundColor: 'rgba(255, 56, 96, 0.1)',
            },
            {
              label: 'Вечер',
              pointBackgroundColor: 'white',
              borderWidth: 1,
              pointBorderColor: '#249EBF',
              data: evening,
              borderColor: 'rgba(50, 115, 220, 0.5)',
              backgroundColor: 'rgba(50, 115, 220, 0.1)',
            }
          ],
        }
        const colors = ["#191970", "#00BFFF", "#008B8B", "#FFA07A"]
        const unpacked_data = this.chartDataStore.filter(value => value.factor).map((value) => ({morning: value.morningm, evening: value.evening, date: value.date, factor_id: value.factor.id, factor_name: value.factor.name, factor_cat: value.factor.category}))
        const grouped_data = Object.entries(unpacked_data.groupBy(item => item.factor_cat)).map((item, key) => ({
          category_name: item[1][0].factor_cat,
          voted_count: item[1].length
        }))
        this.barChartData = {
          labels: Object.entries(grouped_data).map((value) => value[1].category_name),
          datasets: [
            {
              label: "Количество голосов по категории",
              data: Object.entries(grouped_data).map((value) => value[1].voted_count),
              backgroundColor: colors
            },
          ]
        }
        this.loaded = true
      },
      async getUser() {
        console.log(this.isLoggedIn)
        const Data = new FormData();
        Data.append('user_id', this.id);
        const response = await this.sendGetUserRequest(Data);
        this.first_name = response.data.result.first_name;
        this.last_name = response.data.result.last_name;
        const user_score = await this.getUserScore(Data);
        this.percent_lvl = user_score.percent;
        this.description = user_score.recommendation;
      },
      async userClick(user_id) {
        this.$router.push('/participants/' + user_id);
      }
    },
    computed : {
    isLoggedIn: async function() {
      return await this.$store.getters.isAuthenticated;
    }
  },
    async created() {
      if (!await this.isLoggedIn) {
        this.$router.push("/login")
        return
      }
      if (this.$route.query.date_from) {
        this.form.start_date = this.$route.query.date_from
      }

      if (this.$route.query.date_to) {
        this.form.end_date = this.$route.query.date_to
      }

      if (this.$route.query.date_from && this.$route.query.date_to) {
        this.groupClick();
      }
      this.getUser();
    },
  };
  </script>

<style lang="scss">
.FormDate {
  $spacing: 0.75em;
  margin: 1rem;
  display: inline-block;
  position: relative;
  overflow: hidden;
  border: 1px solid #888;
  border-radius: 0.25em;

  // 1. Hide the spinner button in Chrome, Safari and Firefox.
  &__input {
    padding: $spacing;
    padding-right: $spacing / 2;
    padding-left: $spacing / 2;
    border: none;
    text-align: center;
    /* stylelint-disable-next-line property-no-vendor-prefix */
    -moz-appearance: textfield; // 1

    &::-webkit-inner-spin-button {
      display: none; // 1
    }

    &:first-child {
      padding-left: $spacing;
    }

    &:last-child {
      padding-right: $spacing;
    }

    &:focus {
      outline: none;
    }

    &--day,
    &--month {
      width: 3em;
    }

    &--year {
      width: 4em;
    }
  }

  &__divider {
    padding-top: $spacing;
    padding-bottom: $spacing;
    pointer-events: none;
  }
}

.inline-container {
    text-align: center; /* выравнивание по центру */
    margin-bottom: 20px;
    width: 100%; /* отступ снизу */
}

.inline-item {
    vertical-align:top;
    display: inline-block; /* отобразить элементы в строку */
    width: max-content; /* ширина блока */
    height: 45%; /* высота блока */
    margin-left: 20px; /* промежутки между блоками */
}
.customtooltip {
  width: 350px;
  color: black;
}


.liner-block {
  width: max-content;
}

.recomm-block {
  margin-top: 10%;
}

.max-width {
  width: 100%;
  height: 100%;
}

</style>