<script lang="ts">
	import { onMount } from 'svelte';
	import * as THREE from 'three';
	import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
	import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
	import { MeshToonMaterial, TextureLoader } from 'three';
	import { OutlineEffect } from 'three/examples/jsm/effects/OutlineEffect.js';

	let canvas: HTMLCanvasElement;
	let renderer: THREE.WebGLRenderer;
	let scene: THREE.Scene;
	let camera: THREE.PerspectiveCamera;
	let controls: OrbitControls;
	let effect: OutlineEffect;
	let mixers: THREE.AnimationMixer[] = [];

	onMount(() => {
		init();
		window.addEventListener('resize', onResize);
		return () => {
			window.removeEventListener('resize', onResize);
		};
	});

	function loadModelWithAnimation(filename, scale, position, rotation) {
		const loader = new GLTFLoader();
		loader.load(
			filename,
			(gltf) => {
				let mesh = gltf.scene;
				mesh.scale.set(scale, scale, scale);
				mesh.position.set(position[0], position[1], position[2]);
				mesh.rotation.set(rotation[0], rotation[1], rotation[2]);

				scene.add(mesh);
				let mixer = new THREE.AnimationMixer(gltf.scene);
				gltf.animations.forEach((clip) => {
					const action = mixer.clipAction(clip);
					action.play();
				});
				mixers.push(mixer);
			},
			(xhr) => {
				console.log((xhr.loaded / xhr.total) * 100 + '% loaded');
			},
			(error) => {
				console.error('An error happened', error);
			}
		);
	}

	function init() {
		renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
		let width = window.innerWidth / 2;
		let height = window.innerHeight;
		renderer.setSize(width, height);
		renderer.setClearColor(0xffffff);
		effect = new OutlineEffect(renderer);

		camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 2000);
		camera.position.set(0, 10, 0);

		scene = new THREE.Scene();

		controls = new OrbitControls(camera, renderer.domElement);

		const ambientLight = new THREE.AmbientLight(0xffffff, 1);
		scene.add(ambientLight);

		const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
		directionalLight.position.set(0, 50, 50);
		scene.add(directionalLight);
		loadModelWithAnimation('imus/imu_6.glb', 1, [-3, 0, -2], [0, 0.5, (-60 * Math.PI) / 180]);
		render();
	}

	function onResize() {
		renderer.setSize(window.innerWidth, window.innerHeight);
		camera.aspect = window.innerWidth / window.innerHeight;
		camera.updateProjectionMatrix();
	}

	function render() {
		requestAnimationFrame(render);
		controls.update();
		for (let mixer of mixers) {
			mixer.update(0.01);
		}
		renderer.render(scene, camera);
		effect.render(scene, camera);
	}
</script>

<canvas bind:this={canvas}></canvas>
