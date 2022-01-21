<template>

  <el-row justify="center" type="flex">

    <el-form>

      <el-input placeholder="Введи свой ник" v-model="nick" style="height: 40px;border-radius: 10px"/>

      <br>
      <br>
      <el-dropdown style="text-align: center; width: 100%; border: 1px solid black; height: 35px; border-radius: 5px" @command="changeGameType">
        <span class="el-dropdown-link">Тип игры</span>

        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="0">12 месяцев</el-dropdown-item>
          <el-dropdown-item command="1">Единственный победитель</el-dropdown-item>
        </el-dropdown-menu>

      </el-dropdown>

      <br>
      <br>



      <el-button style="width: 100%" @click="createGame">
        Создать игру
      </el-button>
    </el-form>
  </el-row>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'IndexPage',
  data() {
    const nick = "";
    const gameType = 0;
    return {
      nick, gameType
    }
  },
  methods: {
    changeGameType(Type: number){
      this.gameType = Type;
      console.log(this.gameType)
    },
    async createGame(){
      const url = "http://localhost:12001/create_game";
      const data = await this.$axios.$post(url, {
        "nick" : this.nick,
        "game_type" : this.gameType
      });
      await this.$router.push("/game?id=" + data["game_id"] + "&token=" + data["secret_token"])
    }
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Comfortaa:wght@600&display=swap');

* {
  font-family: 'Comfortaa', cursive;
  font-size: 110%;

}


</style>

