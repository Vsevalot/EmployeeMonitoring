import { createApp, initCustomFormatter } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import store from './store'
import 'bootstrap/dist/css/bootstrap.css'
import PrimeVue from 'primevue/config';
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import FloatingVue from 'floating-vue'
import ConfirmationService from 'primevue/confirmationservice';
import Button from "primevue/button"
import ToastService from 'primevue/toastservice';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = 'http://159.223.224.135:8000/api/v1';
// http://159.223.224.135:8000/api/v1
// http://127.0.0.1:8000/api/v1
const app = createApp(App)
app.use(router)
app.use(PrimeVue)
app.use(ConfirmationService);
app.use(ToastService);
app.use(FloatingVue)
app.component('Button', Button);
app.component('DataTable', DataTable)
app.component('Column', Column)
app.use(store)
app.mount('#app')

