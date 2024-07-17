<script lang="ts">
	import { raw_data } from '../stores/websocket';
	import { transformations } from './RiggedModel';
	let data: any;
	let pose: any;

    let pose_raw : any;

	raw_data.subscribe((value) => {
		data = JSON.stringify(value, null, 2);
	});
	transformations.subscribe((value) => {
        pose_raw = value;
		pose = JSON.stringify(value, null, 2);
	});

	function download(data, filename, type) {
		var file = new Blob([data], { type: type });
		if (window.navigator.msSaveOrOpenBlob)
			// IE10+
			window.navigator.msSaveOrOpenBlob(file, filename);
		else {
			// Others
			var a = document.createElement('a'),
				url = URL.createObjectURL(file);
			a.href = url;
			a.download = filename;
			document.body.appendChild(a);
			a.click();
			setTimeout(function () {
				document.body.removeChild(a);
				window.URL.revokeObjectURL(url);
			}, 0);
		}
	}

	function triggerdownload() {
		download(JSON.stringify(pose_raw), 'transformations.json', 'text/plain');
	}
</script>

<button on:click={() => triggerdownload()}>Download Pose</button>

<div class="card" style="width: 20rem;">
	<div class="card-body">
		<h5 class="card-title">Live Video Feed</h5>
		<pre>{data}</pre>
	</div>
</div>

<div class="card" style="width: 20rem;">
	<div class="card-body">
		<h5 class="card-title">Live Video Feed</h5>
		<pre>{pose}</pre>
	</div>
</div>
