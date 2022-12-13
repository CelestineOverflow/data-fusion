<script lang="ts">
	export let name: string;
	import { onMount } from "svelte";
	import * as THREE from "three";
    import Cube from "./components/Cube.svelte";
    import Tabs from "./components/Tabs.svelte";
	const scene = new THREE.Scene();
</script>

<main>
	<Tabs />
</main>

<style>
	main {
		text-align: center;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
