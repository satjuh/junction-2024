import { getHouse } from '$lib/api/house'

export const load = async ({ params, fetch, parent }) => ({
  house: await getHouse(fetch, params.uuid)
})
