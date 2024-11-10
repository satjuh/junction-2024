<script lang="ts">
  import { fileUrl } from '$lib/api/files'
  import type { Floor as IFloor } from '$lib/api/floors'
  import { T, useTask, useThrelte } from '@threlte/core'
  import { interactivity, OrbitControls } from '@threlte/extras'
  import { Box3, Group, Object3D, PerspectiveCamera, Vector3 } from 'three'
  import { CSS2DRenderer } from 'three/examples/jsm/Addons.js'
  import Floor from './Floor.svelte'

  type Props = {
    floors: (IFloor & { hovering?: boolean })[]
    somethingElseHovering?: boolean
  }

  let { floors, somethingElseHovering }: Props = $props()

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

  function fitObjectToCamera(obj: Group): void {
    const box = new Box3().setFromObject(obj)
    const size = new Vector3()
    box.getSize(size)

    const center = new Vector3()
    box.getCenter(center)

    // Calculate the required distance based on the field of view
    const maxSize = Math.max(size.x, size.y, size.z)
    const fov = (perspectiveCamera.fov * Math.PI) / 180 // Convert FOV to radians
    let distance = maxSize / (2 * Math.tan(fov / 2))

    // Offset the distance a bit for padding
    distance *= 1.1

    // Adjust the camera position for a 30-degree angle
    const angle = Math.PI / 6 // 30 degrees in radians
    const offsetX = distance * Math.sin(angle)
    const offsetY = distance * Math.sin(angle / 2) // Slight vertical offset
    const offsetZ = distance * Math.cos(angle)

    perspectiveCamera.position.set(center.x + offsetX, center.y + offsetY, center.z + offsetZ)
    perspectiveCamera.lookAt(center)

    // Update the perspectiveCamera projection matrix
    perspectiveCamera.updateProjectionMatrix()
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

  // svelte-ignore non_reactive_update
  let mainGroup: Group
  // svelte-ignore non_reactive_update
  let perspectiveCamera: PerspectiveCamera

  $effect(() => {
    console.log(floors)
  })
</script>

<T.PerspectiveCamera
  makeDefault
  position={[500, 300, 500]}
  oncreate={(ref) => {
    ref.lookAt(0, 1, 0)
  }}
  bind:ref={perspectiveCamera}
>
  <OrbitControls enableDamping />
</T.PerspectiveCamera>

<T.Group>
  <T.Group bind:ref={mainGroup}>
    {#each floors as floor, i (i)}
      {@const floorsBefore = floors.slice(0, i)}
      {@const baseY = floorsBefore.reduce((acc, f) => acc + f.height, 0)}
      {@const lastFloor = i === floors.length - 1}
      {@const gltfUrl = !lastFloor && floor.floor_3D_walls ? fileUrl(floor.floor_3D_walls) : fileUrl(floor.floor_3D)} }

      <Floor
        {baseY}
        {gltfUrl}
        onClick={() => {}}
        onLoad={i === 0
          ? () => {
              initialCenter(mainGroup)
              fitObjectToCamera(mainGroup)
            }
          : () => {}}
        label={floor.name}
        {somethingElseHovering}
        hovering={floor.hovering}
        objects={floor.objects}
        floorsBefore={floorsBefore.length}
        floorsAfter={floors.slice(i + 1).length}
      />
    {/each}
  </T.Group>

  <T.Mesh rotation.x={-Math.PI / 2} receiveShadow>
    <T.CircleGeometry args={[800, 40]} />
    <T.MeshStandardMaterial color={0xd0ca92} opacity={0.5} transparent />
  </T.Mesh>
</T.Group>
