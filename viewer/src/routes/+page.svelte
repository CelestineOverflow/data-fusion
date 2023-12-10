<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import UdpTester from "../components/UdpTester.svelte";
    import {onMount} from "svelte";
    import Ik from "../components/Ik.svelte";
    import {connectToWebSocket } from "../stores/websocket";
    import Camera from "../components/Camera.svelte";
    import RawData from "../components/RawData.svelte";
    let data : any;

    onMount(() => {
        connectToWebSocket();
    });

</script>

<Navbar />
<UdpTester />




<div class="container">
    <div class="row">
      <div class="col-sm">
        <Ik />
      </div>
      <div class="col-sm">
        <Camera />
      </div>
      <div class="col-sm">
        <RawData />
      </div>
    </div>
  </div>


