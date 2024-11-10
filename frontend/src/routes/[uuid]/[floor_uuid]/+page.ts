import { getHouse } from '$lib/api/house.js'
import { getObjectTemplates } from '$lib/api/objectTemplates.js'

export const load = async ({ params, fetch }) => {
  const house = await getHouse(fetch, params.uuid)

  return {
    house,
    floor_uuid: params.floor_uuid,
    floor: house.floors.find((floor) => floor.uuid === params.floor_uuid),
    objects: await getObjectTemplates(fetch)
  }
}
