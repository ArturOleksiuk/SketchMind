using Microsoft.AspNetCore.Mvc;
using SketchMind.Application.Interfaces.Sketches;

namespace SketchMind.Api.Controllers.Sketches;

[ApiController]
[Route("sketches")]
public sealed class SketchesController(ISketchService sketchService) : ControllerBase
{
    private const long MaxImageSizeInBytes = 1024 * 1024;

    [HttpPost]
    [Consumes("multipart/form-data")]
    public async Task<IActionResult> Upload([FromForm] IFormFile? image, CancellationToken cancellationToken)
    {
        if (image is null || image.Length == 0)
        {
            return BadRequest(new { message = "An image file is required." });
        }

        if (image.Length > MaxImageSizeInBytes)
        {
            return StatusCode(
                StatusCodes.Status413PayloadTooLarge,
                new { message = "The image must be 1 MiB or smaler." });
        }

        using var content = image.OpenReadStream();

        var result = await sketchService.UploadAsync(
            content,
            image.Length,
            cancellationToken);

        if (result is null)
        {
            return BadRequest(new { message = "The file must have a valid PNG signature." });
        }

        return Ok(result);
    }
}