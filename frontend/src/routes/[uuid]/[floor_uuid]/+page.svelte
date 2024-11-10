<script lang="ts">
  import EditScene from '$lib/3D/edit/EditScene.svelte'
  import type { ObjectTemplate as IObjectTemplate } from '$lib/api/objectTemplates'
  import Button from '$lib/components/basics/Button.svelte'
  import { Canvas } from '@threlte/core'
  import { Sky } from '@threlte/extras'
  import ObjectTemplate from './ObjectTemplate.svelte'
  let { data } = $props()

  let house = $derived(data.house)

  let addingObject = $state<IObjectTemplate | null>(null)
</script>

<div id="css-renderer-target"></div>

<div class="flex h-full w-svw">
  <Button href={`/${house.uuid}`} icon class="absolute left-4 top-4 z-20">
    <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
    </svg>
  </Button>

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
        <EditScene floor={data.floor} addingObject={addingObject || undefined} />
      {/if}
    </Canvas>
  </main>
  <div id="layout" class="flex h-full min-w-72 flex-1 flex-col-reverse gap-4 overflow-y-auto bg-black px-10 py-10">
    {#each data.objects as obj}
      <ObjectTemplate
        object={obj}
        onClick={() => {
          addingObject = obj
        }}
        active={addingObject?.uuid === obj.uuid}
      />
    {/each}
  </div>
</div>

<style>
  #css-renderer-target {
    left: 0;
    position: absolute;
    top: 0;
  }
</style>
