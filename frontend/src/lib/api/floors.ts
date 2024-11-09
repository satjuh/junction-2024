import { baseUrl } from '.'

export type Floor = {
  uuid: string
  name: string
  index: number
  height: number
  floor_3D: string
  floor_png: string
}

export type CreateFloorDTO = Omit<Floor, 'uuid'> & { house_id: string }

export const createFloor = async (dto: CreateFloorDTO): Promise<Floor> => {
  const res = await fetch(`${baseUrl}/floor`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dto)
  })

  if (!res.ok) {
    throw new Error('Failed to create floor')
  }

  return res.json()
}

export const updateFloor = async (uuid: string, dto: Floor): Promise<Floor> => {
  const res = await fetch(`${baseUrl}/floors/${uuid}`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dto)
  })

  if (!res.ok) {
    throw new Error('Failed to update floor')
  }

  return res.json()
}
