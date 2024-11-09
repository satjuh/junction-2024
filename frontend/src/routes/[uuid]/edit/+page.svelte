<script lang="ts">
  import { goto } from '$app/navigation'
  import { fileUrl, uploadPng } from '$lib/api/files.js'
  import { createFloor, updateFloor, type Floor } from '$lib/api/floors.js'
  import Button from '$lib/components/basics/Button.svelte'
  import { flip } from 'svelte/animate'
  import type { ChangeEventHandler } from 'svelte/elements'

  let { data } = $props()

  type ServerFloor = Floor
  type LocalFloor = { file: Blob }
  type WorkingFloor = (ServerFloor | LocalFloor) & { url?: string }

  const isServerFloor = (floor: WorkingFloor): floor is ServerFloor => 'uuid' in floor
  const isLocalFloor = (floor: WorkingFloor): floor is LocalFloor => 'file' in floor

  let floors = $state<WorkingFloor[]>(data?.house?.floors.map((f) => ({ ...f, url: f.floor_png })) || [])

  const addFloor = (floorPlan: Blob) => {
    floors.push({ url: URL.createObjectURL(floorPlan), file: floorPlan })
  }

  const addFloorInputFile: ChangeEventHandler<HTMLInputElement> = (e) => {
    const target = e.target as HTMLInputElement

    const files = target.files
    if (files) {
      // Add floor for each file
      for (let i = 0; i < files.length; i++) {
        addFloor(files[i])
      }
    }

    // reset the input value
    target.value = ''
  }

  const swapFloors = (index: number, newIndex: number) => {
    const temp = floors[index]
    floors[index] = floors[newIndex]
    floors[newIndex] = temp
  }

  let loading = $state(0)

  const startUpload = async () => {
    loading = 1

    for (let i = 0; i < floors.length; i++) {
      const floor = floors[i]

      try {
        if (isServerFloor(floor)) {
          const newFloor = await updateFloor(floor.uuid, {
            ...floor,
            index: i,
            name: `Floor ${i + 1}`
          })
        } else {
          const files = await uploadPng(floor.file)

          const newFloor = {
            house_id: data.house.uuid,
            index: i,
            ...files,
            height: 25,
            name: `Floor ${i + 1}`
          }

          console.log(newFloor)

          const serverFloor = await createFloor(newFloor)

          console.log(serverFloor)
        }
      } catch (error) {
        console.error(error)
        loading = 0
        return
      }

      loading = ((i + 1) / floors.length) * 100
    }

    loading = 0
    goto(`/${data.house.uuid}`)
  }
</script>

<main class="mx-auto flex max-w-screen-lg flex-col gap-10 px-10 pt-20">
  <h1>FLOOR PLAN EDITOR</h1>

  {#if floors.length > 0}
    <div class="flex justify-center">
      <Button onclick={startUpload}>Save</Button>
    </div>
  {/if}

  {#if loading > 0}
    <div class="flex w-full flex-col items-center gap-4">
      <span class="text-2xl text-text">Uploading...</span>
      <div class="h-4 w-full rounded-full">
        <div class="h-full rounded-full bg-primary" style="width: {loading}%"></div>
      </div>
    </div>
  {:else}
    <label
      class="flex cursor-pointer items-center justify-center rounded-lg border border-dashed border-primary/40 p-4"
    >
      <input type="file" accept="image/*" multiple class="hidden" onchange={addFloorInputFile} />
      <span class="text-4xl text-primary">+</span>
    </label>
  {/if}

  <div class="floorplan-container flex flex-col-reverse gap-4">
    {#each floors as floor, i (floor.url)}
      <div
        class="floorplan-row flex max-h-40 items-center gap-2 overflow-visible hover:z-10"
        animate:flip={{ duration: 300 }}
      >
        <div class="floorplan flex h-full flex-1 items-center justify-center bg-background">
          {#if isLocalFloor(floor)}
            <img src={floor.url} alt="floor plan" class="image h-auto max-h-svh w-full object-cover" />
          {:else}
            <img src={fileUrl(floor.floor_png)} alt="floor plan" class="image h-auto max-h-svh w-full object-cover" />
          {/if}
        </div>
        <div class="relative flex h-full flex-col justify-start gap-3 py-10">
          <!-- move up -->
          <Button
            class="bg-background text-primary"
            onclick={() => swapFloors(i, i + 1)}
            disabled={i === floors.length - 1}
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
              <path d="M2 12 L8 4 L14 12" fill="none" stroke="salmon" stroke-width="1.5" />
            </svg>
          </Button>

          <div class="flex gap-4">
            <span class="text-text">Floor {i + 1}</span>
            <Button class="bg-background text-primary" onclick={() => floors.splice(i, 1)}>
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
                <path d="M2 2 L14 14 M2 14 L14 2" fill="none" stroke="salmon" stroke-width="1.5" />
              </svg>
            </Button>
          </div>

          <!-- move down -->
          <Button class="bg-background text-primary" onclick={() => swapFloors(i, i - 1)} disabled={i === 0}>
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16">
              <path d="M2 4 L8 12 L14 4" fill="none" stroke="salmon" stroke-width="1.5" />
            </svg>
          </Button>
        </div>
      </div>
    {/each}
  </div>
</main>

<style>
  .floorplan-container {
    perspective: 2000px;
    transform-style: preserve-3d;
  }

  .floorplan {
    /* Rotate around the center */
    transform-origin: center;
    transform: rotateX(75deg) rotateZ(9deg);
    transition: transform 0.2s ease-in-out;
  }

  .floorplan:hover {
    transform: rotateX(0deg) rotateZ(0deg);
  }

  .image {
    /* invert the image */
    filter: invert(1);

    /* Remove black background wit blend mode */
    mix-blend-mode: screen;
  }
</style>
