import { baseUrl } from '.'

export type Object3d = {
  name: string
  x: number
  y: number
  z: number
  data: string
  rotation: number
  file_uuid: string
  floor_id: string
  uuid: string
}

export type CreateObject3dDTO = Omit<Object3d, 'uuid'>

export const createObject3d = async (dto: CreateObject3dDTO): Promise<Object3d> => {
  const res = await fetch(`${baseUrl}/object3ds`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(dto)
  })

  if (!res.ok) {
    throw new Error('Failed to create object3d')
  }

  return res.json()
}
