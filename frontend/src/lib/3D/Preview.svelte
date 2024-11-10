<script lang="ts">
  import { T, useTask } from '@threlte/core'
  import { GLTF, interactivity, OrbitControls } from '@threlte/extras'
  import { type Group, type PerspectiveCamera } from 'three'

  type Props = {
    url: string
  }

  let { url }: Props = $props()

  interactivity()

  let rotation = $state(0)

  useTask((delta) => {
    rotation += delta * 0.2
  })

  let mainGroup: Group
  let camera: PerspectiveCamera
</script>

<T.PerspectiveCamera
  makeDefault
  position={[50, 50, 50]}
  bind:ref={camera}
  oncreate={(ref) => {
    ref.lookAt(0, 0, 0)
  }}
>
  <OrbitControls />
</T.PerspectiveCamera>

<!-- Lighting setup -->
<T.AmbientLight intensity={0.5} />
<T.PointLight position={[30, 30, 30]} intensity={100} />

<T.Group rotation.y={rotation} bind:ref={mainGroup}>
  <GLTF {url}></GLTF>
</T.Group>
