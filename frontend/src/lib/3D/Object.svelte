<script lang="ts">
  import { fileUrl } from '$lib/api/files'
  import type { Object3d } from '$lib/api/object3d'
  import { T } from '@threlte/core'
  import { useGltf } from '@threlte/extras'
  import { Box3, Vector3, type Mesh } from 'three'
  import CssObject from './CssObject.svelte'

  type Props = {
    object: Object3d
    floorsBefore?: number
    floorsAfter?: number
  }

  let { object, floorsAfter, floorsBefore }: Props = $props()

  const gltf = $derived(useGltf(fileUrl(object.file_uuid)))

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

  const floorHeight = 25
  const width = 10
  const depth = 14

  let isElevatorSaft = $derived.by(() => {
    return object.name === 'Elevator' && floorsBefore !== undefined && floorsAfter !== undefined
  })

  let saftHeight = $derived.by(() => {
    const floorsLeft = (floorsAfter || 0) + 1
    return floorsLeft * floorHeight
  })
</script>

<T.Group position.x={object.x} position.z={object.z} rotation.y={object.rotation}>
  {#if mesh}
    <T.Mesh geometry={mesh.geometry}>
      <T.MeshStandardMaterial color={'hotpink'} attach="material" />
      <CssObject position.y={height * 1.5}>
        <div class="relative z-10 flex items-center gap-2 rounded-md border border-primary/40 p-2">
          {object.name}
        </div>
      </CssObject>
    </T.Mesh>
  {/if}

  {#if isElevatorSaft}
    <T.Mesh position.y={saftHeight / 2} position.z={-depth / 2} position.x={-width / 2}>
      <T.MeshStandardMaterial color={'hotpink'} attach="material" />
      <T.BoxGeometry args={[width, saftHeight, depth]} />
    </T.Mesh>
  {/if}
</T.Group>
