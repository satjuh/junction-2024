<script lang="ts">
  import { fileUrl, upload3DModel } from '$lib/api/files'
  import type { Floor as IFloor } from '$lib/api/floors'
  import { createObject3d } from '$lib/api/object3d'
  import type { ObjectTemplate } from '$lib/api/objectTemplates'
  import { T, useTask, useThrelte } from '@threlte/core'
  import { interactivity, OrbitControls } from '@threlte/extras'
  import { Box3, Group, Mesh, Object3D, PerspectiveCamera, Vector3 } from 'three'
  import { CSS2DRenderer } from 'three/examples/jsm/Addons.js'
  import { degToRad } from 'three/src/math/MathUtils.js'
  import EditFloor from './EditFloor.svelte'
  import EditObject from './EditObject.svelte'

  type Props = {
    floor: IFloor
    addingObject?: ObjectTemplate
  }

  let { floor, addingObject }: Props = $props()

  let localFloor = $state(floor)

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

    // magic number
    distance *= 0.7

    // Adjust the camera position for a 30-degree angle
    const angle = degToRad(80)
    const offsetX = distance * Math.sin(angle)
    const offsetY = distance * Math.sin(angle / 2) // Slight vertical offset
    const offsetZ = distance * Math.cos(angle)

    camera.position.set(center.x + offsetX, center.y + offsetY, center.z + offsetZ)
    camera.lookAt(center)

    // Update the camera projection matrix
    camera.updateProjectionMatrix()
  }

  let hoveringFloor = $state<null | number>(null)

  // svelte-ignore non_reactive_update
  let mainGroup: Group
  // svelte-ignore non_reactive_update
  let camera: PerspectiveCamera

  let location = $state<Vector3>(new Vector3())

  let center = $derived.by(() => {
    if (!mainGroup) return new Vector3()
    const bbox = new Box3().setFromObject(mainGroup)
    const center = new Vector3()
    bbox.getCenter(center).y = 0
    return center
  })

  const handleSave = async (position: Vector3, rotation: number) => {
    if (!addingObject) return

    const url = addingObject.model
    const file = await (await fetch(url)).blob()

    const fileUuid = await upload3DModel(file)

    const res = await createObject3d({
      data: '{}',
      file_uuid: fileUuid,
      floor_id: floor.uuid,
      name: addingObject.name,
      rotation: rotation,
      x: position.x,
      y: position.y,
      z: position.z
    })

    localFloor = {
      ...localFloor,
      objects: [...(localFloor.objects || []), res]
    }
    addingObject = undefined
  }
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
    <EditFloor
      baseY={1}
      gltfUrl={fileUrl(floor.floor_3D_walls || floor.floor_3D)}
      onLoad={(obj) => {
        initialCenter(mainGroup)
        fitObjectToCamera(obj as Mesh)
      }}
      objects={localFloor.objects}
    />

    {#if addingObject}
      <EditObject
        object={addingObject}
        onCancel={() => {
          addingObject = undefined
        }}
        onSave={handleSave}
      />
    {/if}
  </T.Group>

  <T.Mesh rotation.x={-Math.PI / 2} receiveShadow>
    <T.CircleGeometry args={[800, 40]} />
    <T.MeshStandardMaterial color={0xd0ca92} opacity={0.5} transparent />
  </T.Mesh>
</T.Group>
