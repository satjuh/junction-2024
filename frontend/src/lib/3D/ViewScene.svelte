<script lang="ts">
  import { fileUrl } from '$lib/api/files'
  import type { Floor as IFloor } from '$lib/api/floors'
  import { T, useTask, useThrelte } from '@threlte/core'
  import { interactivity, OrbitControls } from '@threlte/extras'
  import { Box3, Group, Object3D, Vector3 } from 'three'
  import { CSS2DRenderer } from 'three/examples/jsm/Addons.js'
  import Floor from './Floor.svelte'

  type Props = {
    floors: IFloor[]
  }

  let { floors }: Props = $props()

  interactivity()

  const initialCenter = (ref: Object3D) => {
    // Calculate the bounding box of the model
    const bbox = new Box3().setFromObject(ref, false)
    const size = new Vector3()
    const center = new Vector3()
    bbox.getSize(size)
    bbox.getCenter(center)

    // Center the model and raise it above the floor
    ref.position.set(
      -center.x,
      -center.y + size.y / 2, // Raises the model so its bottom sits on the ground
      -center.z
    )
  }

  const { scene, size, autoRenderTask, camera } = useThrelte()

  // Set up the CSS2DRenderer to run in a div placed atop the <Canvas>
  const element = document.querySelector('#css-renderer-target') as HTMLElement
  const cssRenderer = new CSS2DRenderer({ element })
  $effect(() => cssRenderer.setSize($size.width, $size.height))

  scene.matrixWorldAutoUpdate = false
  useTask(
    () => {
      scene.updateMatrixWorld()
    },
    { before: autoRenderTask }
  )

  useTask(
    () => {
      cssRenderer.render(scene, camera.current)
    },
    {
      after: autoRenderTask,
      autoInvalidate: false
    }
  )

  let hoveringFloor = $state<null | number>(null)

  // svelte-ignore non_reactive_update
  let mainGroup: Group
</script>

<T.PerspectiveCamera
  makeDefault
  position={[500, 500, 500]}
  oncreate={(ref) => {
    ref.lookAt(0, 1, 0)
  }}
>
  <OrbitControls enableDamping />
</T.PerspectiveCamera>

<T.Group bind:ref={mainGroup}>
  {#each floors as floor, i (i)}
    {@const floorsBefore = floors.slice(0, i)}
    {@const baseY = floorsBefore.reduce((acc, f) => acc + f.height, 0)}
    {@const gltfUrl = fileUrl(floor.floor_3D)}

    <Floor
      {baseY}
      {gltfUrl}
      onClick={() => {}}
      onLoad={() => (i === 0 ? initialCenter(mainGroup) : {})}
      label={`Floor ${i}`}
      somethingElseHovering={hoveringFloor !== null && hoveringFloor !== i}
      onHoverStart={() => {
        hoveringFloor = i
      }}
      onHoverEnd={() => {
        if (hoveringFloor === i) {
          hoveringFloor = null
        }
      }}
    />
  {/each}
</T.Group>

<T.Mesh rotation.x={-Math.PI / 2} receiveShadow>
  <T.CircleGeometry args={[800, 40]} />
  <T.MeshStandardMaterial color={0xd0ca92} opacity={0.5} transparent />
</T.Mesh>
