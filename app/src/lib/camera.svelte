<script>
	const videoStreamUrl = 'https://192.168.31.58:8080/my_camera';
</script>

<div class="card" style="width: 40rem;">
	<div class="card-body">
		<img src={videoStreamUrl} alt="Live Video Stream" />
	</div>
</div>

<style>
	img {
		width: 100%;
		max-width: 640px; 
		height: auto;
	}
</style>
