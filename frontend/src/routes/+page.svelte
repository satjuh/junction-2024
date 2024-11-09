<script lang="ts">
  import { getHouses, type House } from '$lib/api/house'
  import Button from '$lib/components/basics/Button.svelte'

  let houses = $state<House[]>([])

  let loading = $state(false)

  $effect(() => {
    // Load from local storage first
    if (localStorage.getItem('houses')) {
      houses = JSON.parse(localStorage.getItem('houses') || '[]')
    }

    loading = true
    getHouses()
      .then((res) => {
        houses = res
        loading = false

        localStorage.setItem('houses', JSON.stringify(res))
      })
      .catch(() => {
        loading = false
      })
  })
</script>

{#snippet house(h: House)}
  <a
    class="relative flex flex-col rounded-md border border-accent/20 shadow-xl shadow-accent/0 transition-all hover:shadow-accent/40"
    href={`/${h.uuid}`}
  >
    <img src={h.image} alt={h.name} class="h-32 w-full max-w-72 object-cover" />

    <span class="absolute right-2 top-2 rounded-full bg-secondary/80 px-2 py-1 text-xs text-background">
      N° {h.latitude}, E° {h.longitude}
    </span>

    <div class=" flex flex-1 flex-col justify-start gap-1 p-4 transition-all">
      <h2 class="overflow-hidden text-ellipsis whitespace-nowrap leading-tight">{h.name}</h2>
      <p>{h.address}</p>
      <span class="line-clamp-5 text-ellipsis text-sm opacity-75">{h.description}</span>
    </div>
  </a>
{/snippet}

<main class="mx-auto flex max-w-screen-xl flex-col gap-10 px-10 pt-20">
  <div class="flex items-center justify-between">
    <h1>HOUSES</h1>
    <Button href="/add-house">ADD</Button>
  </div>
  {#if loading && houses.length === 0}
    <p>Loading...</p>
  {/if}
  {#if !loading && houses.length === 0}
    <p>No houses found</p>
  {/if}
  <div class="layout">
    {#each houses as h (h.uuid)}
      {@render house(h)}
    {/each}

    <a
      class="relative flex flex-col rounded-md border border-accent/20 shadow-xl shadow-accent/0 transition-all hover:shadow-accent/40"
      href="/add-house"
    >
      <div class="flex flex-1 flex-col items-center justify-center gap-2 p-4 transition-all">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-12 w-12 text-accent"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
        </svg>
        <p class="text-center">Add a new house</p>
      </div>
    </a>
  </div>
</main>

<style>
  .layout {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(min(200px, 100%), 1fr));
    gap: 1rem;
  }
</style>
