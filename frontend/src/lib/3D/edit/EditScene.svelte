<script lang="ts">
  import { fileUrl } from '$lib/api/files'
  import type { Floor as IFloor } from '$lib/api/floors'
  import { T, useTask, useThrelte } from '@threlte/core'
  import { interactivity, OrbitControls } from '@threlte/extras'
  import { Box3, Group, Mesh, Object3D, PerspectiveCamera, Vector3 } from 'three'
  import { CSS2DRenderer } from 'three/examples/jsm/Addons.js'
  import Floor from '../Floor.svelte'

  type Props = {
    floor: IFloor
  }

  let { floor }: Props = $props()

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

  const { scene, size, autoRenderTask, camera: defaultCamera } = useThrelte()

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
      cssRenderer.render(scene, defaultCamera.current)
    },
    {
      after: autoRenderTask,
      autoInvalidate: false
    }
  )

  function fitObjectToCamera(obj: Mesh): void {
    const box = new Box3().setFromObject(obj)
    const size = new Vector3()
    box.getSize(size)

    const center = new Vector3()
    box.getCenter(center)

    // Calculate the required distance based on the field of view
    const maxSize = Math.max(size.x, size.y, size.z)
    const fov = (camera.fov * Math.PI) / 180 // Convert FOV to radians
    let distance = maxSize / (2 * Math.tan(fov / 2))

    // Offset the distance a bit for padding
    distance *= 1.2

    // Update the camera position and orientation
    camera.position.set(center.x, center.y, center.z + distance)
    camera.lookAt(center)

    // Update the camera projection matrix
    camera.updateProjectionMatrix()
  }

  let hoveringFloor = $state<null | number>(null)

  // svelte-ignore non_reactive_update
  let mainGroup: Group
  // svelte-ignore non_reactive_update
  let camera: PerspectiveCamera
</script>

<T.PerspectiveCamera
  makeDefault
  position={[0, 300, 0]}
  oncreate={(ref) => {
    ref.lookAt(0, 0, 0)
  }}
  bind:ref={camera}
>
  <OrbitControls enableDamping />
</T.PerspectiveCamera>

<T.Group>
  <T.Group bind:ref={mainGroup}>
    <Floor
      baseY={floor.height}
      gltfUrl={fileUrl(floor.floor_3D)}
      onLoad={(obj) => {
        initialCenter(mainGroup)
        fitObjectToCamera(obj as Mesh)
      }}
    />
  </T.Group>

  <T.Mesh rotation.x={-Math.PI / 2} receiveShadow>
    <T.CircleGeometry args={[800, 40]} />
    <T.MeshStandardMaterial color={0xd0ca92} opacity={0.5} transparent />
  </T.Mesh>
</T.Group>
