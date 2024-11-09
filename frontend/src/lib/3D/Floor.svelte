<script lang="ts">
  import { T } from '@threlte/core'
  import { interactivity, OrbitControls, useGltf } from '@threlte/extras'
  import { tweened } from 'svelte/motion'
  import { Box3, Object3D, Vector3, WireframeGeometry } from 'three'
  import CssObject from './CssObject.svelte'
  import Label from './Label.svelte'
  import { cachedUrl } from './cachedUrl'
  import { readable } from 'svelte/store'
  import { degToRad } from 'three/src/math/MathUtils.js'

  type Props = {
    gltfUrl: string
    baseY: number
    onClick?: (event: MouseEvent) => void
    onLoad?: (object: Object3D) => void
    label?: string
    hovering?: boolean
    somethingElseHovering?: boolean
    onHoverStart?: () => void
    onHoverEnd?: () => void
  }

  let {
    gltfUrl,
    baseY,
    onClick,
    label,
    onLoad,
    hovering = $bindable(),
    somethingElseHovering = false,
    onHoverStart = () => {},
    onHoverEnd = () => {}
  }: Props = $props()

  const url = cachedUrl(gltfUrl)

  const gltf = $derived($url ? useGltf($url) : readable(undefined))
  let geometry = $derived($gltf?.nodes['geometry_0'].geometry || null)

  const opacity = tweened(0.5, { duration: 200 })

  let onLoadSent = $state(false)

  let previousHovering = $state(false)

  $effect(() => {
    if (geometry && !onLoadSent && onLoad) {
      onLoad(geometry)
      onLoadSent = true
    }

    if (hovering) {
      opacity.set(1)
    } else if (somethingElseHovering) {
      opacity.set(0.05)
    } else {
      opacity.set(0.5)
    }

    if (hovering && !previousHovering) {
      onHoverStart()
    } else if (!hovering && previousHovering) {
      onHoverEnd()
    }
    previousHovering = hovering || false
  })
</script>

<T.Group position.y={baseY}>
  {#if geometry}
    <T.Mesh {geometry} rotation.x={degToRad(90)}>
      <T.MeshStandardMaterial color={0x4080ff} opacity={$opacity} transparent attach="material" />

      <T.LineSegments args={[new WireframeGeometry(geometry)]}>
        <T.LineBasicMaterial color={'salmon'} attach="material" transparent opacity={$opacity} linewidth={0.1} />
      </T.LineSegments>

      <CssObject>
        <Label label={label || ''} bind:hovering />
      </CssObject>
    </T.Mesh>
  {/if}
</T.Group>
