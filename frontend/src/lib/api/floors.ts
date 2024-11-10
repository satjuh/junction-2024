import { baseUrl } from '.'
import type { Object3d } from './object3d'

export type Floor = {
  uuid: string
  name: string
  index: number
  height: number
  floor_3D: string
  floor_3D_walls?: string
  floor_png: string
  objects?: Object3d[]
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
  const res = await fetch(`${baseUrl}/floor/${uuid}`, {
    method: 'PUT',
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
