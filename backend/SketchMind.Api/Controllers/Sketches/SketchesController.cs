using Microsoft.AspNetCore.Mvc;

namespace SketchMind.Api.Controllers.Sketches;

[ApiController]
[Route("sketches")]
public sealed class SketchesController : ControllerBase
{
    private const long MaxImageSizeInBytes = 1024 * 1024;

    [HttpPost]
    [Consumes("multipart/form-data")]
    public IActionResult Upload([FromForm] IFormFile? image)
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

        return Ok(new { sizeInBytes = image.Length });
    }
}