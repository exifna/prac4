<template>
  <el-row justify="center" type="flex">
    <el-form >

      <el-alert type="error" v-if="show_error" style="width: 100%">Не удалось подключится к игре...</el-alert>

      <br v-if="show_error">

      <el-input v-model="game_id" placeholder="ID игры"/>

      <br>
      <br>
      <el-input v-model="nick" placeholder="Имя"/>
      <br>
      <br>

      <el-button style="width: 100%" @click="inviteGame">
        Присоедениться
      </el-button>

      <br>


    </el-form>
  </el-row>


</template>

<script>
export default {
  name: "invite",

  data() {
    const game_id = this.$route.query.id;
    const nick = "";
    const show_error = false;

    return {
      game_id, nick, show_error
    }
  },
  methods : {
    async inviteGame(){
      const data = await this.$axios.$post("http://localhost:12001/accept_invite", {
        "game_id" : this.game_id,
        "nick" : this.nick
      })
      if (!data["success"]){
        this.show_error = true;
        return
      }
      await this.$router.push("/game?id=" + this.game_id + "&token=" + data["secret_token"])

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
