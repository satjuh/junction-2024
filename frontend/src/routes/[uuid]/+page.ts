import { getHouse } from '$lib/api/house'

export const load = async ({ params, fetch }) => {
  const uuid = params.uuid

  return {
    house: await getHouse(fetch, uuid)
  }
}
