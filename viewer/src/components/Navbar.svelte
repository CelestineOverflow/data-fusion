<script lang="ts">
    import { state } from '../stores/websocket';
    let server_state : string = '🚩';
    state.subscribe((value) => {
        server_state = value;
    });
</script>

<nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
    <div class="container-fluid">
        <!-- <img src="banner.png" alt="logo" style="width: 30px; height: 30px;" /> -->
        <a class="navbar-brand" href="www.google.com">🥽 Motion Fusion <span class="badge bg-success">Alpha!</span></a>
        <button
            class="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNavDropdown"
            aria-controls="navbarNavDropdown"
            aria-expanded="false"
            aria-label="Toggle navigation"
        >
            <span class="navbar-toggler-icon" />
        </button>
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="www.google.com"
                        >T0</a
                    >
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="www.google.com">T1</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="www.google.com">T2</a>
                </li>
            </ul>
        </div>
    </div>
    <div class="d-flex">
        <button class="btn btn-outline-light me-2" type="button">
            <span class="material-icons">settings</span>
        </button>
        <button class="btn btn-outline-light me-2" type="button">
            <span class="material-icons">help</span>
        </button>
        <p class="text-light me-2">Server State: {server_state}</p>
    </div>
</nav>