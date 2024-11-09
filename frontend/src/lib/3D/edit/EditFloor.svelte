<script lang="ts">
  import { T } from '@threlte/core'
  import { useGltf } from '@threlte/extras'
  import { tweened } from 'svelte/motion'
  import { Object3D, WireframeGeometry } from 'three'
  import { degToRad } from 'three/src/math/MathUtils.js'
  import CssObject from '../CssObject.svelte'
  import Label from '../Label.svelte'

  type Props = {
    gltfUrl: string
    baseY: number
    onLoad?: (object: Object3D) => void
    label?: string
  }

  let { gltfUrl, baseY, label, onLoad }: Props = $props()

  const gltf = useGltf(gltfUrl)
  let geometry = $derived($gltf?.nodes['geometry_0'].geometry || null)

  const opacity = tweened(0.5, { duration: 200 })

  let onLoadSent = $state(false)

  $effect(() => {
    if (geometry && !onLoadSent && onLoad) {
      onLoad(geometry)
      onLoadSent = true
    }
  })
</script>

<T.Group position.y={baseY}>
  {#if geometry}
    <T.Mesh {geometry} rotation.x={degToRad(90)}>
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
</T.Group>
