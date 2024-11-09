<script lang="ts">
  import { goto } from '$app/navigation'
  import { createHouse, type CreateHouseDTO } from '$lib/api/house'
  import Button from '$lib/components/basics/Button.svelte'
  import { toast } from 'svelte-sonner'
  import type { FormEventHandler } from 'svelte/elements'

  let loading = $state(false)

  const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault()

    const formData = new FormData(e.currentTarget)
    const data = Object.fromEntries(formData)

    loading = true

    const base64 = await new Promise<string>((resolve) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result as string)
      reader.readAsDataURL(data.image as Blob)
    })

    const res = await createHouse({
      ...data,
      image: base64
    } as CreateHouseDTO)

    toast.success('House added successfully')

    loading = false
    goto('/')
  }
</script>

<main class="mx-auto flex max-w-screen-xl flex-col gap-10 px-10 pt-20">
  <h1>ADD HOUSE</h1>
  <form onsubmit={handleSubmit} class="flex flex-col gap-6">
    <label class="flex flex-col gap-1">
      <span>Name</span>
      <input class="border-secondary/40" type="text" name="name" required />
    </label>

    <label class="flex flex-col gap-1">
      <span>Address</span>
      <input class="border-secondary/40" type="text" name="address" required />
    </label>

    <div class="flex flex-col gap-1">
      <span>Location</span>
      <div class="flex gap-6">
        <label class="flex items-center gap-1">
          <span class=" text-background-300">N°</span>
          <input
            class="border-secondary/40"
            type="number"
            step="0.0001"
            name="latitude"
            placeholder="Latitude"
            required
          />
        </label>
        <label class="flex items-center gap-1">
          <span class=" text-background-300">E°</span>
          <input
            class="border-secondary/40"
            type="number"
            step="0.0001"
            name="longitude"
            placeholder="Longitude"
            required
          />
        </label>
      </div>
    </div>

    <label class="flex flex-col gap-1">
      <span>Description</span>
      <textarea class="border-secondary/40" name="description" required></textarea>
    </label>

    <label class="flex flex-col gap-1">
      <span>Image</span>
      <input class="border-secondary/40" type="file" name="image" accept="image/*" required />
    </label>

    <div>
      <Button type="submit" disabled={loading}>SAVE</Button>
    </div>
  </form>
</main>
