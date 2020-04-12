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
          <b-navbar-nav class="ml-auto">
            <b-nav-item-dropdown right>
              <template slot="button-content">更多</template>
              <b-dropdown-item :href="global.news">公告</b-dropdown-item>
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item :href="global.dashboard">管理我的空间</b-dropdown-item>
              <b-dropdown-divider></b-dropdown-divider>
              <b-dropdown-item :href="link.link" v-for="link in global.extend">{{ link.title }}</b-dropdown-item>
              <b-dropdown-item :href="global.client.download">下载客户端</b-dropdown-item>
            </b-nav-item-dropdown>
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
          <b-col cols="6">
            <b-row>
              <b-col cols="4" v-for="l in global.links" :key="l.link"><a :href="l.link" >{{ l.title }}</a></b-col>
            </b-row>
          </b-col>
          <b-col cols="2">
            <b-row>
              <div id="qrCode" ref="qrCodeDiv" class="qr"></div>
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
  import QRCode from 'qrcodejs2';
  export default {
    name: 'app',
    data(){
      return {
        typelist:[],
        global:{
          id: "",
          dashboard: "",
          client: {
            download: ""
          },
          extend:[],
            links:[],
        },
      }
    },
    methods:{
      async init(){
        Axios.get('./type.json').then(async (res)=>{
          this.typelist = res.data.type;
        });
        Axios.get('./global.json').then((res)=>{
          this.global = res.data;
          new QRCode(this.$refs.qrCodeDiv, {
            text: '/ipns/'+res.data.id+'/',
            width: 120,
            height: 120,
            colorDark: "#333333",
            colorLight: "#ffffff",
            correctLevel: QRCode.CorrectLevel.L
          });
        }).catch((err)=>{
          console.log(err)
        })
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
