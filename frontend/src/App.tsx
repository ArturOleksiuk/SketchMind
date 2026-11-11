import { useRef, useState } from 'react'
import { ReactSketchCanvas } from 'react-sketch-canvas'
import type { ReactSketchCanvasRef } from 'react-sketch-canvas'
import { uploadSketch } from './api/sketches'

export default function App() {
  const canvasRef = useRef<ReactSketchCanvasRef>(null)
  const uploadInProgress = useRef(false)
  const [hasDrawing, setHasDrawing] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [feedback, setFeedback] = useState('')
  const [hasError, setHasError] = useState(false)

  function clearSketch() {
    canvasRef.current?.clearCanvas()
    setFeedback('')
    setHasError(false)
  }

  async function sendSketch() {
    const canvas = canvasRef.current
    if (!canvas || !hasDrawing || uploadInProgress.current) return

    uploadInProgress.current = true
    setIsUploading(true)
    setFeedback('')
    setHasError(false)

    try {
      const dataUrl = await canvas.exportImage('png')
      // Convert the locally generated data URL to a file; no server is called.
      const image = await fetch(dataUrl)
      const blob = await image.blob()
      const file = new File([blob], 'sketch.png', { type: 'image/png' })
      const result = await uploadSketch(file)

      setFeedback(
        `Demo upload complete: ${result.fileName} (${(result.size / 1024).toFixed(1)} KB). No file was sent to the backend.`,
      )
    } catch (error) {
      setHasError(true)
      setFeedback(error instanceof Error ? error.message : 'Could not prepare the drawing. Please try again.')
    } finally {
      uploadInProgress.current = false
      setIsUploading(false)
    }
  }

  return (
    <main className="min-h-screen bg-[#f3f5ef] px-4 py-10 text-[#172b23] sm:py-16">
      <div className="mx-auto max-w-3xl">
        <header className="mb-7 sm:mb-9">
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
            SketchMind
          </h1>
          <p className="mt-3 text-base text-[#526458] sm:text-lg">
            Draw a simple object, like a cat, a tree, or a bicycle.
          </p>
        </header>

        <section
          aria-labelledby="canvas-title"
          className="rounded-3xl border border-[#dce3d8] bg-white p-3 shadow-sm sm:p-5"
        >
          <div className="flex items-center justify-between gap-4 px-2 pb-3">
            <h2 id="canvas-title" className="text-base font-semibold">
              Drawing canvas
            </h2>

            <button
              type="button"
              onClick={clearSketch}
              disabled={isUploading || !hasDrawing}
              className="rounded-lg border border-[#dce3d8] px-4 py-2 text-sm font-medium transition hover:bg-[#eef3eb] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#35634e] disabled:cursor-not-allowed disabled:opacity-50"
            >
              Clear
            </button>
          </div>

          <div className="h-[320px] overflow-hidden rounded-2xl border border-[#e4e9e1] sm:h-[440px]">
            <ReactSketchCanvas
              ref={canvasRef}
              width="100%"
              height="100%"
              canvasColor="#ffffff"
              strokeColor="#172b23"
              strokeWidth={5}
              readOnly={isUploading}
              onChange={(paths) => {
                setHasDrawing(paths.some((path) => path.drawMode))
                setFeedback('')
                setHasError(false)
              }}
              style={{ border: 'none', borderRadius: 0 }}
            />
          </div>

          <div className="mt-4 flex flex-wrap items-center justify-between gap-3 px-2">
            <p className="text-sm text-[#526458]">PNG upload · Demo mode</p>
            <button
              type="button"
              onClick={sendSketch}
              disabled={!hasDrawing || isUploading}
              className="rounded-lg bg-[#35634e] px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-[#284c3b] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#35634e] disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isUploading ? 'Sending…' : 'Send drawing'}
            </button>
          </div>
          <p
            role="status"
            aria-live="polite"
            className={`mt-3 px-2 text-sm ${hasError ? 'text-red-700' : 'text-[#35634e]'}`}
          >
            {isUploading ? 'Preparing PNG and simulating an upload…' : feedback}
          </p>
        </section>
      </div>
    </main>
  )
}
