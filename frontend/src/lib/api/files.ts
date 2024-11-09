import { baseUrl } from '.'

export type FileResponse = {
  floor_png: string
  floor_3D: string
}

export const uploadPng = async (file: Blob): Promise<FileResponse> => {
  const formData = new FormData()
  formData.append('in_file', file)
  const res = await fetch(`${baseUrl}/file/`, {
    method: 'POST',
    body: formData
  })
  if (!res.ok) {
    throw new Error('Failed to upload PNG')
  }
  return res.json()
}

export const fileUrl = (path: string) => `${baseUrl}/file/${path}`
