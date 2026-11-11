export type UploadSketchResult = {
  sizeInBytes: number
}

export async function uploadSketch(file: File): Promise<UploadSketchResult> {
  if (file.type !== 'image/png' || file.size === 0) {
    throw new Error('Please provide a non-empty PNG image.')
  }

  const form = new FormData()
  form.append('image', file)

  const response = await fetch('/api/sketches', {
    method: 'POST',
    body: form,
  })

  if (!response.ok) {
    throw new Error(`Upload failed (HTTP ${response.status}).`)
  }

  return response.json()
}
