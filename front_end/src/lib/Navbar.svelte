<script>
	// import Beranda from "./Beranda.svelte";
	// import Profile from "./Profile.svelte";
	
	export let menu = 1;
</script>

<!-- <style>
	ul#menu li{
		display : inline;
	}
</style> -->

<ul id="menu">
	<li><a href="/" on:click|preventDefault={() => (menu = 1)}>Beranda</a></li> |
	<li><a href="/" on:click|preventDefault={() => (menu = 2)}>Profile</a></li>
</ul>

{#if menu === 1}
<p>
  Ini adalah halaman beranda
</p>
{:else if menu === 2}
<p>
  Ini adalah halaman profile
</p>
{:else}
<h1>
	Page Not Found
</h1>
{/if}

<style>
  /* Import Google Font */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

/* Base styling */
body {
  font-family: 'Roboto', Arial, sans-serif;  /* Fallback font */
}


html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  font-family: 'Roboto', Arial, sans-serif;
  background: #f4f4f4;
  color: #333;
}


</style>

