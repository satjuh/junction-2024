<script lang="ts">
  import { goto } from '$app/navigation'
  import ViewScene from '$lib/3D/ViewScene.svelte'
  import Button from '$lib/components/basics/Button.svelte'
  import { Canvas } from '@threlte/core'
  import { Sky } from '@threlte/extras'
  let { data } = $props()

  let house = $derived(data.house)
  let floors = $derived(house.floors)

  $effect(() => {
    if (!floors.length) {
      goto(`/${house.uuid}/edit`)
    }
  })

  let hoveringFloor = $state<null | number>(null)

  let sceneFloors = $derived(floors.map((f, i) => ({ ...f, hovering: i === hoveringFloor })))
</script>

<div id="css-renderer-target"></div>

<div class="flex h-full w-svw">
  <main class="relative flex h-svh flex-[3]">
    <Canvas>
      <Sky
        turbidity={20}
        rayleigh={0.57}
        azimuth={180}
        elevation={-5}
        mieCoefficient={0.038}
        mieDirectionalG={0}
        exposure={0.26}
      />
      <ViewScene floors={sceneFloors} somethingElseHovering={hoveringFloor !== null} />
    </Canvas>
  </main>
  <div id="layout" class="flex h-full min-w-72 flex-1 flex-col-reverse bg-black">
    {#each floors as floor, i}
      <!-- svelte-ignore a11y_no_static_element_interactions -->
      <!-- svelte-ignore event_directive_deprecated -->
      <div
        class="flex items-center justify-between p-4"
        class:bg-accent={hoveringFloor === i}
        on:mouseenter={() => (hoveringFloor = i)}
        on:mouseleave={() => (hoveringFloor = null)}
      >
        <h3 class="text-text">
          Floor {i + 1}
        </h3>
        <!-- <button class="text-text" onclick={() => goto(`/${house.uuid}/${floor.uuid}`)}> Add features </button> -->
        <Button icon color={hoveringFloor === i ? 'primary' : 'accent'} href={`/${house.uuid}/${floor.uuid}`}>
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </Button>
      </div>
    {/each}
  </div>
</div>

<style>
  #css-renderer-target {
    left: 0;
    position: absolute;
    pointer-events: none;
    top: 0;
  }
</style>
