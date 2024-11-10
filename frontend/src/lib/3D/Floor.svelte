<script lang="ts">
  import type { Object3d } from '$lib/api/object3d'
  import { T } from '@threlte/core'
  import { useGltf } from '@threlte/extras'
  import { tweened } from 'svelte/motion'
  import { readable } from 'svelte/store'
  import { Mesh, WireframeGeometry } from 'three'
  import { degToRad } from 'three/src/math/MathUtils.js'
  import { cachedUrl } from './cachedUrl'
  import CssObject from './CssObject.svelte'
  import Label from './Label.svelte'
  import Object from './Object.svelte'

  type Props = {
    gltfUrl: string
    baseY: number
    onClick?: (event: MouseEvent) => void
    onLoad?: (object: Mesh) => void
    label?: string
    hovering?: boolean
    somethingElseHovering?: boolean
    objects?: Object3d[]
    floorsBefore?: number
    floorsAfter?: number
  }

  let {
    gltfUrl,
    baseY,
    label,
    onLoad,
    hovering,
    somethingElseHovering = false,
    objects,
    floorsAfter,
    floorsBefore
  }: Props = $props()

  const url = $derived(cachedUrl(gltfUrl))

  const gltf = $derived($url ? useGltf($url) : readable(undefined))
  let geometry = $derived($gltf?.nodes['geometry_0'].geometry || null)

  const opacity = tweened(0.5, { duration: 200 })

  let onLoadSent = $state(false)

  $effect(() => {
    if (geometry && !onLoadSent && onLoad) {
      onLoad(mesh)
      onLoadSent = true
    }

    if (hovering) {
      opacity.set(1)
    } else if (somethingElseHovering) {
      opacity.set(0.05)
    } else {
      opacity.set(0.5)
    }
  })

  let mesh: Mesh

  $effect(() => {
    console.log({ objects })
  })
</script>

<T.Group position.y={baseY}>
  {#if geometry}
    <T.Mesh bind:ref={mesh} {geometry} rotation.x={degToRad(-90)}>
      <T.MeshStandardMaterial color={0x4080ff} opacity={$opacity} transparent attach="material" />

      <T.LineSegments args={[new WireframeGeometry(geometry)]}>
        <T.LineBasicMaterial color={'salmon'} attach="material" transparent opacity={$opacity} linewidth={0.1} />
      </T.LineSegments>

      {#if label}
        <CssObject position.x={300}>
          <Label {label} {hovering} />
        </CssObject>
      {/if}
    </T.Mesh>
  {/if}

  {#if objects?.length}
    {#each objects as object}
      <Object {object} {floorsBefore} {floorsAfter} />
    {/each}
  {/if}
</T.Group>
