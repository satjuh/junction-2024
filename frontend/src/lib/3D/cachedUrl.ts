import { retrieveFile } from '$lib/indexdb'
import { writable } from 'svelte/store'

export const cachedUrl = (url: string) => {
  const { subscribe, set } = writable<string | undefined>(undefined)

  retrieveFile(url).then((data) => {
    set(URL.createObjectURL(data))
  })

  return { subscribe }
}
