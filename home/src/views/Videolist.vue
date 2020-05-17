<template>
  <div id="home">
    <b-container>
      <b-row>
        <h2>{{ title }}</h2>
      </b-row>
      <b-row>
        <b-col sm="6" md="4" lg="3" xl="2" v-for="video in videolist">
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
    name: 'home',
    data(){
      return {
        title: '',
        type: '',
        videolist: []
      }
    },
    methods:{
      async init(){
        this.type = this.$route.path.substr(1);
        await Axios.get('./type.json').then(async (res)=>{
          for (let i=0;i<res.data.type.length;i++){
            if(res.data.type[i].name===this.type){
              this.title = res.data.type[i].title
            }
          }
        });
        await Axios.get('./type_'+this.type+'.json').then(async (res)=>{
          this.videolist = [];
          for (let i  = 0; i<res.data.list.length;i++) {
            let temp = await Axios.get('/ipns/'+res.data.list[i].id+'/'+res.data.list[i].usertype+'.json').then((res)=>{
              return res.data;
            });
            for (let j=0;j<temp.length;j++){
              this.videolist.push(temp[j])
            }
          }
        });
      },
    },
    created() {
      this.init()
    },
    watch:{
      $route(to,from){
        this.init();
      },
      title(title) {
        document.title = this.title !=="" ? this.title + " - VideoShare":"VideoShare";
      }
    }
  }
</script>
<style>
  .row >.col-sm-6, .row >.col-md-4, .row >.col-lg-3, .row >.col-xl-2 {
    padding-left: 1px;
    padding-right: 1px;
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
