<template>
  <div id="app">
    <b-navbar type="dark" variant="info">
      <b-navbar-brand :href="'/ipns/'+global.id+'/'">VideoShare</b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :href="'/ipns/'+user.id+'/#/'+type.name" v-for="type in user.type" :key="type.name">{{ type.title }}</b-nav-item>
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
    <b-container fluid class="main">
      <b-row>
        <b-col lg="9" >
          <video id="player" :poster="cover" controls autoplay class="video-js vjs-big-play-centered">
          </video>
          <h2 class="title">{{ title }}</h2>
          <p>{{ description }}</p>
        </b-col>
        <b-col lg="3" class="info">
          <b-card>
            <b-media>
              <b-img slot="aside" width="64" :src="user.avatar" rounded="circle"></b-img>
              <h5 >{{ user.username }}</h5>
              <p>{{ user.description }}</p>
            </b-media>
          </b-card>
          <b-card>
            <div class="ipfsqr">
              <p>IPFS地址</p>
              <div id="qrCode" ref="qrCodeDiv" class="qr"></div>
            </div>
            <div class="playerselect">
              <p>加载其他解码器  (Html5可能不支持播放本页视频)</p>
              <a :href="'potplayer://'+playfileurl">Potplayer for Windows</a><br>
              <a :href="'iina://weblink?url='+playfileurl">Iina player for Mac os</a>
            </div>
          </b-card>
          <json-viewer class="hidden-sm" :value="mediainfo" :expand-depth=2></json-viewer>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <b-list-group class="filelist">
            <b-list-group-item button v-for="file in files" :key="file.url" @click="playfile(file)">
              {{ file.title }}
              <b-badge variant="success" class="rate">{{ file.size/file.duration | formatRate}}</b-badge>
              <b-badge variant="warning" class="dura">{{ file.duration | formatDura }}</b-badge>
              <b-badge variant="info" class="size">{{ file.size | formatSize }}</b-badge>
            </b-list-group-item>
          </b-list-group>
        </b-col>
      </b-row>
    </b-container>
    <div class="footer">
      <b-container>
        <b-row>
          <b-col cols="6">
            <b-row>
              <b-col cols="4" v-for="l in global.links" :key="l.links"><a :href="l.link" >{{ l.title }}</a></b-col>
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
import videojs from 'video.js'
import QRCode from 'qrcodejs2';
export default {
  name: 'app',
  data(){
    return {
      title:"",
      description:"",
      cover: "",
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
      files:[],
      playfileurl: '',
      mediainfo:{}
    }
  },
  methods:{
    init(){
      Axios.get('./files.json').then((res)=>{
        this.files = res.data.files;
        this.title = res.data.title;
        this.description = res.data.description;
        this.cover = res.data.cover;
        this.playfile(this.files[0]);
        let myhash = window.location.pathname;
        let qrcode = '';
        if(myhash.substring(0, 6) === "/ipfs/"){
          qrcode = myhash;
        }else {
            qrcode = window.location.href;
        }
          new QRCode(this.$refs.qrCodeDiv, {
              text: qrcode,
              width: 120,
              height: 120,
              colorDark: "#333333",
              colorLight: "#ffffff",
              correctLevel: QRCode.CorrectLevel.L
          });
      });
      Axios.get('./user.json').then((res)=>{
        this.user = res.data;
        return this.user.id;
      }).then((id)=>{
        Axios.get('/ipns/'+id+'/user.json').then((res)=>{
          this.user = res.data;
        }).catch((err)=>{
          console.log(err)
        })
      });
      Axios.get('./global.json').then((res)=>{
        this.global = res.data;
        return this.global.id;
      }).then((id)=>{
        Axios.get('/ipns/'+id+'/global.json').then((res)=>{
          this.global = res.data;
        }).catch((err)=>{
          console.log(err)
        });
          new QRCode(this.$refs.qrCodeDivipns, {
              text: '/ipns/'+id,
              width: 120,
              height: 120,
              colorDark: "#333333",
              colorLight: "#ffffff",
              correctLevel: QRCode.CorrectLevel.L
          });
      });
    },
    playfile(item){
      this.mediainfo = item.mediainfo;
      this.playfileurl = window.location.origin + item.url;
      const sources = [{
        type:"video/mp4",
        src:item.url
      }];
      const player = videojs('player');
      player.ready(function(){
        const obj  = this;
        obj.src(sources);
        obj.load();
      });
    }
  },
  created() {
    this.init()
  },
  filters: {
    formatSize(size) {
      const sub = ['B','K','M','G','T'];
      for (let i = 0; i < sub.length; i++) {
        if(size<1024) return size.toFixed(2) + sub[i];
        size /= 1024;
      }
      return '';
    },
    formatDura(time) {
      let min = time / 60;
      return min.toFixed(0) + '分' + time%60 + '秒';
    },
    formatRate(bit) {
      let kbit = bit * 8 / 1024;
      let mbit = kbit / 1024;
      return mbit.toFixed(2) + 'Mbps';
    }
  },
  watch: {
    title(title) {
      document.title = this.title !=="" ? this.title + " - VideoShare":"VideoShare";
    }
  }
}
</script>

<style>
  .title{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  #player{
    width: 100%;
    height: 80vh;
  }
  .info{
    max-height: 80vh;
    overflow: auto;
  }
  .filelist button{
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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
    background: url("/ipfs/QmSiGaJ6phBKWuDmYpEocLgZgmwfGnDP9wuHww4Skxkcfq");
  }
  @media screen and (max-width:992px){
    .hidden-sm{
      display: none;
    }
    #player{
      width: 100%;
      height: calc(57vw);
    }
  }
  .ipfsqr{
    width: 120px;
    margin-right: 10px;
    float: left;
  }
  .ipfsqr p{
    margin-bottom: 4px;
    text-align: center;
  }
  .playerselect{

  }
  .playerselect p{
    margin-bottom: 4px;
    text-align: center;
  }
</style>
