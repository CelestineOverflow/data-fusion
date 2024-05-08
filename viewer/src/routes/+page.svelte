<script lang="ts">
	import IK_SolverT from './../components/IK_Solver_t.svelte';
	import MergedXR_IK from './../components/MergedXR_IK.svelte';
    import Navbar from "../components/Navbar.svelte";
    import UdpTester from "../components/UdpTester.svelte";
    import {onMount} from "svelte";
    import Ik from "../components/Ik.svelte";
    import {connectToWebSocket } from "../stores/websocket";
    import Camera from "../components/Camera.svelte";
    import RawData from "../components/RawData.svelte";
    import Chest from "../components/Chest.svelte";
    import Test from "../components/Test.svelte";
    import Test2 from "../components/Test2.svelte";
    import Scheleton from "../components/Scheleton.svelte";
    import TestXr from "../components/TestXR.svelte";
    import Iktesting from "../components/Iktesting.svelte";
    import IkSolverT from "../components/IK_Solver_t.svelte";
    import Cube from '../components/Cube.svelte';
    let data : any;
    onMount(() => {
        connectToWebSocket();
    });

</script>
<Navbar />
<UdpTester />
  <div class="container">
    <div class="row">
      <!-- <div class="col-sm">
        <Camera />
      </div>

      <div class="col-xxl">
        <Chest />
      </div> -->
      <!-- <div class="col-sm">
        <RawData />
      </div>


      <div class="col-xxl">
        <div class="row">
          <div class="col-xxl">
            <Scheleton />
          </div>
        </div>
        
        <div class="row">
          <div class="col-xxl">
            <Test />
          </div>
        </div>
        

      </div>
      <div class="col-xxl">
        <Test2 />
      </div>
      <div class="col-xxl">
        
      </div> -->
      <!-- <div class="col-xxl">
        <Ik />
      </div> -->
    <!-- <IK_SolverT /> -->
    <!-- <Cube /> -->
    <MergedXR_IK />
    </div>
  </div>
