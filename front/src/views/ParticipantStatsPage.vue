<template>
  <div style="text-align:center">
    <h1>Организация: {{ company }}</h1>
    <div v-if="is_exists" style="text-align:center">
    <VDropdown :showTriggers="triggers => [...triggers, 'hover']">
      <h1>Уровень благополучия: {{ percent_lvl }}%</h1>
      <template #popper>
        <h5 class="customtooltip" v-close-popper>{{ description }}</h5>
      </template>
    </VDropdown>
    </div>
    <div v-else style="text-align:center">
      <VTooltip :placements="right-start">
        <h2>Недостаточно данных для определения уровня благополучия</h2>
        <template #popper>
          Необходимо отмечать состояние на протяжение месяца (а также выбрать интервал более 1 месяца).
        </template>
      </VTooltip>
    </div>
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

  <div>
    <div style="align-content: center;" class="column-container chart-block">
      <div class="column-item">
        <Bar v-if="loaded" :data="chartData" :options="barOptions"/>
      </div>
      <div class="column-item">
        <Pie v-if="clicked" :data="chartPieData" :options="pieOptions"/>
      </div>
    </div>
    
    <DataTable v-if="pieClicked" :value="tableValues" class="recom-block">
        <Column field="factor" header="Фактор"></Column>
        <Column field="recommendation" header="Рекомендация"></Column>
    </DataTable>
</div>
</template>

<script>
import { mapActions } from 'vuex';
import { Bar, Pie } from 'vue-chartjs';
import { DataTable } from 'primevue/datatable';
import { Column } from 'primevue/column';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, ArcElement);
export default {
  name: `FormDate`,
  components: {
    Bar,
    Pie,
    DataTable,
    Column
  },
  data() {
    return {
      form: {
        start_date: '',
        end_date: '',
      },
      is_exists: false,
      percent_lvl: 0,
      description: "Выберите диапазон дат для получения уровня благополучия",
      company: "",
      chartData: null,
      chartPieData: null,
      chartDataStore: null,
      loaded: false,
      clicked: false,
      pieClicked: false,
      barOptions: {
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
      pieOptions: {
        onClick: this.handlePieChartClick,
        
        plugins: {
          legend: {
            labels: {
              font: {
                size: 18
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
      tableValues: null
    };
  },
  mounted() {
    this.tableValues = [{
        "Рекомендация": "Что-то там",
        "Фактор": "Обратились на ты"
      },{
        "Рекомендация": "Что-то там",
        "Фактор": "Обратились на ты"
      },{
        "Рекомендация": "Что-то там",
        "Фактор": "Обратились на ты"
      },]
  }
  ,
  methods: {
    ...mapActions(['participantsStats', 'sendMeRequest', 'getGroupScore', 'downloadFileForGroup']),
    async downloadClick() {
      const Data = new FormData();
      Data.append('date_from', this.form.start_date);
      Data.append('date_to', this.form.end_date);
      await this.downloadFileForGroup(Data);
    },
    handleChartClick(evt, array) {
      try {
        debugger
        let test = this.chartDataStore[array[0].index]["factors"]
        const colors = ["#8bf759", "#d8f759", "#f75976", "#f7d559", "#59edf7", "#5998f7"]
        this.pieOptions["plugins"]["title"]["text"] =  this.chartDataStore[array[0].index]["category"]
        this.chartPieData = {
          labels: test.map((value) => value["name"]),
          datasets: [
            {
              label: "Количество голосов по фактору",
              data: test.map((value) => value["voted"]),
              ids_data: test.map((value) => value["id"]),
              backgroundColor: colors
            },
          ]
        }
        this.clicked = true
      } catch {

      }
    },
    handlePieChartClick(evt, array) {
      try {
        let factor = this.chartPieData.labels[array[0].index]
        let needed_id = this.chartPieData.datasets[0].ids_data[array[0].index]
        let recommendation = "";
        
        for(let i = 0; i < this.chartDataStore.length; i++) {
          let cat_data = this.chartDataStore[i].factors;
          for (let j = 0; j < cat_data.length; j++) {
            if (cat_data[j].id == needed_id) {
              recommendation = cat_data[j].recommendation;
            }
          }
        }
        this.tableValues = [{ factor: factor, recommendation: recommendation}];
        this.pieClicked = true;
      } catch {
        
      }
    },
    async groupClick() {
      debugger
      this.clicked = false;
      this.pieClicked = false;
      this.is_exists = false;

      this.description = "Выберите диапазон дат для получения уровня благополучия";

      const Dates = new FormData();
      Dates.append('date_from', this.form.start_date);
      Dates.append('date_to', this.form.end_date);
      const response = await this.participantsStats(Dates);
      const colors = ["#8bf759", "#d8f759", "#f75976", "#f7d559", "#59edf7", "#5998f7"]
      this.chartDataStore = response.data["result"]
      const happines = response.data["happiness"]
      
      if (happines != null) {
        this.percent_lvl = happines.percent;
        this.description = happines.recommendation;
        this.is_exists = true;
      }

      let current_data = {}
      debugger
      for(let i = 0; i < this.chartDataStore.length; i++) {
        let cat_data = this.chartDataStore[i];
        current_data[cat_data["category"]] = Array.from(cat_data["factors"]).reduce((acc, c_v) => acc + c_v["voted"], 0);
      }
      this.chartData = {
        labels: Object.entries(current_data).map((value) => value[0]),
        datasets: [
          {
            label: "Количество голосов по категории",
            data: Object.entries(current_data).map((value) => value[1]),
            backgroundColor: colors
          }
        ]
      }
      this.loaded = true
  },
    async getMe() {
      debugger
      const response = await this.sendMeRequest();
      this.company = response.data.result.company;
    },
  },
  
  computed : {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
  created() {
    this.getMe();
  },
};
</script>

<style lang="scss">
.FormDate {
  $spacing: 0.75em;
  margin: 1rem;
  width: 300px;
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
    display: inline-block; 
    text-align: center; /* выравнивание по центру */
    margin-bottom: 20px;
    width: 100%; /* отступ снизу */
}

.recom-block {
    vertical-align:top;
    display: inline-block; /* отобразить элементы в строку */
    width: 35%; /* ширина блока */
    height: 35%; /* высота блока */
    margin-left: 20px; /* промежутки между блоками */
}

.chart-block {
    vertical-align:top;
    display: inline-block; /* отобразить элементы в строку */
    width: 50%; /* ширина блока */
    height: 35%; /* высота блока */
    margin-left: 20px; /* промежутки между блоками */
}

.column-item {
    margin-left: auto;
    margin-right: auto;
    width: 60%; /* ширина блока */
    height: 25%; /* высота блока */
}

.column-container {
    flex-direction: column;
}
</style>