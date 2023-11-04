<script lang="ts">
    import Navbar from "../components/Navbar.svelte";
    import UdpTester from "../components/UdpTester.svelte";
    import { raw_data as raw_data_store } from "../stores/server_stats";
    import Ik from "../components/Ik.svelte";
    let raw_data : any;
    raw_data_store.subscribe((value) => {
        raw_data = value;
    });
</script>
<p>Raw data: {JSON.stringify(raw_data)}</p>
<Navbar />
<UdpTester />
<Ik />

