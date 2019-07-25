<template>
  <div id="app">
    <b-container fluid>
      <b-row>
        <b-col cols="2">
          <b-form-group
                  :label="'选择服务器地址['+server_url.length+']'"
                  label-for="S-url"
          >
            <b-input-group>
              <b-form-select v-model="ipfsapi" :options="server_url" @change="changeserverlist"></b-form-select>
              <b-input-group-append>
                <b-button variant="outline-primary" v-b-modal.edit-server>编辑</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
          <b-form-group
                  :label="'选择账号['+key_list.length+']'"
                  label-for="key-list"
          >
            <b-input-group>
              <b-form-select v-model="ipfskey" :options="key_list" @change="changeuserlist"></b-form-select>
              <b-input-group-append>
                <b-button variant="outline-primary" v-b-modal.edit-keys>编辑</b-button>
              </b-input-group-append>
            </b-input-group>
          </b-form-group>
          {{usertemp}}
          <b-form-group
                  :label="'分类['+type_list.length+']'"
                  label-for="type-list"
          >
            <b-form-select id="type-list" :select-size="4" v-model="selectetype" :options="type_list" @change="changetypelist"></b-form-select>
          </b-form-group>
          <b-button-group>
            <b-button variant="success" v-b-modal.edit-newtype>新建</b-button>
            <b-button variant="info" v-b-modal.edit-updatetype>修改</b-button>
            <b-button variant="danger" @click="t_del">删除</b-button>
          </b-button-group>
          <p></p>
          <b-button size="lg" variant="success" block @click="publish">保存</b-button>
        </b-col>
        <b-col cols="3">
          <b-form-group
                  :label="'我的视频['+video_list.length+']'"
                  label-for="video-list"
          >
            <b-form-select id="video-list" :select-size="20" v-model="selectevideo" :options="video_list" @change="changevideolist"></b-form-select>
          </b-form-group>
        </b-col>
        <b-col cols="7">
          <h4>视频详情 <small>{{ filejson }}</small></h4>
          <b-row>
            <b-col sm="6">
              <b-row>
                <b-col>
                  <label for="videotitle">标题:</label>
                </b-col>
                <b-col sm="10">
                  <b-form-input id="videotitle" v-model="video.title"></b-form-input>
                </b-col>
              </b-row>
              <b-row>
                <b-col sm="2">
                  <label for="videodescription">简介:</label>
                </b-col>
                <b-col sm="10">
                  <b-form-textarea id="videodescription"
                                   rows="3"
                                   max-rows="6"
                                   v-model="video.description"
                  ></b-form-textarea>
                </b-col>
              </b-row>
            </b-col>
            <b-col sm="6">
              <b-form-file
                      id="videocover"
                      v-model="coverselect"
                      @change="up_cover"
              ></b-form-file>
              <b-img thumbnail fluid :src="videocover"></b-img>
            </b-col>
          </b-row>
          <b-form-group
                  label="播放列表"
                  label-for="video-list"
          >
            <b-form-select id="file-list" :select-size="15" v-model="videofile" :options="videofile_list"></b-form-select>
          </b-form-group>
          <b-button-group>
            <b-button variant="success" @click="f_moveup">上移</b-button>
            <b-button variant="success" @click="f_movedown">下移</b-button>
          </b-button-group>
          <b-button-group>
            <b-button variant="info" @click="f_edit">修改</b-button>
            <b-button variant="danger" @click="f_del">删除</b-button>
            <b-button variant="success" @click="f_update">更新</b-button>
          </b-button-group>
          <b-button-group>
            <b-button variant="success" v-b-modal.edit-newvideo>新建</b-button>
          </b-button-group>
        </b-col>
      </b-row>
    </b-container>

    <b-modal id="edit-server" title="编辑服务器" size="lg" @ok="s_save">
      <b-row>
        <b-col sm="6">
          <b-form-select id="servereditlist" :select-size="15" v-model="server_urls" :options="server_url" @change="s_change"></b-form-select>
        </b-col>
        <b-col sm="6">
          <b-form-input v-model="server_urls_t"></b-form-input>
          <b-button-group>
            <b-button variant="success" @click="s_new">新建</b-button>
            <b-button variant="info" @click="s_update">修改</b-button>
            <b-button variant="danger" @click="s_del">删除</b-button>
          </b-button-group>
        </b-col>
      </b-row>
    </b-modal>

    <b-modal id="edit-keys" title="编辑账号" size="lg">
      <b-row>
        <b-col sm="4">
          <b-form-select id="keyseditlist" :select-size="15" v-model="selectekey" :options="key_list" @change="u_change"></b-form-select>
        </b-col>
        <b-col sm="8">
          <b-row>
            <b-col>
              <label for="keyname">标识:</label>
            </b-col>
            <b-col sm="10">
              <b-form-input id="keyname" v-model="keyname"></b-form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              地址：
            </b-col>
            <b-col sm="10">
              {{ keyid }}
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <label for="username">昵称:</label>
            </b-col>
            <b-col sm="10">
              <b-form-input id="username" v-model="username"></b-form-input>
            </b-col>
          </b-row>
          <b-row>
            <b-col sm="2">
              <label for="description">简介:</label>
            </b-col>
            <b-col sm="10">
              <b-form-textarea id="description"
                               rows="3"
                               max-rows="6"
                               v-model="description"
              ></b-form-textarea>
            </b-col>
          </b-row>
          <b-row>
            <b-col>
              <b-form-file
                      id="avatar"
                      v-model="avatarselect"
                      @change="up_avatar"
              ></b-form-file>
              <b-img thumbnail fluid :src="avatar"></b-img>
            </b-col>
          </b-row>
          <b-button-group>
            <b-button variant="success" @click="u_new">新建</b-button>
            <b-button variant="info" @click="u_update">修改</b-button>
            <b-button variant="danger" @click="u_del">删除</b-button>
          </b-button-group>
        </b-col>
      </b-row>
    </b-modal>

    <b-modal id="edit-newtype" title="新建分类" @ok="t_new">
      <b-form-group
              label="标题"
              label-for="typetitle"
      >
        <b-form-input v-model="typetitle" trim></b-form-input>
      </b-form-group>
      <b-form-group
              label="标识"
              label-for="typeid"
      >
        <b-form-input v-model="typeid" trim></b-form-input>
      </b-form-group>
    </b-modal>

    <b-modal id="edit-updatetype" title="修改分类" @ok="t_edit">
      <b-form-group
              label="标题"
              label-for="typetitle"
      >
        <b-form-input v-model="typetitle" trim></b-form-input>
      </b-form-group>
      <b-form-group
              label="标识"
              label-for="typeid"
      >
        <b-form-input v-model="typeid" trim></b-form-input>
      </b-form-group>
    </b-modal>

    <b-modal id="edit-newvideo" title="新建视频" @ok="f_upload">
      <b-alert variant="success" show>请使用上传脚本辅助上传！</b-alert>
      <b-form-group
              label="hash"
              label-for="videohash"
      >
        <b-form-input v-model="videohash" trim></b-form-input>
      </b-form-group>
    </b-modal>

  </div>
</template>

<script>
import Axios from 'axios'
import ipfsClient from 'ipfs-http-client'
export default {
  name: 'app',
  data(){
    return {
      template:{
        global:'',
        userlist:'',
        player:'',
      },
      globalfile:{},
      userfile:{},
      ipfsapi:"",
      server_url:['/ip4/127.0.0.1/tcp/5001'],
      ipfskey:'',
      key_list:[],
      selectetype:'',
      type_list:[],
      selectevideo:'',
      video_list:[],
      videofile:'',
      videofile_list:[],
      video:{
        title:'',
        description:'',
      },
      videocover:'',
      coverselect:'',

      server_urls:'',
      server_urls_t:'',
      selectekey:'',

      keyname:'',
      keyid:'',
      username:'',
      description:'',
      avatar:'',
      avatarselect:'',
      userhash:'',
      myhash:'',

      typetitle:'',
      typeid:'',

      videohash:'',
      temphash:'',
      filejson:'',
      usertemp:'',
      cache:{},
    }
  },
  methods:{
    init(){
      Axios.get('./data.json').then((res)=>{
        this.template = res.data.template;
      });
      //服务器列表初始化
      if(localStorage.getItem('videoshare_ipfsapilist')){
        this.server_url = JSON.parse(localStorage.getItem('videoshare_ipfsapilist'));
      }
    },
    // 编辑服务器
    s_change(){
      this.server_urls_t = this.server_urls;
    },
    s_new(){
      this.server_url.push(this.server_urls_t);
    },
    s_update(){
      for(let i=0;i<this.server_url.length;i++){
        if(this.server_url[i]===this.server_urls)this.server_url[i]=this.server_urls_t;
      }
    },
    s_del(){
      for(let i=this.server_url.length;i>0;i--){
        if(this.server_url[i]===this.server_urls)this.server_url.splice(i, 1);
      }
    },
    s_save(){
      localStorage.setItem('videoshare_ipfsapilist',JSON.stringify(this.server_url))
    },

    changeserverlist(){
      const ipfs = ipfsClient(this.ipfsapi);
      ipfs.key.list((err, keys) => {
        for(let i=0;i<keys.length;i++){
          this.key_list.push({
            "text":keys[i].name,
            "value":keys[i].id,
          })
        }
      });
      if(!this.globalfile.hash){
        ipfs.object.links(this.template.global, (err, res) => {
          for (let i = 0; i < res.length; i++) {
            if(res[i].Name==='global.json'){
              this.globalfile = {
                hash:res[i].Hash.string,
                size:res[i].Tsize,
              };
              break;
            }
          }
        })
      }
    },
    // 编辑账号
    u_change(){
      const ipfs = ipfsClient(this.ipfsapi);
      this.keyid = this.selectekey;
      for (let i=0;i<this.key_list.length;i++){
        if(this.key_list[i].value===this.keyid)this.keyname=this.key_list[i].text;
      }
      ipfs.name.resolve('/ipns/'+this.keyid,(err, name)=>{
        this.myhash = name;
        ipfs.object.links(name.replace(/\/ipfs\//,''), (err, links) => {
          if(links.length<0){
            console.log('新账号')
          }
          let flag = false;
          for(let i=0;i<links.length;i++){
            if(links[i].Name==='user.json'){
              flag=true;
              this.userhash = links[i].Hash.string;
              break;
            }
          }
          if(!flag){
            console.log('已绑定其他项目')
          }else{
            console.log('有账号',this.userhash);
            ipfs.cat(this.userhash,(err, res)=>{
              res = JSON.parse(res);
              this.username = res.username;
              this.description = res.description;
              this.avatar = res.avatar;
            });
          }
        });

      });
    },
    async up_avatar(){
      const ipfs = ipfsClient(this.ipfsapi);
      setTimeout(async()=>{
        console.log(this.avatarselect);
        if(this.avatarselect){
          let file = await ipfs.add(this.avatarselect);
          this.avatar = '/ipfs/'+file[0].hash;
        }
      },50);
    },
    async u_new(){
      const ipfs = ipfsClient(this.ipfsapi);
      const key = await ipfs.key.gen(this.keyname,{type:'rsa',size: 2048});
      this.keyid = key.id;
      let user = {
        id:this.keyid,
        username:this.username,
        avatar:this.avatar,
        description:this.description,
        type:[]
      };
      const results = await ipfs.add(Buffer.from(JSON.stringify(user)));
      let newhash = await ipfs.object.patch.addLink(this.template.userlist, {
        name: 'user.json',size: results[0].size, cid:results[0].hash
      });
      newhash = await ipfs.object.patch.addLink(newhash, {
        name: 'global.json',size: this.globalfile.size, cid:this.globalfile.hash
      });
      const res = await ipfs.name.publish(newhash.string,{key:this.keyid,lifetime:'168h'});
      console.log(res);
    },
    async u_update(){
      const ipfs = ipfsClient(this.ipfsapi);
      let user = await ipfs.cat(this.userhash+'/user.json');
      user = JSON.parse(user);
      user.username = this.username;
      user.description = this.description;
      user.avatar = this.avatar;
      const results = await ipfs.add(Buffer.from(JSON.stringify(user)));
      let newhash = await ipfs.object.patch.rmLink(this.userhash,{Name: 'user.json'});
      newhash = await ipfs.object.patch.addLink(newhash, {
        name: 'user.json',size: results[0].size, cid:results[0].hash
      });
      const res = await ipfs.name.publish(newhash.string,{key:this.keyid,lifetime:'168h'});
      console.log(res);
    },
    async u_del(){
      const ipfs = ipfsClient(this.ipfsapi);
      ipfs.key.rm(this.keyname);
    },
    // 编辑类型
    async changeuserlist(){
      const ipfs = ipfsClient(this.ipfsapi);
      this.usertemp = await ipfs.name.resolve('/ipns/'+this.ipfskey);
      this.usertemp = this.usertemp.substr(6);
      let res = await ipfs.object.links(this.usertemp);
      for (let i = 0; i < res.length; i++) {
        if(res[i].Name==='user.json'){
          this.userfile = {
            hash:res[i].Hash.string,
            size:res[i].Tsize,
          };
          break;
        }
      }
      let typetemp = await ipfs.cat(this.usertemp+'/user.json');
      typetemp = JSON.parse(typetemp);
      for(let i=0;i<typetemp.type.length;i++){
        this.type_list.push({
          "text":typetemp.type[i].title,
          "value":typetemp.type[i].name,
        });
      }
    },
    async t_new(){
      const ipfs = ipfsClient(this.ipfsapi);
      let typetemp = await ipfs.cat(this.usertemp+'/user.json');
      typetemp = JSON.parse(typetemp);
      typetemp.type.push({
        title:this.typetitle,
        name:this.typeid,
      });
      const results = await ipfs.add(Buffer.from(JSON.stringify(typetemp)));
      let newhash = await ipfs.object.patch.rmLink(this.usertemp,{Name: 'user.json'});
      newhash = await ipfs.object.patch.addLink(newhash, {
        name: 'user.json',size: results[0].size, cid:results[0].hash
      });
      const results2 = await ipfs.add(Buffer.from(JSON.stringify([])));
      newhash = await ipfs.object.patch.addLink(newhash, {
        name: this.typeid+'.json',size: results2[0].size, cid:results2[0].hash
      });
      this.usertemp = newhash.string;
      console.log(this.usertemp);
      for(let i=0;i<typetemp.type.length;i++){
        this.type_list.push({
          "text":typetemp.type[i].title,
          "value":typetemp.type[i].name,
        });
      }
    },
    async t_edit(){
      const ipfs = ipfsClient(this.ipfsapi);
      let typetemp = await ipfs.cat(this.usertemp+'/user.json');
      typetemp = JSON.parse(typetemp);
      for (let i = 0; i < typetemp.type.length; i++) {
        if(typetemp.type[i].name === this.selectetype){
          typetemp.type[i].title = this.typetitle;
        }
      }
      const results = await ipfs.add(Buffer.from(JSON.stringify(typetemp)));
      let newhash = await ipfs.object.patch.rmLink(this.usertemp,{Name: 'user.json'});
      newhash = await ipfs.object.patch.addLink(newhash, {
        name: 'user.json',size: results[0].size, cid:results[0].hash
      });
      this.usertemp = newhash.string;
      this.type_list = [];
      for(let i=0;i<typetemp.type.length;i++){
        this.type_list.push({
          "text":typetemp.type[i].title,
          "value":typetemp.type[i].name,
        });
      }
    },
    async t_del(){
      const ipfs = ipfsClient(this.ipfsapi);
      let typetemp = await ipfs.cat(this.usertemp+'/user.json');
      typetemp = JSON.parse(typetemp);
      let ind=-1;
      for (let i = 0; i < typetemp.type.length; i++) {
        if(typetemp.type[i].name === this.selectetype){
          ind = i;
          break;
        }
      }
      let r = confirm('确认删除?');
      if(!r)return;
      typetemp.type.splice(ind,1);
      const results = await ipfs.add(Buffer.from(JSON.stringify(typetemp)));
      let newhash = await ipfs.object.patch.rmLink(this.usertemp,{Name: 'user.json'});
      newhash = await ipfs.object.patch.addLink(newhash, {
        name: 'user.json',size: results[0].size, cid:results[0].hash
      });
      newhash = await ipfs.object.patch.rmLink(newhash,{Name: this.selectetype+'.json'});
      this.usertemp = newhash.string;

      this.type_list = [];
      for(let i=0;i<typetemp.type.length;i++){
        this.type_list.push({
          "text":typetemp.type[i].title,
          "value":typetemp.type[i].name,
        });
      }
    },
    async changetypelist(){
      const ipfs = ipfsClient(this.ipfsapi);
      let typetemp = await ipfs.cat(this.usertemp+'/'+this.selectetype+'.json');
      typetemp = JSON.parse(typetemp);
      this.video_list = [];
      for(let i=0;i<typetemp.length;i++){
        this.video_list.push({
          "text":typetemp[i].title,
          "value":typetemp[i].url,
        });
      }
    },
    //视频列表操作
    async changevideolist(){
      const ipfs = ipfsClient(this.ipfsapi);
      this.temphash = this.selectevideo.substr(6);
      let vfile = await ipfs.object.get(this.temphash);
      this.filejson = vfile['files.json'].string;
      let videoinfo = await ipfs.cat(this.filejson);
      videoinfo = JSON.parse(videoinfo);
      this.video.title = videoinfo.title;
      this.video.description = videoinfo.description;
      this.videocover = videoinfo.cover;
      for(let i=0;i<videoinfo.files.length;i++){
        this.videofile_list.push({
          "text":videoinfo.files[i].title,
          "value":videoinfo.files[i].url,
        });
      }
    },
    async f_moveup(){
      const ipfs = ipfsClient(this.ipfsapi);
      let ind=-1;
      for(let i=0;i<this.videofile_list.length;i++){
        if(this.videofile_list[i].value===this.videofile){
          ind = i;
          break;
        }
      }
      if(ind<=0)return;
      let videoinfo = await ipfs.cat(this.filejson);
      videoinfo = JSON.parse(videoinfo);
      let temp = videoinfo.files[ind];
      videoinfo.files[ind]=videoinfo.files[ind-1];
      videoinfo.files[ind-1] = temp;
      const results = await ipfs.add(Buffer.from(JSON.stringify(videoinfo)));
      this.filejson = results[0].hash;
      this.videofile_list=[];
      for(let i=0;i<videoinfo.files.length;i++){
        this.type_list.push({
          "text":videoinfo.files[i].title,
          "value":videoinfo.files[i].url,
        });
      }
    },
    async f_movedown(){
      const ipfs = ipfsClient(this.ipfsapi);
      let ind=-1;
      for(let i=0;i<this.videofile_list.length;i++){
        if(this.videofile_list[i].value===this.videofile){
          ind = i;
          break;
        }
      }
      if(ind<0||ind>=this.videofile_list.length-1)return;
      let videoinfo = await ipfs.cat(this.filejson);
      videoinfo = JSON.parse(videoinfo);
      let temp = videoinfo.files[ind];
      videoinfo.files[ind]=videoinfo.files[ind+1];
      videoinfo.files[ind+1] = temp;
      const results = await ipfs.add(Buffer.from(JSON.stringify(videoinfo)));
      this.filejson = results[0].hash;
      this.videofile_list=[];
      for(let i=0;i<videoinfo.files.length;i++){
        this.videofile_list.push({
          "text":videoinfo.files[i].title,
          "value":videoinfo.files[i].url,
        });
      }
    },
    async f_edit(){
      const ipfs = ipfsClient(this.ipfsapi);
      let ind=-1;
      for(let i=0;i<this.videofile_list.length;i++){
        if(this.videofile_list[i].value===this.videofile){
          ind = i;
          break;
        }
      }
      let title = prompt('编辑文件名',this.videofile_list[ind].text);
      if(title===null)return;
      let videoinfo = await ipfs.cat(this.filejson);
      videoinfo = JSON.parse(videoinfo);
      videoinfo.files[ind].title = title;
      const results = await ipfs.add(Buffer.from(JSON.stringify(videoinfo)));
      this.filejson = results[0].hash;
      this.videofile_list=[];
      for(let i=0;i<videoinfo.files.length;i++){
        this.videofile_list.push({
          "text":videoinfo.files[i].title,
          "value":videoinfo.files[i].url,
        });
      }
    },
    async f_del(){
      const ipfs = ipfsClient(this.ipfsapi);
      let ind=-1;
      for(let i=0;i<this.videofile_list.length;i++){
        if(this.videofile_list[i].value===this.videofile){
          ind = i;
          break;
        }
      }
      let r = confirm('确认删除?');
      if(!r)return;
      let videoinfo = await ipfs.cat(this.filejson);
      videoinfo = JSON.parse(videoinfo);
      videoinfo.files.splice(ind,1);
      const results = await ipfs.add(Buffer.from(JSON.stringify(videoinfo)));
      this.filejson = results[0].hash;
      this.videofile_list=[];
      for(let i=0;i<videoinfo.files.length;i++){
        this.videofile_list.push({
          "text":videoinfo.files[i].title,
          "value":videoinfo.files[i].url,
        });
      }
    },
    async f_update(){
      const ipfs = ipfsClient(this.ipfsapi);
      let videoinfo = await ipfs.cat(this.filejson);
      videoinfo = JSON.parse(videoinfo);
      videoinfo.title = this.video.title;
      videoinfo.description = this.video.description;
      videoinfo.cover = this.videocover;
      const results = await ipfs.add(Buffer.from(JSON.stringify(videoinfo)));
      this.filejson = results[0].hash;
      let newhash = await ipfs.object.patch.addLink(this.template.player,{
        name: 'files.json',size: results[0].size, cid:results[0].hash
      });
      newhash = await ipfs.object.patch.addLink(newhash,{
        name: 'global.json',size: this.globalfile.size, cid:this.globalfile.hash
      });
      newhash = await ipfs.object.patch.addLink(newhash,{
        name: 'user.json',size: this.userfile.size, cid:this.userfile.hash
      });
      this.temphash = newhash.string;

      let typetemp = await ipfs.cat(this.usertemp+'/'+this.selectetype+'.json');
      typetemp = JSON.parse(typetemp);
      for (let i = 0; i < typetemp.length; i++) {
        if(typetemp[i].url===this.selectevideo){
          typetemp[i]={
            title:videoinfo.title,
            cover:videoinfo.cover,
            url:'/ipfs/'+this.temphash
          }
        }
      }
      const results2 = await ipfs.add(Buffer.from(JSON.stringify(typetemp)));
      let newhash2 = await ipfs.object.patch.rmLink(this.usertemp,{Name: this.selectetype+'.json'});
      newhash2 = await ipfs.object.patch.addLink(newhash2, {
        name: this.selectetype+'.json',size: results2[0].size, cid:results2[0].hash
      });
      this.usertemp = newhash2.string;

      this.video_list = [];
      for(let i=0;i<typetemp.length;i++){
        this.video_list.push({
          "text":typetemp[i].title,
          "value":typetemp[i].url,
        });
      }
    },
    //文件操作
    async f_upload(){
      const ipfs = ipfsClient(this.ipfsapi);
      let results = await ipfs.object.get(this.videohash);
      let videoinfo = await ipfs.cat(this.videohash);
      videoinfo = JSON.parse(videoinfo);
      let newhash = await ipfs.object.patch.addLink(this.template.player, {
        name: 'files.json',size: results.size, cid:this.videohash
      });
      newhash = await ipfs.object.patch.addLink(newhash,{
        name: 'global.json',size: this.globalfile.size, cid:this.globalfile.hash
      });
      newhash = await ipfs.object.patch.addLink(newhash,{
        name: 'user.json',size: this.userfile.size, cid:this.userfile.hash
      });
      let playerhash = newhash.string;

      let typetemp = await ipfs.cat(this.usertemp+'/'+this.selectetype+'.json');
      typetemp = JSON.parse(typetemp);
      typetemp.push({
        title:videoinfo.title,
        cover:videoinfo.cover,
        url:'/ipfs/'+playerhash
      });
      const results2 = await ipfs.add(Buffer.from(JSON.stringify(typetemp)));
      let newhash2 = await ipfs.object.patch.rmLink(this.usertemp,{Name: this.selectetype+'.json'});
      newhash2 = await ipfs.object.patch.addLink(newhash2, {
        name: this.selectetype+'.json',size: results2[0].size, cid:results2[0].hash
      });
      this.usertemp = newhash2.string;
      this.video_list = [];
      for(let i=0;i<typetemp.length;i++){
        this.video_list.push({
          "text":typetemp[i].title,
          "value":typetemp[i].url,
        });
      }
    },
    async up_cover(){
      const ipfs = ipfsClient(this.ipfsapi);
      setTimeout(async()=>{
        console.log(this.coverselect);
        if(this.coverselect){
          let file = await ipfs.add(this.coverselect);
          this.videocover = '/ipfs/'+ file[0].hash;
        }
      },50);
    },
    async publish(){
      const ipfs = ipfsClient(this.ipfsapi);
      let res = await ipfs.object.links(this.usertemp);
      let userjson = {};
      let tempjson = [];
      let name = '';
      for (let i = 0; i < res.length; i++) {
        if(res[i].Name==='user.json'){
          userjson = {
            hash:res[i].Hash.string,
            size:res[i].Tsize,
          };
          break;
        }
      }
      let res2 = await ipfs.cat(userjson.hash);
      res2 = JSON.parse(res2);
      for (let i = 0; i < res2.type.length; i++) {
        for (let j = 0; j < res.length; j++) {
          if(res[j].Name===res2.type[i].name+'.json'){
            tempjson.push({
              hash:res[j].Hash.string,
              size:res[j].Tsize,
              name:res2.type[i].name
            });
            break;
          }
        }
      }
      let newhash = await ipfs.object.patch.addLink(this.template.userlist, {
        name: 'user.json',size: userjson.size, cid:userjson.hash
      });
      newhash = await ipfs.object.patch.addLink(newhash,{
        name: 'global.json',size: this.globalfile.size, cid:this.globalfile.hash
      });
      for (let i = 0; i < tempjson.length; i++) {
        newhash = await ipfs.object.patch.addLink(newhash, {
          name: tempjson[i].name+'.json',size: tempjson[i].size, cid:tempjson[i].hash
        });
      }
      let res4 = await ipfs.key.list();
      for (let i = 0; i < res4.length; i++) {
        if(res4[i].id === this.ipfskey){
          name = res4[i].name;
          break;
        }
      }
      const res3 = await ipfs.name.publish(newhash.string,{key:name,lifetime:'168h'});
      console.log(res3);
    },
  },
  created() {
    this.init()
  },
}
</script>

<style>
</style>
