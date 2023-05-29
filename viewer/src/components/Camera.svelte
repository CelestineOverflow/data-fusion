<script lang="ts">
    import { onMount } from "svelte";
    let image: HTMLImageElement;

    async function getImage() {
        const response = await fetch(
            "http://127.0.0.1:8000/get_image?camera_id=2"
        );
        image.src = URL.createObjectURL(await response.blob());
    }

    onMount(() => {
        getImage();
    });
</script>

<div class="card" style="width: 18rem;">
    <img bind:this={image}  class="card-img-top" alt="..." />
    <div class="card-body">
        <h5 class="card-title">Image from cv2</h5>
        <p class="card-text">
            Http request to get image from cv2
        </p>
        <button on:click={getImage}>Refresh Image</button>
    </div>
</div>
