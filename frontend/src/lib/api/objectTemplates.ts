export type ObjectTemplate = {
  uuid: string
  name: string
  model: string // url
  data: string // any
}

export const getObjectTemplates = async (fetch: typeof window.fetch): Promise<ObjectTemplate[]> => {
  return [
    {
      uuid: '1',
      name: 'Elevator',
      model: '/elevator.glb',
      data: '{}'
    },
    {
      uuid: '2',
      name: 'Escalator',
      model: '/escalator.glb',
      data: '{}'
    },
    {
      uuid: '3',
      name: 'Electrical Box',
      model: '/eletric_box.glb',
      data: '{}'
    }
  ]
}
