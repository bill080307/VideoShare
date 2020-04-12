<template>
  <div id="app">
    <b-navbar type="dark" variant="info">
      <b-navbar-brand to="/">VideoShare</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="type.name" v-for="type in user.type" :key="type.name">{{ type.title }}</b-nav-item>
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
            <b-dropdown-item :href="link.link" v-for="link in global.extend" :key="link.link">{{ link.title }}</b-dropdown-item>
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
        <b-col cols="7">
          <h1>{{ user.username }}</h1>
          <p> {{ user.description }}</p>
        </b-col>
        <b-col cols="2">
          <div id="qrCode" ref="qrCodeDiv" class="qr"></div>
        </b-col>
      </b-row>
    </b-container>
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
              <div id="qrCodeipns" ref="qrCodeDivipns" class="qr"></div>
            </b-row>
          </b-col>
          <b-col cols="4">
            <a class="f_logo" :href="'/ipns/'+global.id+'/'"></a>
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
        extend:[],
        links:[],
      },
    }
  },
  methods:{
    init(){
      Axios.get('./user.json').then((res)=>{
        new QRCode(this.$refs.qrCodeDiv, {
          text: '/ipns/'+res.data.id+'/',
          width: 120,
          height: 120,
          colorDark: "#333333",
          colorLight: "#ffffff",
          correctLevel: QRCode.CorrectLevel.L
        });
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
          new QRCode(this.$refs.qrCodeDivipns, {
              text: '/ipns/'+id,
              width: 120,
              height: 120,
              colorDark: "#333333",
              colorLight: "#ffffff",
              correctLevel: QRCode.CorrectLevel.L
          });
      });
    }
  },
  created(){
    this.init();
  }
}
</script>
<style>
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
    background: url("/ipfs/QmSiGaJ6phBKWuDmYpEocLgZgmwfGnDP9wuHww4Skxkcfq");
  }
</style>
