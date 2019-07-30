<template>
  <div id="app">
    <b-navbar type="dark" variant="info">
      <b-navbar-brand to="/">VideoShare</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="type.name" v-for="type in user.type">{{ type.title }}</b-nav-item>
        </b-navbar-nav>
        <b-navbar-nav class="ml-auto">
          <b-nav-item-dropdown right>
            <template slot="button-content">更多</template>
            <b-dropdown-item :href="'/ipns/'+user.id">前往 {{ user.username }} 用户空间</b-dropdown-item>
            <b-dropdown-item :href="'/ipns/'+global.id">前往聚合空间</b-dropdown-item>
            <b-dropdown-item :href="global.news">公告</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item :href="global.dashboard">管理我的空间</b-dropdown-item>
            <b-dropdown-divider></b-dropdown-divider>
            <b-dropdown-item :href="link.link" v-for="link in global.extend">{{ link.title }}</b-dropdown-item>
            <b-dropdown-item :href="global.client.download">下载客户端</b-dropdown-item>
          </b-nav-item-dropdown>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
    <b-container>
      <b-row>
        <b-col cols="3">
          <b-img fluid :src="user.avatar"></b-img>
        </b-col>
        <b-col cols="9">
          <h1>{{ user.username }}</h1>
          <p> {{ user.description }}</p>
        </b-col>
      </b-row>
    </b-container>
    <router-view/>
  </div>
</template>

<script>
import Axios from 'axios'
export default {
  name: 'app',
  data(){
    return {
      title:"",
      description:"",
      user:{
        avatar:"",
        username:"",
        description:""
      },
      global:{
        id: "",
        dashboard: "",
        client: {
          download: ""
        },
        extend:[]
      },
    }
  },
  methods:{
    init(){
      Axios.get('./user.json').then((res)=>{
        this.user = res.data;
        return this.user.id;
      });
      Axios.get('./global.json').then((res)=>{
        this.global = res.data;
        return this.global.id;
      }).then((id)=>{
        Axios.get('/ipns/'+id+'/global.json').then((res)=>{
          this.global = res.data;
        }).catch((err)=>{
          console.log(err)
        })
      });
    }
  },
  created(){
    this.init();
  }
}
</script>
<style>
</style>
