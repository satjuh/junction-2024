<script lang="ts">
  import { twMerge } from 'tailwind-merge'

  type Props = {
    label: string
    hovering?: boolean
  }

  let { label, hovering }: Props = $props()

  let baseClasses = 'font-bold text-text bg-black px-2 py-1 rounded-lg transition-all'

  let hoverClasses = 'bg-primary text-background'

  let classes = $derived(twMerge(baseClasses, hovering ? hoverClasses : ''))
</script>

<div class={classes}>
  {label}
</div>
