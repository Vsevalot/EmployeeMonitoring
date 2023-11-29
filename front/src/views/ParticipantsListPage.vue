<template>
    <div v-if="isLoggedIn">
      <div style="text-align:center">
        <button class="btn btn-primary hover:bg-gray-800 mb-5 ms-4 me-4" @click="groupClick()">
              Посмотреть статистику по группам
        </button>
      </div>
      <div id="search">
        <svg viewBox="0 0 420 60" xmlns="http://www.w3.org/2000/svg">
          <rect class="bar"/>
          
          <g class="magnifier">
            <circle class="glass"/>
            <line class="handle" x1="32" y1="32" x2="44" y2="44"></line>
          </g>

          <g class="sparks">
            <circle class="spark"/>
            <circle class="spark"/>
            <circle class="spark"/>
          </g>

          <g class="burst pattern-one">
            <circle class="particle circle"/>
            <path class="particle triangle"/>
            <circle class="particle circle"/>
            <path class="particle plus"/>
            <rect class="particle rect"/>
            <path class="particle triangle"/>
          </g>
          <g class="burst pattern-two">
            <path class="particle plus"/>
            <circle class="particle circle"/>
            <path class="particle triangle"/>
            <rect class="particle rect"/>
            <circle class="particle circle"/>
            <path class="particle plus"/>
          </g>
          <g class="burst pattern-three">
            <circle class="particle circle"/>
            <rect class="particle rect"/>
            <path class="particle plus"/>
            <path class="particle triangle"/>
            <rect class="particle rect"/>
            <path class="particle plus"/>
          </g>
        </svg>
        <input type=search name=q aria-label="Search for inspiration" placeholder="Фильтр по участникам"  ref="users_filter" v-model="users_filter"/>
      </div>

      <div style="text-align:center">
        <f7-list>
          <tr v-for="user in users">
            <div class="costomcontainer">
              <div class="card">
                <h2>{{user.first_name}}</h2>
                <h2>{{user.last_name}}</h2>
                <div class="title title--common" @click="userClick(user.id)">Посмотреть</div>
                
                <svg viewBox="0 0 100 100">
                  <path d="m38.977 59.074c0 2.75-4.125 2.75-4.125 0s4.125-2.75 4.125 0"></path>
                  <path d="m60.477 59.074c0 2.75-4.125 2.75-4.125 0s4.125-2.75 4.125 0"></path>
                  <path d="m48.203 69.309c1.7344 0 3.1484-1.4141 3.1484-3.1484 0-0.27734-0.22266-0.5-0.5-0.5-0.27734 0-0.5 0.22266-0.5 0.5 0 1.1836-0.96484 2.1484-2.1484 2.1484s-2.1484-0.96484-2.1484-2.1484c0-0.27734-0.22266-0.5-0.5-0.5-0.27734 0-0.5 0.22266-0.5 0.5 0 1.7344 1.4141 3.1484 3.1484 3.1484z"></path>
                  <path d="m35.492 24.371c0.42187-0.35156 0.48047-0.98438 0.125-1.4062-0.35156-0.42188-0.98438-0.48438-1.4062-0.125-5.1602 4.3047-16.422 17.078-9.5312 42.562 0.21484 0.79688 0.85547 1.4062 1.6641 1.582 0.15625 0.035156 0.31641 0.050781 0.47266 0.050781 0.62891 0 1.2344-0.27344 1.6445-0.76562 0.82812-0.98828 2.0039-1.5391 2.793-1.8203 0.56641 1.6055 1.4766 3.3594 2.9727 4.9414 2.2852 2.4219 5.4336 3.9453 9.3867 4.5547-3.6055 4.5-3.8047 10.219-3.8086 10.484-0.011719 0.55078 0.42187 1.0078 0.97656 1.0234h0.023438c0.53906 0 0.98437-0.42969 1-0.97266 0-0.054688 0.17187-4.8711 2.9805-8.7773 0.63281 1.2852 1.7266 2.5 3.4141 2.5 1.7109 0 2.7578-1.2695 3.3398-2.6172 2.8867 3.9258 3.0586 8.8359 3.0586 8.8906 0.015625 0.54297 0.46094 0.97266 1 0.97266h0.023438c0.55078-0.015625 0.98828-0.47266 0.97656-1.0234-0.007812-0.26953-0.20703-6.0938-3.9141-10.613 7.0781-1.3086 10.406-5.4219 11.969-8.9766 1.0508 0.98828 2.75 2.1992 4.793 2.1992 0.078126 0 0.15625 0 0.23828-0.003906 0.47266-0.023438 1.5781-0.074219 3.4219-4.4219 1.1172-2.6406 2.1406-6.0117 2.8711-9.4922 4.8281-22.945-4.7852-30.457-9.1445-32.621-12.316-6.1172-22.195-3.6055-28.312-0.42188-0.48828 0.25391-0.67969 0.85938-0.42578 1.3477s0.85938 0.67969 1.3477 0.42578c5.7031-2.9688 14.934-5.3047 26.5 0.4375 7.1875 3.5703 9 11.586 9.2539 17.684 0.49609 11.93-4.2617 23.91-5.7344 25.062h-0.015626c-1.832 0-3.4102-1.5742-4.0352-2.2852 0.28906-0.99609 0.44531-1.8672 0.52734-2.5117 0.62891 0.16797 1.2812 0.27344 1.9727 0.27344 0.55469 0 1-0.44922 1-1 0-0.55078-0.44531-1-1-1-7.3203 0-10.703-13.941-10.734-14.082-0.097656-0.40625-0.4375-0.71094-0.85156-0.76172-0.43359-0.050781-0.82031 0.16406-1.0117 0.53906-1.8984 3.7188-1.4297 6.7539-0.67969 8.668-6.2383-2.2852-8.9766-8.6914-9.0078-8.7617-0.17969-0.43359-0.62891-0.68359-1.1016-0.60156-0.46094 0.082032-0.80469 0.47266-0.82422 0.94141-0.14062 3.3359 0.67188 5.75 1.5 7.3164-8.3125-2.4297-10.105-11.457-10.184-11.875-0.097656-0.51562-0.57422-0.86328-1.0898-0.8125-0.51953 0.054687-0.90625 0.50391-0.89062 1.0234 0.41406 13.465-1.8516 17.766-3.2383 19.133-0.66406 0.65625-1.1992 0.67188-1.2383 0.67188-0.53906-0.050781-1.0156 0.31641-1.0938 0.85156-0.078125 0.54688 0.29688 1.0547 0.84375 1.1328 0.03125 0.003906 0.11328 0.015625 0.23828 0.015625 0.36719 0 1.1016-0.09375 1.9414-0.66406 0.050781 0.38672 0.125 0.81641 0.21875 1.2656-1.0273 0.35156-2.6211 1.0781-3.7812 2.4648-0.015625 0.019532-0.054687 0.066406-0.15625 0.046875-0.039062-0.007812-0.13281-0.039062-0.16406-0.15234-2.1875-8.1094-5.7148-28.309 8.8867-40.496zm12.711 51.828c-1.0039 0-1.5898-1.207-1.8672-2.0117 0.48047 0.023438 0.95703 0.050781 1.4531 0.050781 0.74219 0 1.4453-0.035156 2.1289-0.082031-0.24219 0.83594-0.76172 2.043-1.7148 2.043zm-13.148-30.664c1.9531 3.6211 5.6367 7.9102 12.305 8.6992 0.43359 0.046875 0.83984-0.18359 1.0234-0.57422 0.18359-0.39062 0.089844-0.85938-0.22656-1.1523-0.074219-0.070312-1.2734-1.2227-1.9688-3.6367 2 2.6094 5.3359 5.6836 10.305 6.5664 0.42187 0.070312 0.83594-0.125 1.0469-0.49219 0.21094-0.36719 0.16406-0.82812-0.11719-1.1484-0.023437-0.027344-1.9414-2.2969-1.2891-5.8906 1.2227 3.5508 3.7461 9.2227 7.8945 11.551-0.03125 0.55859-0.14844 1.668-0.55078 3.0156-0.085937 0.13672-0.125 0.28516-0.13672 0.44531-1.3008 3.8906-5.0039 9.3281-15.547 9.3281-5.375 0-9.4414-1.418-12.086-4.2109-3.5664-3.7656-3.332-8.8477-3.332-8.8984v-0.011719c1.5898-2.7227 2.5-7.3203 2.6797-13.59z"></path>
                </svg>
              </div>
            </div>
          </tr>
        </f7-list>
      </div>
    </div>
    <p v-else>
      <span><a href="/register">Register</a></span>
      <span> or </span>
      <span><a href="/login">Log In</a></span>
    </p>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapActions } from 'vuex';
  
  export default {
    name: 'Ping',
    data() {
      return {
        users: [],
        saved_users: [],
        users_filter: "",
      };
    },
    watch: {
      users_filter(current, prev) {
        if (current.length > 0) {
          console.log(this.users)
          const result = this.saved_users.filter((user) => (user.first_name + " " + user.last_name).includes(current));
          this.users = result;
        } else {
          this.users = this.saved_users
        }
      },
    },
    methods: {
      ...mapActions(['participantsList']),
      async getMessage() {
        console.log(this.isLoggedIn)
        if (this.isLoggedIn) {
          debugger
          const response = await this.participantsList()
          
          this.users = response.data.result;
          this.saved_users = response.data.result;
        }
      },
      async userClick(user_id) {
        debugger
        this.$router.push({name: 'current_participants', params: {id: user_id}});
      },
      async groupClick() {
        this.$router.push('/participants/stats');
      }
    },
    computed : {
    isLoggedIn: function() {
      return this.$store.getters.isAuthenticated;
    }
  },
    created() {
      this.getMessage();
    },
  };
  </script>

  <style lang="scss">

@import url("https://fonts.googleapis.com/css?family=Roboto:400,400i,700");

*,
*::before,
*::after {
  margin: 0;
  padding: 0;
  box-sizing: inherit;
}

.contbody {
  height: 100vh;
  
  box-sizing: border-box;
  font-family: 'Roboto', 'Sans-serif';
  background-color: whitesmoke;
  
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.costomcontainer {
  display: flex;
  
}

.card {
  margin: 1rem;
  width: 300px;
  height: 500px;
  padding: .5rem 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 12px 32px 4px rgba(black, .2);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  transition: .2s;
  
  &:hover {
    transform: translateY(-5px);
  }

  .title {
    color: white;
    margin: 1rem;
    padding: .5rem 1rem;
    border-radius: 50px;
    transition: .2s;
    cursor: pointer;
    
    &--legendary {
      background-color: #f4d03f;
      &:hover {
        box-shadow: 0 0 12px rgba(#f4d03f, .8);
      }
    }
    
        &--epic {
      background-color: #8c14fc;
      &:hover {
        box-shadow: 0 0 12px rgba(#8c14fc, .8);
      }
    }
    
        &--common {
      background-color: #2ecc71;
      &:hover {
        box-shadow: 0 0 12px rgba(#2ecc71, .8);
      }
    }
    
  }
  
  .desc {
    text-align: center;
  }
  
  .actions {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    
    button {
      padding: .5rem .8rem;
      cursor: pointer;
      background-color: transparent;
      border: none;
      text-transform: uppercase;
      outline: 0;
      transition: background-color .4s, color .4s, transform .1s;
      
      &:hover {
        color: white;
        box-shadow: 0 0 24px rgba(black, .2);
      }
      
      &:active {
        transform: scale(0.95);
        box-shadow: 0 0 16px rgba(black, .3);
      }
    }
    
    &__like {
      &:hover {
        background-color: #00b16a;
      }
    }
    
        &__trade {
      &:hover {
        background-color: #3498db;
      }
    }
    
        &__cancel {
      &:hover {
        background-color: #c0392b;
      }
    }
  }
}

p {
  margin-top: 1rem;
  color: #484848;
}

a:link,
a:visited {
  text-decoration: none;
  color: #2574a9;
}

.active {
  background-color: #00b16a;
}



button::-moz-focus-inner {
  border: 0;
}




#search {
	display: grid;
	grid-area: search;
	grid-template:
		"search" 60px
		/ 420px;
	justify-content: center;
	align-content: center;
	justify-items: stretch;
	align-items: stretch;
	background: hsl(0, 0%, 99%);
}

#search input {
	display: block;
	grid-area: search;
	-webkit-appearance: none;
	appearance: none;
	width: 100%;
	height: 100%;
	background: none;
	padding: 0 30px 0 60px;
	border: none;
	border-radius: 100px;
	font: 24px/1 system-ui, sans-serif;
	outline-offset: -8px;
}


#search svg {
	grid-area: search;
	overflow: visible;
	color: hsl(215, 100%, 50%);
	fill: none;
	stroke: currentColor;
}

.spark {
	fill: currentColor;
	stroke: none;
	r: 15;
}

.spark:nth-child(1) {
	animation:
		spark-radius 2.03s 1s both,
		spark-one-motion 2s 1s both;
}

@keyframes spark-radius {
	0% { r: 0; animation-timing-function: cubic-bezier(0, 0.3, 0, 1.57) }
	30% { r: 15; animation-timing-function: cubic-bezier(1, -0.39, 0.68, 1.04) }
	95% { r: 8 }
	99% { r: 10 }
	99.99% { r: 7 }
	100% { r: 0 }
}

@keyframes spark-one-motion {
	0% { transform: translate(-20%, 50%); animation-timing-function: cubic-bezier(0.63, 0.88, 0, 1.25) }
	20% { transform: rotate(-0deg) translate(0%, -50%); animation-timing-function: ease-in }
	80% { transform: rotate(-230deg) translateX(-20%) rotate(-100deg) translateX(15%); animation-timing-function: linear }
	100% { transform: rotate(-360deg) translate(30px, 100%); animation-timing-function: cubic-bezier(.64,.66,0,.51) }
}

.spark:nth-child(2) {
	animation:
		spark-radius 2.03s 1s both,
		spark-two-motion 2.03s 1s both;
}

@keyframes spark-two-motion {
	0% { transform: translate(120%, 50%) rotate(-70deg) translateY(0%); animation-timing-function: cubic-bezier(0.36, 0.18, 0.94, 0.55) }
	20% { transform: translate(90%, -80%) rotate(60deg) translateY(-80%); animation-timing-function: cubic-bezier(0.16, 0.77, 1, 0.4) }
	40% { transform: translate(110%, -50%) rotate(-30deg) translateY(-120%); animation-timing-function: linear }
	70% { transform: translate(100%, -50%) rotate(120deg) translateY(-100%); animation-timing-function: linear }
	80% { transform: translate(95%, 50%) rotate(80deg) translateY(-150%); animation-timing-function: cubic-bezier(.64,.66,0,.51) }
	100% { transform: translate(100%, 50%) rotate(120deg) translateY(0%) }
}

.spark:nth-child(3) {
	animation:
		spark-radius 2.05s 1s both,
		spark-three-motion 2.03s 1s both;
}

@keyframes spark-three-motion {
	0% { transform: translate(50%, 100%) rotate(-40deg) translateX(0%); animation-timing-function: cubic-bezier(0.62, 0.56, 1, 0.54) }
	30% { transform: translate(40%, 70%) rotate(20deg) translateX(20%); animation-timing-function: cubic-bezier(0, 0.21, 0.88, 0.46) }
	40% { transform: translate(65%, 20%) rotate(-50deg) translateX(15%); animation-timing-function: cubic-bezier(0, 0.24, 1, 0.62) }
	60% { transform: translate(60%, -40%) rotate(-50deg) translateX(20%); animation-timing-function: cubic-bezier(0, 0.24, 1, 0.62) }
	70% { transform: translate(70%, -0%) rotate(-180deg) translateX(20%); animation-timing-function: cubic-bezier(0.15, 0.48, 0.76, 0.26) }
	100% { transform: translate(70%, -0%) rotate(-360deg) translateX(0%) rotate(180deg) translateX(20%); }
}




.burst {
	stroke-width: 3;
}

.burst :nth-child(2n) { color: #ff783e }
.burst :nth-child(3n) { color: #ffab00 }
.burst :nth-child(4n) { color: #55e214 }
.burst :nth-child(5n) { color: #82d9f5 }

.circle {
	r: 6;
}

.rect {
	width: 10px;
	height: 10px;
}

.triangle {
	d: path("M0,-6 L7,6 L-7,6 Z");
	stroke-linejoin: round;
}

.plus {
	d: path("M0,-5 L0,5 M-5,0L 5,0");
	stroke-linecap: round;
}




.burst:nth-child(4) {
	transform: translate(30px, 100%) rotate(150deg);
}

.burst:nth-child(5) {
	transform: translate(50%, 0%) rotate(-20deg);
}

.burst:nth-child(6) {
	transform: translate(100%, 50%) rotate(75deg);
}

.burst * {}

@keyframes particle-fade {
	0%, 100% { opacity: 0 }
	5%, 80% { opacity: 1 }
}

.burst :nth-child(1) { animation: particle-fade 600ms 2.95s both, particle-one-move 600ms 2.95s both; }
.burst :nth-child(2) { animation: particle-fade 600ms 2.95s both, particle-two-move 600ms 2.95s both; }
.burst :nth-child(3) { animation: particle-fade 600ms 2.95s both, particle-three-move 600ms 2.95s both; }
.burst :nth-child(4) { animation: particle-fade 600ms 2.95s both, particle-four-move 600ms 2.95s both; }
.burst :nth-child(5) { animation: particle-fade 600ms 2.95s both, particle-five-move 600ms 2.95s both; }
.burst :nth-child(6) { animation: particle-fade 600ms 2.95s both, particle-six-move 600ms 2.95s both; }

@keyframes particle-one-move { 0% { transform: rotate(0deg) translate(-5%) scale(0.0001, 0.0001) } 100% { transform: rotate(-20deg) translateX(8%) scale(0.5, 0.5) } }
@keyframes particle-two-move { 0% { transform: rotate(0deg) translate(-5%) scale(0.0001, 0.0001) } 100% { transform: rotate(0deg) translateX(8%) scale(0.5, 0.5) } }
@keyframes particle-three-move { 0% { transform: rotate(0deg) translate(-5%) scale(0.0001, 0.0001) } 100% { transform: rotate(20deg) translateX(8%) scale(0.5, 0.5) } }
@keyframes particle-four-move { 0% { transform: rotate(0deg) translate(-5%) scale(0.0001, 0.0001) } 100% { transform: rotate(-35deg) translateX(12%) } }
@keyframes particle-five-move { 0% { transform: rotate(0deg) translate(-5%) scale(0.0001, 0.0001) } 100% { transform: rotate(0deg) translateX(12%) } }
@keyframes particle-six-move { 0% { transform: rotate(0deg) translate(-5%) scale(0.0001, 0.0001) } 100% { transform: rotate(35deg) translateX(12%) } }



.bar {
	width: 100%;
	height: 100%;
	ry: 50%;
	stroke-width: 5;
	animation: bar-in 900ms 3s both;
}

@keyframes bar-in {
	0% { stroke-dasharray: 0 180 0 226 0 405 0 0 }
	100% { stroke-dasharray: 0 0 181 0 227 0 405 0 }
}

.magnifier {
	animation: magnifier-in 600ms 3.6s both;
	transform-box: fill-box;
}

@keyframes magnifier-in {
	0% { transform: translate(20px, 8px) rotate(-45deg) scale(0.01, 0.01); }
	50% { transform: translate(-4px, 8px) rotate(-45deg); }
	100% { transform: translate(0px, 0px) rotate(0deg); }
}

.magnifier .glass {
	cx: 27;
	cy: 27;
	r: 8;
	stroke-width: 3;
}
.magnifier .handle {
	x1: 32;
	y1: 32;
	x2: 44;
	y2: 44;
	stroke-width: 3;
}



#results {
	grid-area: results;
	background: hsl(0, 0%, 95%);
}
  </style>