import { getHouse } from '$lib/api/house'

export const load = async ({ params, fetch, parent }) => {
  const uuid = params.uuid

  return {
    house: await getHouse(fetch, uuid)
  }
}
