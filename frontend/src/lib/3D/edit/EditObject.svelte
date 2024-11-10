<script lang="ts">
  import type { ObjectTemplate } from '$lib/api/objectTemplates'
  import Button from '$lib/components/basics/Button.svelte'
  import { T } from '@threlte/core'
  import { TransformControls, useGltf } from '@threlte/extras'
  import { Box3, Vector3, type Mesh } from 'three'
  import { degToRad } from 'three/src/math/MathUtils.js'
  import CssObject from '../CssObject.svelte'

  type Props = {
    object: ObjectTemplate
    onSave: (position: Vector3, rotation: number) => void
    onCancel: () => void
  }

  let { object, onSave, onCancel }: Props = $props()

  const gltf = $derived(useGltf(object.model))
  let mesh = $derived.by(() => {
    console.log('gltf', gltf)
    if (!$gltf) return null

    const scene = $gltf.scene

    // Find the first mesh in scene
    for (let i = 0; i < scene.children.length; i++) {
      const child = scene.children[i]
      if (child.type === 'Mesh') {
        return child as Mesh
      }
    }
  })

  let height = $derived.by(() => {
    if (!mesh) return 0
    const bbox = new Box3().setFromObject(mesh, false)
    return bbox.getSize(new Vector3()).y
  })

  let state = $state<'translate' | 'rotate'>('translate')

  const swap = () => {
    state = state === 'translate' ? 'rotate' : 'translate'
  }

  //   $effect(() => {
  //     console.log($gltf)
  //   })

  // svelte-ignore non_reactive_update
  let localMesh: Mesh

  const handleSave = () => {
    if (!localMesh) return
    onSave(localMesh.position, localMesh.rotation.y)
  }
</script>

<T.Group>
  {#if mesh}
    <T.Mesh geometry={mesh.geometry} bind:ref={localMesh}>
      {#snippet children({ ref })}
        <TransformControls
          object={ref}
          translationSnap={10}
          rotationSnap={degToRad(10)}
          showY={state === 'rotate'}
          showZ={state === 'translate'}
          showX={state === 'translate'}
          mode={state}
        />
        <T.MeshStandardMaterial color={'hotpink'} attach="material" />
        <CssObject position.y={height * 1.5}>
          <div class="relative z-10 flex items-center gap-2">
            <Button onclick={onCancel} icon class="bg-transparent text-background">
              <!-- svg for cancel -->
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 512 512">
                <path
                  fill="currentColor"
                  fill-rule="evenodd"
                  d="M420.48 121.813L390.187 91.52L256 225.92L121.813 91.52L91.52 121.813L225.92 256L91.52 390.187l30.293 30.293L256 286.08l134.187 134.4l30.293-30.293L286.08 256z"
                />
              </svg>
            </Button>

            <Button onclick={swap} icon color="accent">
              {#if state === 'translate'}
                <!-- svg for rotate -->
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
                  <path
                    fill="currentColor"
                    d="M12 6C6.3 6 2 8.15 2 11c0 2.45 3.19 4.38 7.71 4.88l-.42.41a1 1 0 0 0 0 1.42a1 1 0 0 0 1.42 0l2-2a1 1 0 0 0 .21-.33a1 1 0 0 0 0-.76a1 1 0 0 0-.21-.33l-2-2a1 1 0 0 0-1.42 1.42l.12.11C6 13.34 4 12 4 11c0-1.22 3.12-3 8-3s8 1.78 8 3c0 .83-1.45 2-4.21 2.6a1 1 0 0 0-.79 1.19a1 1 0 0 0 1.19.77c3.65-.8 5.81-2.5 5.81-4.56c0-2.85-4.3-5-10-5"
                  />
                </svg>
              {:else}
                <!-- svg for translate -->
                <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 24 24">
                  <path
                    fill="none"
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="1.5"
                    d="M12 3v6m-9 3h6m12 0h-6m-3 9v-6.5M9 6l1.705-1.952C11.315 3.35 11.621 3 12 3c.38 0 .684.35 1.295 1.048L15 6m0 12l-1.705 1.952C12.685 20.65 12.379 21 12 21c-.38 0-.684-.35-1.295-1.048L9 18m9-9l1.952 1.705C20.65 11.315 21 11.621 21 12c0 .38-.35.684-1.048 1.295L18 15M6 15l-1.952-1.705C3.35 12.685 3 12.379 3 12c0-.38.35-.684 1.048-1.295L6 9"
                    color="currentColor"
                  />
                </svg>
              {/if}
            </Button>
            <Button
              onclick={() => {
                handleSave()
              }}
              icon
            >
              <!-- svg for save -->
              <svg xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 20 20">
                <path fill="currentColor" d="m15.3 5.3l-6.8 6.8l-2.8-2.8l-1.4 1.4l4.2 4.2l8.2-8.2z" />
              </svg>
            </Button>
          </div>
        </CssObject>
      {/snippet}
    </T.Mesh>
  {/if}
</T.Group>
