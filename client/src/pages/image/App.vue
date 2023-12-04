<template>
  <nav class="navbar navbar-expand-lg bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">EZAble</a>
    </div>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavDropdown"
            aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse justify-content-md-center" id="navbarNavDropdown">
      <ul class="navbar-nav">
        <li class="nav-item">
          <a class="nav-link" href="/">Audio & Image Detection</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="/audio">Audio Detection</a>
        </li>
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Image Detection</a>
        </li>
      </ul>
    </div>
  </nav>
  <div class="app">
    <div class="container text-center">
      <div class="row">
        <div class="col">
          <div class="card">
            <div class="card-body">
              <camera-item @captured-image="handleCapturedImage"></camera-item>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="card">
            <div class="card-body">
              <detection-result-item :capturedImage="capturedImage"
                                     :capturedAudio="capturedAudio"></detection-result-item>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import CameraItem from '@/components/Camera.vue'
import DetectionResultItem from "@/components/DetectionResult";

export default {
  name: 'App',
  data() {
    return {
      capturedImage: null,
      capturedAudio: null,
    }
  },
  components: {
    DetectionResultItem,
    CameraItem,
  },
  methods: {
    handleCapturedImage(data) {
      this.capturedImage = data
    },
    handleCapturedAudio(data) {
      this.capturedAudio = data
    }
  },
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
}

body {
  background: url('@/assets/bg.png') no-repeat;
  background-size: cover;
}

.app {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-family: 'VT323', monospace;
}

.main {
  width: 30%;
  height: 35%;
  border: solid 1px rgb(0, 0, 0);
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

h1 {
  font-size: 50px;
}

p {
  font-size: 30px;
  margin-bottom: 20px;
}

.camera-icon {
  width: 25px;
  height: 25px;
}

.camera-icon:hover {
  cursor: pointer;
}
</style>