<template>
  <div class="container">
    <div class="section">
      <div class="notification">
        <p>あなたの書いたラフスケッチをアップロードしましょう</p>
        <p>※変換に30秒程度かかる場合があります</p>
        <p>※処理の都合上、1辺が600pxのサイズに縮小されます</p>
      </div>
      <div class="file is-large is-centered">
        <label class="file-label">
          <input @change="fileChange" class="file-input" type="file" name="file" />
          <span class="file-cta">
            <span class="file-icon">
              <i class="fa fa-upload"></i>
            </span>
            <span class="file-label">
              ラフ画をアップロードして線画化を試す
            </span>
          </span>
        </label>
        <a :class="['button', 'is-large', { 'is-loading': isLoading }]">{{ isLoading ? "処理中": "進捗状況" }}</a>
      </div>
    </div>

    <div class="section">
      <div class="columns">
        <div class="column" @dragover="dragOver" @drop="dropFile">
          <h2></h2>
          <figure class="image">
            <img :src="preSrc">
          </figure>
        </div>
        <div class="column is-centered">
          <figure class="image">
            <img :src="simplifiedSrc">
          </figure>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>

<script>
  import axios from 'axios'

  export default {
    data: function () {
      return {
        isDragOver: false,
        file: null,
        isLoading: false,
        simplifiedSrc: "static/simplifiedSample.png",
        preSrc: "static/sample.jpg"
      }
    },
    methods: {
      fileChange: function (event) {
        this.file = event.target.files[0]
        this.preSrc = URL.createObjectURL(this.file)
        this.apiRequest()
      },
      apiRequest: function () {
        const fd = new FormData()
        fd.append('file', this.file)

        const opt = {
          responseType: 'blob',
          timeout: 30000
        }

        this.isLoading = true
        axios.post('/api/simplify', fd, opt).then(res => {
          this.isLoading = false
          this.simplifiedSrc = URL.createObjectURL(res.data)
        }).catch(err => {
          console.error('err:', err)
          this.isLoading = false
        });
      },
      dropFile: function (evt) {
        evt.stopPropagation()
        evt.preventDefault()
        let files = evt.dataTransfer.files
        this.file = files[0]
        this.isDragOver = true
        this.apiRequest()
      },
      dragOver: function (evt) {
        evt.stopPropagation()
        evt.preventDefault()
        this.isDragOver = false
      }
    }
  }
</script>
