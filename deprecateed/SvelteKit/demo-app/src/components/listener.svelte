<script lang="ts">
    import {listen } from '@tauri-apps/api/event'
    import { onMount } from 'svelte'
    let textfromRust = "nothing yet"

    listen('rust-event', (payload)=> {
        textfromRust = payload
    })
</script>

<p>{textfromRust}</p>