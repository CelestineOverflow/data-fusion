<script lang="ts">
    import type { raw_data } from "../stores/server_stats";

    import Camera from "../components/Camera.svelte";
    import Cube from "../components/Cube.svelte";
    import Gtlf from "../components/Gtlf.svelte";
    import Navbar from "../components/Navbar.svelte";
    import UdpTester from "../components/UdpTester.svelte";
    import { raw_data as raw_data_store } from "../stores/server_stats";
    let raw_data : any;
    raw_data_store.subscribe((value) => {
        raw_data = value;
    });
</script>
<p>Raw data: {JSON.stringify(raw_data)}</p>
<Navbar />
<UdpTester />
<Gtlf />
<!-- s -->
