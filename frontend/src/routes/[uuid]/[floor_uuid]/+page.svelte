<script lang="ts">
  import EditScene from '$lib/3D/edit/EditScene.svelte'
  import { Canvas } from '@threlte/core'
  import { Sky } from '@threlte/extras'
  let { data } = $props()

  let house = $derived(data.house)
</script>

<div id="css-renderer-target"></div>

<div class="flex h-full w-svw">
  <main class="relative flex h-svh flex-[3]">
    <Canvas>
      <Sky
        turbidity={0.65}
        rayleigh={0.17}
        azimuth={180}
        elevation={85}
        mieCoefficient={0.013}
        mieDirectionalG={0.7}
        exposure={1}
      />
      {#if data.floor}
        <EditScene floor={data.floor} />
      {/if}
    </Canvas>
  </main>
  <div id="layout" class="flex h-full min-w-72 flex-1 flex-col-reverse bg-black"></div>
</div>

<style>
  #css-renderer-target {
    left: 0;
    position: absolute;
    pointer-events: none;
    top: 0;
  }
</style>
