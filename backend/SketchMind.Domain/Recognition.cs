namespace SketchMind.Domain
{
    public class Recognition
    {
        public Guid Id { get; private set; } = Guid.NewGuid();
        public DateTime CreatedAtUtc { get; private set; } = DateTime.UtcNow;
        public RecognitionStatus Status { get; private set; } = RecognitionStatus.Pending;

        public string? PredictedLabel { get; private set; }
        public double? Confidence { get; private set; }

        private Recognition() { }

        public void Complete(string label, double confidence)
        {
            if (Status is not RecognitionStatus.Pending)
            {
                throw new InvalidOperationException($"Cannot complete recognition from status {Status}");    
            }

            if (string.IsNullOrWhiteSpace(label))
            {
                throw new ArgumentException("Label is required.", nameof(label));
            }

            if (confidence is < 0 or > 1)
            {
                throw new ArgumentOutOfRangeException(nameof(confidence));
            }

            PredictedLabel = label;
            Confidence = confidence;
            Status = RecognitionStatus.Completed;
        }

        public void MarkModelUnavailable()
        {
            if (Status is not RecognitionStatus.Pending)
            {
                throw new InvalidOperationException($"Cannot mark recognition as unavailable from status {Status}.");
            }

            Status = RecognitionStatus.ModelUnavailable;
        }
            
    }
}