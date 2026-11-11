using SketchMind.Application.Interfaces.Sketches;
using SketchMind.Application.DTOs.Sketches;

namespace SketchMind.Application.Services
{
    public class SketchService : ISketchService
    {
        public async Task<UploadSketchResult?> UploadAsync(
            Stream content,
            long size,
            CancellationToken cancellationToken)
        {
            bool isPng = await ValidatePngAsync(content, cancellationToken);

            if (!isPng)
            {
                return null;
            }

            return new UploadSketchResult(
                SizeInBytes: size);
        }
        private static async Task<bool> ValidatePngAsync(Stream content, CancellationToken cancellationToken)
        {
            byte[] pngSignature = new byte[] { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A };

            var header = new byte[pngSignature.Length];

            int bytesRead = await content.ReadAtLeastAsync(
                header,
                minimumBytes: header.Length,
                throwOnEndOfStream: false,
                cancellationToken: cancellationToken
            );

            return bytesRead == pngSignature.Length && header.SequenceEqual(pngSignature);
        }
    }
}