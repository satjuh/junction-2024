<script lang="ts">
  import Preview from '$lib/3D/Preview.svelte'
  import type { ObjectTemplate } from '$lib/api/objectTemplates'
  import { Canvas } from '@threlte/core'
  import { twMerge } from 'tailwind-merge'

  type Props = {
    object: ObjectTemplate
    onClick?: () => void
    active?: boolean
  }

  let { object, onClick, active }: Props = $props()
</script>

<button
  class={twMerge(
    'flex flex-col items-center overflow-hidden rounded-md bg-accent-900 py-5',
    active && 'bg-secondary-900'
  )}
  onclick={onClick}
>
  <div class="">
    <Canvas>
      <Preview url={object.model} />
    </Canvas>
  </div>

  <h1 class="text-2xl font-bold">{object.name}</h1>
</button>
