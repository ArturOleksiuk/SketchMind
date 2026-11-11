using SketchMind.Application.DTOs.Sketches;

namespace SketchMind.Application.Interfaces.Sketches
{
    public interface ISketchService
    {
        Task<UploadSketchResult?> UploadAsync(
            Stream content,
            long size,
            CancellationToken cancellationToken);
    }
}