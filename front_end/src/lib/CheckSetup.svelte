<script>
	import Camera from './Camera.svelte';
import IK_SolverT from './IK_Solver_t.svelte';
	import RawData from './RawData.svelte';

</script>

<div id="container">
	<IK_SolverT />
	<div id="text">
		<section>
            <Camera />
            <h1>Check Raw Data Below</h1>
            <RawData />
        </section>
	</div>
</div>

<style>
	#container {
		display: flex; /* Establishes a flex container */
		align-items: center; /* Vertically align items in the middle */
		justify-content: space-around; /* Distributes space around items */
		height: 100vh; /* Optional: takes full viewport height */
	}

	#text {
		flex: 1; /* Allows the text block to grow and shrink */
		padding: 20px; /* Adds some spacing around the text */
	}
    .img {
    width: 20%;  /* Sets the width to 50% of its container */
    height: auto;  /* Sets the height to auto, preserving the aspect ratio */
    flex: 1;  /* Allows the image block to grow and shrink */
    padding: 20px;  /* Adds some spacing around the image */
}
</style>
