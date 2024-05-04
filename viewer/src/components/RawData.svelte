<script lang="ts">

        import {limbs_data } from "../stores/body";

        let data : any;

        limbs_data.subscribe((value) => {
                data = JSON.stringify(value, null, 2);
        });
</script>


<div class="card" style="width: 20rem;">
    <div class="card-body">
        <h5 class="card-title">Live Video Feed</h5>
        <pre>{data}</pre>
    </div>
</div>
