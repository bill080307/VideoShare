<template>
  <div id="app">
    <div class="header">
      <b-navbar type="dark">
        <b-container>
          <b-navbar-nav>
            <b-nav-item to="/">主站</b-nav-item>
            <b-nav-item href="#">主站A</b-nav-item>
            <b-nav-item href="#">主站S</b-nav-item>
            <b-nav-item href="#">短视频</b-nav-item>
            <b-nav-item href="#">直播</b-nav-item>
          </b-navbar-nav>
        </b-container>
      </b-navbar>
      <b-container>
        <a to="/" class="h_logo">Video Share</a>
      </b-container>
    </div>
    <div class="nava">
      <b-navbar type="light" variant="light" toggleable="lg">
        <b-container>
          <b-navbar-nav>
            <b-nav-item to="/">首页</b-nav-item>
            <b-nav-item :to="navitem.name" v-for="navitem in typelist" >
              {{ navitem.title }}
            </b-nav-item>
          </b-navbar-nav>
        </b-container>
      </b-navbar>
    </div>
    <router-view/>
    <div class="footer">
      <b-container>
        <b-row>
          <b-col cols="4">
            <b-row>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
            </b-row>

          </b-col>
          <b-col cols="4">
            <b-row>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
              <b-col cols="5"><a href="#">Video Share</a></b-col>
            </b-row>
          </b-col>
          <b-col cols="4">
            <a class="f_logo" href="#"></a>
          </b-col>
        </b-row>
      </b-container>
    </div>
  </div>
</template>
<script>
  import Axios from 'axios'
  export default {
    name: 'app',
    data(){
      return {
        typelist:[],
      }
    },
    methods:{
      async init(){
        await Axios.get('./type.json').then(async (res)=>{
          this.typelist = res.data.type;
        });
      },
    },
    created() {
      this.init()
    },
  }
</script>
<style>
  .header{
    height: 200px;
    background: url("assets/header.jpg") center repeat-x;
  }
  .header .navbar{
    background-color: rgba(0, 0, 0, 0.6) ;
  }
  .h_logo{
    position: relative;
    top: 22px;
    left: 50px;
    display: block;
    width: 300px;
    height: 100px;
    background: url("assets/logo.png") no-repeat;
    text-indent: -999px;
  }
  .footer{
    margin-top: 40px;
    padding-top: 40px;
    padding-bottom: 40px;
    background-color: #f6f9fa;
  }
  .f_logo{
    display: inline-block;
    width: 300px;
    height: 100px;
    background: url("assets/logo.png");
  }
</style>
