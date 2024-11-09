import { baseUrl } from '.'
import type { Floor } from './floors'

export type House = {
  uuid: string
  name: string
  address: string
  image: string
  latitude: number
  longitude: number
  description: string
  floors: Floor[]
}

export type CreateHouseDTO = Omit<House, 'uuid'>

export const createHouse = async (house: CreateHouseDTO): Promise<House> => {
  const response = await fetch(`${baseUrl}/houses`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(house)
  })

  if (!response.ok) {
    throw new Error('Failed to create house')
  }

  return response.json()
}

export const getHouses = async (): Promise<House[]> => {
  const response = await fetch(`${baseUrl}/houses`)

  if (!response.ok) {
    throw new Error('Failed to fetch houses')
  }

  return response.json()
}

export const getHouse = async (fetch: typeof window.fetch, uuid: string): Promise<House> => {
  const response = await fetch(`${baseUrl}/houses/${uuid}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    }
  })

  if (!response.ok) {
    throw new Error('Failed to fetch house')
  }

  return response.json()
}
