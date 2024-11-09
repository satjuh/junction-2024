<script lang="ts">
  import { onMount } from 'svelte'
  import { twMerge } from 'tailwind-merge'

  type Props = {
    label: string
    hovering?: boolean
  }

  let { label, hovering = $bindable() }: Props = $props()

  let baseClasses = 'font-bold text-text bg-black border border-primary p-2 rounded-lg transition-all'

  let hoverClasses = 'bg-primary text-background'

  let classes = $derived(twMerge(baseClasses, hovering ? hoverClasses : ''))

  let ref: HTMLElement

  // Compare mouse coordinates to the bounding box of the label
  const mouseInside = (event: MouseEvent) => {
    const { left, top, width, height } = ref.getBoundingClientRect()
    const { clientX, clientY } = event
    return clientX >= left && clientX <= left + width && clientY >= top && clientY <= top + height
  }

  const handleMouseMove = (event: MouseEvent) => {
    hovering = mouseInside(event)
  }

  onMount(() => {
    document.addEventListener('mousemove', handleMouseMove)

    return () => {
      document.removeEventListener('mousemove', handleMouseMove)
    }
  })
</script>

<div class={classes} bind:this={ref}>
  {label}
</div>
