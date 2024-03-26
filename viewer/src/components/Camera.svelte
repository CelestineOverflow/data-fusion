
<script>
    // You can dynamically change this URL if needed
    const videoStreamUrl = 'http://localhost:8080/my_camera';
  </script>
  



    <div class="card" style="width: 40rem;">

        <div class="card-body">
          <h5 class="card-title">Live Video Feed</h5>
          <img src={videoStreamUrl} alt="Live Video Stream">
        </div>
      </div>
  
  <style>
    img {
      /* You can apply custom styles if needed */
      width: 100%;
      max-width: 640px; /* Set a max-width if you want to control the video size */
      height: auto;
    }
  </style>
  