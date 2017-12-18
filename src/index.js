import './index.css'
import Vue from 'vue';
import App from './components/App.vue';
import Dropzone from 'dropzone'
import axios from 'axios'

(function () {
  new Vue({
    el: '#app',
    render: h => h(App)
  })

  const dz = new Dropzone("#dz")
  dz.on("addedfile", function(file) {
    const fd = new FormData()
    fd.append('file', file)

    axios.post('/api/simplify', fd, {responseType: 'blob', timeout: 30000}).then(res => {
      console.log(res)
      const img = document.getElementById("response")
      img.src = URL.createObjectURL(res.data)
    }).catch(err => {
        console.error('err:', err);
    });
  })
})()

