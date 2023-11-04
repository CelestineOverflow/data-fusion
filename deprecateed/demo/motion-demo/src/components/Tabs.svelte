<script lang="ts">
    export let activeTabValue = 1;
    import Cube from "./Cube.svelte";
    import {
        Collapse,
        Navbar,
        NavbarToggler,
        NavbarBrand,
        Nav,
        NavItem,
        NavLink,
        Dropdown,
        DropdownToggle,
        DropdownMenu,
        DropdownItem,
        Container,
    } from "sveltestrap";
    import { Icon } from "sveltestrap";
    import Welcome from "./Welcome.svelte";
    import About from "./About.svelte";
    import SerialDemo from "./SerialDemo.svelte";
    import BlenderGlTf from "./Blender_glTF.svelte";
    import IKdemo from "./IKdemo.svelte";
    import IKloaded from "./IKloaded.svelte";
    let items = [
        { label: "Welcome", value: 1, component: Welcome, icon: "globe2" },
        { label: "Serial Demo", value: 2, component: SerialDemo, icon: "wrench" },
        { label: "Cube Demo", value: 3, component: Cube, icon: "wrench" },
        { label: "About this", value: 4, component: About, icon: "file-text" },
        { label: "Blender Import Demo", value: 5, component: BlenderGlTf, icon: "file-text" },
        { label: "IK Demo", value: 6, component: IKdemo, icon: "file-text" },
        { label: "IK loaded", value: 7, component: IKloaded, icon: "file-text"}
    ];
</script>

<Navbar color="dark" dark expand="md">
    <Nav class="mx-auto" pills>
        {#each items as item}
            <NavItem>
                <NavLink
                    active={activeTabValue === item.value}
                    on:click={() => (activeTabValue = item.value)}
                    >{item.label} <Icon name={item.icon} />
                </NavLink>
            </NavItem>
        {/each}
    </Nav>
</Navbar>

{#if activeTabValue === 1}
    <Welcome />
{:else if activeTabValue === 2}
    <SerialDemo />
{:else if activeTabValue === 3}
    <Cube />
{:else if activeTabValue === 4}
    <About />
{:else if activeTabValue === 5}
    <BlenderGlTf />
{:else if activeTabValue === 6}
    <IKdemo />
{:else if activeTabValue === 7}
    <IKloaded />
{/if}