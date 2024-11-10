<script lang="ts">
  import { useThrelte } from '@threlte/core'
  import { GLTFExporter } from 'three/examples/jsm/Addons.js'

  type Props = {
    exportGtlf: () => Promise<[Blob, string]>
  }

  let { exportGtlf = $bindable() }: Props = $props()

  const { scene } = useThrelte()

  exportGtlf = async () => {
    const exporter = new GLTFExporter()

    const res = await new Promise<[Blob, string]>((res) => {
      console.log(scene.children)

      exporter.parse(
        scene.children[2],
        function (result) {
          // If the result is a string (for GLTF JSON)
          if (result instanceof ArrayBuffer) {
            const blob = new Blob([result], { type: 'application/octet-stream' })

            console.log('Sccuessfully exported scene')
            res([blob, 'scene.gltf'])
          } else {
            const json = JSON.stringify(result)
            const blob = new Blob([json], { type: 'application/json' })
            res([blob, 'scene.gltf'])
          }
        },
        () => {
          console.error('Failed to export scene')
        },
        { binary: true }
      )
    })

    return res
  }
</script>
