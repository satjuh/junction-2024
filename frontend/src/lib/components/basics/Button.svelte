<script lang="ts">
  import type { HTMLAnchorAttributes, HTMLButtonAttributes } from 'svelte/elements'
  import { twMerge } from 'tailwind-merge'

  type Colors = 'primary' | 'secondary' | 'accent'
  type BaseProps = {
    color?: Colors
    disabled?: boolean
  }

  type ButtonProps = BaseProps & HTMLButtonAttributes
  type LinkProps = BaseProps & { href: string } & HTMLAnchorAttributes

  type Props = ButtonProps | LinkProps

  function isLinkProps(props: Props): props is LinkProps {
    return 'href' in props
  }

  function isButtonProps(props: Props): props is ButtonProps {
    return !('href' in props)
  }

  let { children, class: className, color = 'primary', disabled, ...other }: Props = $props()

  const baseClasses = 'px-4 py-2 bg-primary text-background rounded-full font-body font-extrabold'

  const colorClasses = {
    primary: 'bg-primary text-background',
    secondary: 'bg-secondary text-background',
    accent: 'bg-accent text-background'
  }

  const classes = $derived(
    twMerge(baseClasses, color ? colorClasses[color] : null, className, disabled && 'opacity-20')
  )
</script>

{#if isLinkProps(other)}
  <a
    {...other}
    rel="external"
    href={disabled ? undefined : other.href}
    class={classes}
    tabindex={disabled ? -1 : undefined}
  >
    {#if children}
      {@render children()}
    {/if}
  </a>
{:else if isButtonProps(other)}
  <button {...other} class={classes} {disabled}>
    {#if children}
      {@render children()}
    {/if}
  </button>
{/if}
