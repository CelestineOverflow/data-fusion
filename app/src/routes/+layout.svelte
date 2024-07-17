<script lang="ts">
    import { onMount, onDestroy } from 'svelte';
	import { connectToWebSocket } from '../stores/store';
    import "../app.css";
    onMount(() => {
        connectToWebSocket();
    });
</script>

<nav class="flex justify-center space-x-4">
    <a href="/" class="text-blue-500 hover:text-blue-700">Main 📌</a>
    <a href="/test" class="text-blue-500 hover:text-blue-700">Test 🧪</a>
    <a href="/camera" class="text-blue-500 hover:text-blue-700">Camera 📷</a>
    <a href="/settings" class="text-blue-500 hover:text-blue-700">Settings 🔧</a>
</nav>

<slot></slot>