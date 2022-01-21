<template>
  <el-row justify="center" type="flex">
    <el-form >

      <el-alert type="error" v-if="parse_error" @close="parse_error = !parse_error" effect="dark">
        <span>Не удалось получить информацию о состоянии игрока...</span>
      </el-alert>
      <br v-if="parse_error">
      <el-button v-if="run_game_button" style="width: 100%" @click="runGame">
        Запустить игру
      </el-button>
      <hr>
      <i v-if="wait_game" class="el-icon-loading"/>
      <span v-if="wait_game" style="width: 100%; text-align: center; align-items: center">
        Игра не началась...
      </span>
      <br v-if="wait_game">

      <i class="el-icon-link"/>
      <span class="font-bold">Код для подключения: <span @click="copyText(game_id)">{{ game_id }}</span>, ссылка для подключения: <span @click="copyText('localhost:3000/invite?id=' + game_id)">localhost:3000/invite?id={{game_id}}</span></span>

      <br>
      <hr>
      <i class="el-icon-view"/>
      <span>Тип игры: {{gameType}}</span>
      <br>
      <i class="el-icon-user-solid"/>
      <span>Игроков: {{players.length}}</span>
      <br>
      <i class="el-icon-user"/>
      <span>Пользователи</span>
      <br>
      <template v-for="item in players">
        <i class="el-icon-caret-right"/>
        <span> {{item}}</span>
        <br>
      </template>

      <hr>


    </el-form>
  </el-row>
</template>

<script>
export default {
  name: "game",
  data (){
    const game_id = this.$route.query.id
    const token = this.$route.query.token
    const wait_game = false;
    const run_game_button = false
    const players = [];
    const gameType = "";
    const parse_error = false;
    const me = {
      balance : 0,
      workshops: 0,
      flighters : 0,
      material: 0
    }

    setTimeout(this.updateData, 4000)
    return {game_id, wait_game, run_game_button, players, token, gameType, parse_error}
  },
  async asyncData({$axios, route}){
    const url = "http://localhost:12001/check_run";
    const data = await $axios.$post(url, {
      "token" : route.query.token,
      "game_id" : route.query.id
    })
    const wait_game = data["wait"];
    const run_game_button = data["run_button"];
    const players = await $axios.$post("http://localhost:12001/players", {"game_id" : route.query.id})
    const gameType = await $axios.$post("http://localhost:12001/game_type", {"game_id" : route.query.id})
    return {wait_game, run_game_button, players, gameType}
  }
  ,
  methods: {
    copyText(text){
      navigator.clipboard.writeText(text);
    },
    async runGame(){
      await this.$axios.$post("http://localhost:12001/run_game", {
        "token" : this.token,
        "game_id" : this.game_id,
      })
      this.run_game_button = false;
      this.wait_game = false;
    },
    async updateData(){
      const url = "http://localhost:12001/check_run";
      const data = await this.$axios.$post(url, {
        "token" : this.$route.query.token,
        "game_id" : this.$route.query.id
      })
      console.log(data)
      this.wait_game = data["wait"];
      this.players = await this.$axios.$post("http://localhost:12001/players", {"game_id" : this.$route.query.id})

      try{
        const me = await this.$axios.$post("http://localhost:12001/me", {"token" : this.$route.query.token,"game_id" : this.$route.query.id})
        if (me["success"] == false){
          this.parse_error = true
        }
        else {
          this.me.balance = me["balance"]
          this.me.workshops = me["workshops"]
          this.me.flighters = me["flighters"]
          this.me.material = me["material"]
        }
      }
      catch{
        this.parse_error = true;
      }
      setTimeout(this.updateData, 4000)
    }
  }
}
</script>


<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@600&display=swap');

* {
  font-family: 'Comfortaa', cursive;
  font-size: 110%;

}



</style>

