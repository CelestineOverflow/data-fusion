<script>
	import StartUp from '$lib/AboutThis.svelte';
	// import IkSolverT from '$lib/IK_Solver_t.svelte';
    import MergedXR_IK from './../lib/MergedXR_IK.svelte';
	export let menu = 1;
    import {connectToWebSocket} from './../stores/websocket';
    import {onMount} from "svelte";
	import CheckSetup from '$lib/CheckSetup.svelte';
	import MergedXrIk from './../lib/MergedXR_IK.svelte';
	import RawData from '$lib/RawData.svelte';
	import { triggerdownload } from '$lib/RiggedModel';
    onMount(() => {
        connectToWebSocket();
    });
</script>
<RawData />
<button on:click={() => triggerdownload()}>Download Pose</button>
<MergedXrIk />
<!-- 
<body>
    
    <ul id="menu">
        <li id="banner">Data Fusion</li>
        <li><a href="/" on:click|preventDefault={() => (menu = 1)}>About This Project</a></li>
        <li><a href="/" on:click|preventDefault={() => (menu = 2)}>Check Setup</a></li>
        <li><a href="/" on:click|preventDefault={() => (menu = 3)}>XR/VR</a></li>
        
    </ul>

    {#if menu === 1}
    <p>
      <StartUp />
    </p>
    {:else if menu === 2}
    <p>
      <CheckSetup />
    </p>
    {:else if menu === 3}
    <p>
      <MergedXrIk />
    </p>
    {:else}
    <h1>
        Page Not Found
    </h1>
    {/if}

</body>  -->
<style>
	/* Import Google Font */
	@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

	/* Base styling */
	body {
	  font-family: 'Roboto', Arial, sans-serif; 
	  margin: 0;
	  padding: 0;
	  background-color: #f4f4f4; /* Light gray background */
	}

    #menu #banner {
      color: #ffffff; /* Dark grey text color */
      font-size: 20px; /* Larger text size */
      margin-right: 20px; /* More space around the banner */
    }

	#menu {
	  list-style: none;
	  background-color: #333; /* Dark background for the navbar */
	  margin: 0;
	  padding: 0;
	  text-align: center;
	}

	#menu li {
	  display: inline;
	  margin-right: 10px;
	}

	#menu a {
	  text-decoration: none;
	  color: white; /* White text color */
	  padding: 10px 15px;
	  display: inline-block;
	}

	#menu a:hover {
	  background-color: #555; /* Darker background on hover */
	}

	#menu a:focus {
	  outline: none;
	  background-color: #777; /* Background change on focus */
	}

	/* Active link style */
	#menu a:active {
	  background-color: #999; /* No purple, just a lighter grey */
	}
</style>
