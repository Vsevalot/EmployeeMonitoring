import axios from 'axios';
import Cookies from 'js-cookie'

const state = {
  token: Cookies.get('token'),
};

const getters = {
  isAuthenticated: async (state) => {
    try {
      const response = await axios.get('participants/me', {headers: { Authorization: state.token }})
      return !!state.token
    } catch {
      return false
    }
  },
  userToken: state => state.token,
};

const actions = {
  async register({commit}, user) {
    const userData = {
      first_name: user.get('first_name'),
      last_name: user.get('last_name'),
      surname: user.get('surname'),
      birthdate: user.get('birthdate'),
      phone: user.get('phone'),
      position: user.get('position'),
      email: user.get('email'),
      password: user.get('password'),
      personal_data_confirmed: user.get('personal_data_confirmed'),
      company: user.get('company'),
      department: user.get('department'),
    }
    const response =await axios.post('register/managers', userData);
    Cookies.set('token', response.data.result);
    commit('setToken', response.data.result)
  },
  async logIn({commit}, user) {
    const userData = {
      email: user.get('email'),
      password: user.get('password')
    }
    const response = await axios.post('login', userData);
    //const response = await fetch('http://159.223.224.135:8000/api/v1/login', {body: JSON.stringify(userData), headers: {'Content-Type': 'application/json;charset=utf-8'}, method: 'post', credentials: "include"})
    //const result = await response.json()
    Cookies.set('token', response.data.result);
    commit('setToken', response.data.result)
  },
  async logOut({commit}) {
    Cookies.remove('token')
    const token = null;
    commit('removeToken', token);
  },
  async participantsStats({commit}, dates) {
    const datesBody = {
      date_from: dates.get('date_from'),
      date_to: dates.get('date_to'),
    }
    const response = await axios.get('participants/stats', { params: datesBody, headers: { Authorization: this.getters.userToken }});
    return response
  },
  async participantsList({commit}, dates) {
    const response = await axios.get('/participants', {headers: { Authorization: this.getters.userToken }})
    return response;
  },
  async participantStats({commit}, data) {
    const datesBody = {
      date_from: data.get('date_from'),
      date_to: data.get('date_to'),
    }
    const response =await axios.get('participants/' + data.get('id') + '/stats', { params: datesBody, headers: { Authorization: this.getters.userToken }});
    return response
  },
  async sendMeRequest({commit}) {
    const response = await axios.get('participants/me', {headers: { Authorization: this.getters.userToken }});
    return response
  },
  async getStates({commit}) {
    const response = await axios.get('states', {headers: { Authorization: this.getters.userToken }});
    return response
  },
  async sendGetUserRequest({commit}, data) {
    const response = await axios.get('participants/' + data.get('user_id'), {headers: { Authorization: this.getters.userToken }});
    return response
  },
  async getGroupScore({commit}) {
    //const response =await axios.get('participants/stats/score', { headers: { Authorization: this.getters.userToken }});
    return { percent: 25, recommendation: "Что-то там" }
  },
  async getUserScore({commit}, data) {
    //const response =await axios.get('participants/' + data.get('id') + '/stats/score', { headers: { Authorization: this.getters.userToken }});
    return { percent: 25, recommendation: "Что-то там" }
  },
  async downloadFileForOne({commit}, data) {
    const datesBody = {
      date_from: data.get('date_from'),
      date_to: data.get('date_to'),
    }
    const file_name = data.get('fio') + '_' + data.get('date_from') + '_' + data.get('date_to')
    const response = await axios.get('participants/' + data.get('id') + '/stats/download-csv', { params: datesBody, responseType: 'json', headers: { Authorization: this.getters.userToken, 'Accept': 'application/json'}})
    const anchor = document.createElement('a');
    anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(response["data"]);
    anchor.target = '_blank';
    anchor.download = file_name + '.csv';
    anchor.click();
    return response
  },
  async downloadFileForGroup({commit}, data) {
    const datesBody = {
      date_from: data.get('date_from'),
      date_to: data.get('date_to'),
    }

    const file_name = data.get('company') + '_' + data.get('date_from') + '_' + data.get('date_to')

    const response =await axios.get('participants/stats/download-csv', { params: datesBody, headers: { Authorization: this.getters.userToken }});
    const anchor = document.createElement('a');
    anchor.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(response["data"]);
    anchor.target = '_blank';
    anchor.download = file_name + '.csv';
    anchor.click();
    return response
  }
};

const mutations = {
  setToken(state, token) {
    state.token = token;
  },

  
  removeToken(state, token){
    state.token = token;
  },
};

export default {
  state,
  getters,
  actions,
  mutations
};