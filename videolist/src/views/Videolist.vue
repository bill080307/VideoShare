<template>
  <div class="videolist">
    <b-container fluid>
      <b-row>
        <b-col sm="12" md="6" lg="4" xl="3" v-for="(video,index) in videolist" :key="index">
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
        this.videolist = res.data.videolist;
      });
    },
    async getalllist(){
      let tempvideolist=[];
      let type = await Axios.get('./user.json');
      for (let i = 0; i < type.data.type.length; i++) {
        const vlist = await Axios.get('./'+type.data.type[i].name+'.json');
        tempvideolist = tempvideolist.concat(vlist.data);
      }
      this.videolist = tempvideolist;
      console.log(this.videolist)
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

</style>
