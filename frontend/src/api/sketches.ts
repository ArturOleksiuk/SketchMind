export type UploadSketchResult = {
  fileName: string
  size: number
}

// Frontend-only mock. Replace this implementation with a multipart/form-data
// request when the backend upload endpoint is available.
export async function uploadSketch(file: File): Promise<UploadSketchResult> {
  if (file.type !== 'image/png' || file.size === 0) {
    throw new Error('Please provide a non-empty PNG image.')
  }

  // Simulate network latency without sending or storing the file.
  await new Promise<void>((resolve) => window.setTimeout(resolve, 700))

  return { fileName: file.name, size: file.size }
}
