<script lang="ts">
  import type { Object3d } from '$lib/api/object3d'
  import { T } from '@threlte/core'
  import { useGltf } from '@threlte/extras'
  import { tweened } from 'svelte/motion'
  import { BufferGeometry, Mesh, WireframeGeometry } from 'three'
  import { degToRad } from 'three/src/math/MathUtils.js'
  import CssObject from '../CssObject.svelte'
  import Label from '../Label.svelte'
  import Object from '../Object.svelte'

  type Props = {
    gltfUrl: string
    baseY: number
    onLoad?: (object: Mesh) => void
    label?: string
    objects?: Object3d[]
  }

  let { gltfUrl, baseY, label, onLoad, objects }: Props = $props()

  const gltf = useGltf(gltfUrl)
  let geometry = $derived($gltf?.nodes['geometry_0'].geometry || null) as BufferGeometry

  const opacity = tweened(0.5, { duration: 200 })

  let onLoadSent = $state(false)

  // svelte-ignore non_reactive_update
  let mesh: Mesh

  $effect(() => {
    if (geometry && !onLoadSent && onLoad) {
      onLoad(mesh)
      onLoadSent = true
    }
  })
</script>

<T.Group position.y={baseY}>
  {#if geometry}
    <T.Mesh {geometry} rotation.x={degToRad(-90)} bind:ref={mesh}>
      <T.MeshStandardMaterial color={0x4080ff} opacity={$opacity} transparent attach="material" />

      <T.LineSegments args={[new WireframeGeometry(geometry)]}>
        <T.LineBasicMaterial color={'salmon'} attach="material" transparent opacity={$opacity} linewidth={0.1} />
      </T.LineSegments>

      {#if label}
        <CssObject position.x={300}>
          <Label {label} />
        </CssObject>
      {/if}
    </T.Mesh>
  {/if}

  {#if objects}
    {#each objects as object}
      <Object {object} />
    {/each}
  {/if}
</T.Group>
