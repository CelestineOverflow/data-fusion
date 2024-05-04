<script lang="ts">
    import { limbs_data, resetLocalStorage } from "../stores/body";
    let limbs = [];
    limbs_data.subscribe((value) => {
        limbs = value;
    });
    let selectedLimb = limbs[0]; // Default to the first limb
    let addFactor = 1;
    if (limbs.length < 0) {
        resetLocalStorage();
        console.log("resetting local storage");
    }
</script>

<button
    class="btn btn-primary"
    on:click={() => {
        resetLocalStorage();
    }}
    >Nuke Local Storage
</button>

<div class="mt-3">
    <label for="limbSelector">Select Limb</label>
    <select id="limbSelector" bind:value={selectedLimb}>
        {#each limbs as limb}
            <option value={limb}>{limb.name}</option>
        {/each}
    </select>
</div>

<div class="mt-3">
    <h6>Adding Factor {addFactor}</h6>
    <div class="form-group">
        <button
            class="btn btn-primary"
            on:click={() => {
                addFactor *= 2;
            }}
            >x2
        </button>
        <button
            class="btn btn-primary"
            on:click={() => {
                addFactor /= 2;
            }}
            >/2
        </button>
    </div>
</div>

<div class="mt-3">
    <h6>{selectedLimb.name} Rotation</h6>
    <div class="form-group">
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.send = !selectedLimb.send;
            }}
            >{selectedLimb.send ? "Stop Sending" : "Start Sending"}
        </button>
    </div>
    <div class="form-group">
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationX = 0;
                selectedLimb.rotationY = 0;
                selectedLimb.rotationZ = 0;
            }}
            >Reset Rotation
        </button>
    </div>
    <div class="form-group">
        
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationX += addFactor;
            }}
            >+
        </button>
        
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationX -= addFactor;
            }}>-</button
        >
        <label>X-axis rotation {selectedLimb.rotationX}</label>
    </div>
    <div class="form-group">
        
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationY += addFactor;
            }}
            >+
        </button>
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationY -= addFactor;
            }}>-</button
        >
        <label>Y-axis rotation {selectedLimb.rotationY}</label>
    </div>
    <div class="form-group">
        
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationZ += addFactor;
            }}
            >+
        </button>
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.rotationZ -= addFactor;
            }}>-</button
        >
        <label>Z-axis rotation {selectedLimb.rotationZ}</label>
    </div>
</div>
<div class="mt-3">
    <h6>{selectedLimb.name} Position</h6>
    <div class="form-group">
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionX = 0;
                selectedLimb.positionY = 0;
                selectedLimb.positionZ = 0;
            }}
            >Reset Position
        </button>
    </div>
    <div
        class="form-group
            "
    >
        
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionX += addFactor;
            }}
            >+
        </button>
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionX -= addFactor;
            }}>-</button
        >
        <label>X-axis position {selectedLimb.positionX}</label>
    </div>
    <div class="form-group">
        
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionY += addFactor;
            }}
            >+
        </button>
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionY -= addFactor;
            }}>-</button
        >
        <label>Y-axis position {selectedLimb.positionY}</label>
    </div>
    <div class="form-group">
       
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionZ += addFactor;
            }}
            >+
        </button>
        <button
            class="btn btn-primary"
            on:click={() => {
                selectedLimb.positionZ -= addFactor;
            }}>-</button
        >
        <label>Z-axis position {selectedLimb.positionZ}</label>
    </div>
</div>
