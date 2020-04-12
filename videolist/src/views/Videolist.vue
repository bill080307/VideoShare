<template>
  <div class="videolist">
    <b-container>
      <b-row>
        <b-col sm="6" md="4" lg="3" xl="2" v-for="(video,index) in videolist" :key="index" class="video">
          <b-card :img-src="video.cover">
            <b-card-text>
              <a :href="video.url"><h4>{{ video.title }}</h4></a>
            </b-card-text>
          </b-card>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import Axios from 'axios'
export default {
  name: 'videolist',
  data(){
    return {
      videolist:[],
    }
  },
  methods:{
    init(){
      let type = this.$route.path.substr(1);
      if(type.length>0){
        this.getlist(type);
      }else{
        this.getalllist();
      }
    },
    getlist(type){
      Axios.get('./'+type+'.json').then((res)=>{
        this.videolist = res.data;
      });
    },
    async getalllist(){
      let tempvideolist=[];
      let type = await Axios.get('./user.json');
      for (let i = 0; i < type.data.type.length; i++) {
        const vlist = await Axios.get('./'+type.data.type[i].name+'.json');
          for (let j = 0; j < vlist.data.length; j++) {
              let flag = true;
              for (let k = 0; k < tempvideolist.length; k++) {
                  if(tempvideolist[k]['url'] === vlist.data[j]['url']){
                      flag = false;
                      break;
                  }
              }
              if(flag){
                  tempvideolist.push(vlist.data[j])
              }
          }
      }
      this.videolist = tempvideolist;
    }
  },
  created(){
    this.init();
  },
  watch:{
    $route(to,from){
      this.init();
    }
  }
}
</script>
<style>
  .video{
    padding-left:5px;
    padding-right:5px;
    padding-bottom: 15px;
  }
  .card > .card-body{
    padding: 0.4rem;
  }
  a > h4{
    font-size: 0.8rem;
    overflow: hidden;
    text-overflow:ellipsis;
    white-space: nowrap;
  }
</style>
