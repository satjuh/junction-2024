<script lang="ts">
  import { goto } from '$app/navigation'
  import ViewScene from '$lib/3D/ViewScene.svelte'
  import { Canvas } from '@threlte/core'
  import { Sky } from '@threlte/extras'
  let { data } = $props()

  let house = $derived(data.house)
  let floors = $derived(house.floors)

  $effect(() => {
    console.log(house)
    if (!floors.length) {
      goto(`/${house.uuid}/edit`)
    }
  })
</script>

<div id="css-renderer-target"></div>

<main class="relative flex h-svh">
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
    <ViewScene />
  </Canvas>
</main>
<div id="layout" class="absolute right-0 top-0 h-full w-[25vw] min-w-72 flex-col bg-black">
  {#each floors as floor, i}
    <div class="flex items-center justify-between p-2">
      <span class="text-white">
        Floor {i + 1}
      </span>
      <button class="text-white" onclick={() => goto(`/${house.uuid}/${floor.uuid}`)}> Edit </button>
    </div>
  {/each}
</div>

<style>
  #css-renderer-target {
    left: 0;
    position: absolute;
    pointer-events: none;
    top: 0;
  }
</style>
