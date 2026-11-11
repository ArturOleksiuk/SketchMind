using Microsoft.Extensions.DependencyInjection;
using SketchMind.Application.Interfaces.Sketches;
using SketchMind.Application.Services;

namespace SketchMind.Application
{
    public static class DependencyInjection
    {
        public static IServiceCollection AddApplication(this IServiceCollection services)
        {
            services.AddScoped<ISketchService, SketchService>();

            return services;
        }
    }
}
