<template>
  <div class="recorder">
    <button class="button" @click="toggleRecorder()">
      <span v-if="!mediaRecorder">Start Recorder</span>
      <span v-else>Stop Recorder</span>
    </button>
    <button v-if="newAudio" class="recorder-download">
      <a id="downloadAudio" download="Capture.wav" class="button" role="button" @click="downloadAudio">
        Download
      </a>
    </button>
    <audio v-if="newAudio" :src="newAudioURL" id="audioPlay" controls></audio>
  </div>
</template>

<script>


export default {
  name: 'RecorderItem',
  data() {
    return {
      mediaRecorder: null,
      stream: null,
      newAudio: null, // webm format
      recordedChunks: [],
      audioMIMEString: null,
      wavAudio: null
    }
  },
  computed: {
    newAudioURL() {
      return URL.createObjectURL(this.newAudio)
    }
  },
  methods: {
    startRecording () {
      const msOfAudio = 1500

      const constraints = (window.constraints = {
        audio: {
          channelCount: 2
        },
        video: false
      })

      navigator.mediaDevices
        .getUserMedia(constraints)
        .then(stream => {
          this.stream = stream
          this.mediaRecorder = new MediaRecorder(stream)
          this.newAudio = null
          this.recordedChunks = []
          this.mediaRecorder.addEventListener("dataavailable", e => {
            if (e.data.size > 0) {
              this.recordedChunks.push(e.data)
            }
          })
          this.mediaRecorder.start(msOfAudio)
        })
        .catch(error => {
          alert(error, "May the browser didn't support or there is some errors.")
        })

      setTimeout(this.stopRecording, msOfAudio)
    },
    stopAudioStream () {
      const tracks = this.stream.getTracks()
      tracks.forEach(track => {
        track.stop()
      })
      console.log('Recorder closed')
    },
    async stopRecording() {
      this.mediaRecorder.addEventListener("stop", async () => {
        // when trying to convert the audio to WAV format, simply changing param 'type' does not work
        // this.newAudio = new Blob(this.recordedChunks, {type: 'audio/wav; codecs=MS_PCM'});
        // while, an working way is: Blob --> AudioBuffer --> WAV file
        this.newAudio = new Blob(this.recordedChunks)
        this.newAudioArrayBuffer = await this.newAudio.arrayBuffer()
        let toWav = require('audiobuffer-to-wav')
        let converter = require('base64-arraybuffer')


        const context = new AudioContext();
        await context.decodeAudioData(this.newAudioArrayBuffer, (buffer) => {
          this.wavAudio = toWav(buffer);
          this.audioMIMEString = converter.encode(this.wavAudio)
          console.log(this.audioMIMEString)
          this.$emit('captured-audio', this.audioMIMEString)
        })
      })
      this.mediaRecorder.stop()
      this.stopAudioStream()
      this.mediaRecorder = null
      this.stream = null
    },
    toggleRecorder() {
      if (!this.mediaRecorder) {
        this.startRecording()
      } else {
        this.stopRecording()
      }
    },
    downloadAudio() {
      // directly inserting the MIME string into the 'href' property doesn't work in this case
      // since the MIME string of a WAV file is too long for a GET request
      const download = document.getElementById("downloadAudio");
      const file = new File([this.wavAudio], 'capture.wav', {
        type: 'audio/wav',
      })
      const url = URL.createObjectURL(file, {oneTimeOnly: true})
      download.setAttribute("href", url);
    }
  }
}
</script>


<!--<style>-->

<!--.wrapper {-->
<!--  position: relative;-->
<!--  display: flex;-->
<!--  align-items: center;-->
<!--  justify-content: center;-->
<!--  flex-direction: column;-->
<!--  width: 50%;-->
<!--  height: 90%;-->
<!--  background-color: white;-->
<!--  border: solid 2px rgb(0, 0, 0);-->
<!--}-->

<!--button {-->
<!--  border: solid 1px rgb(0, 0, 0);-->
<!--  /*font-size: 10px;*/-->
<!--  cursor: pointer;-->
<!--}-->

<!--.button {-->
<!--  width: 140px;-->
<!--  height: 40px;-->
<!--}-->
<!--</style>-->