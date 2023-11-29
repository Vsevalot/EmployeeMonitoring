    <template>
        <div class="container">
            <Bar v-if="loaded" :data="chartData" />
        </div>
    </template>
  
  <script>
  import { mapActions } from 'vuex';
  import { Bar } from 'vue-chartjs'
  import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  export default {
    name: 'BarChart',
    components: { Bar },
    data: () => ({
        loaded: false,
        chartData: null
    }),
    methods: {
        ...mapActions(['participantsStats']),
    },
    async mounted () {
        this.loaded = false

        try {
            console.log("test")
            const Dates = new FormData();
            Dates.append('date_from', "1999-01-01");
            Dates.append('date_to', "1999-01-01");
            this.chartdata = await this.participantsStats(Dates);
            //const { userlist } = await fetch('/api/userlist')
            //this.chartdata = userlist

            this.loaded = true
        } catch (e) {
            console.error(e)
        }
    }
  }
  </script>