<script lang="ts">
	import { raw_data } from '../stores/store';
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
</script>

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
