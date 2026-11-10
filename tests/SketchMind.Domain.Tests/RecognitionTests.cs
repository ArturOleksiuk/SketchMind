using Xunit;
using SketchMind.Domain;

namespace SketchMind.Domain.Tests;

public class RecognitionTests
{
    const string TestLabel  = "cat";
    const double TestConfidence = 0.98;

    [Fact]
    public void Complete_ValidResult_SetsPredictionAndCompletedStatus()
    {
        // Arrange

        var recognition = new Recognition();

        // Act

        recognition.Complete(TestLabel, TestConfidence);

        // Assert
        Assert.Equal(RecognitionStatus.Completed, recognition.Status);
        Assert.Equal(TestLabel, recognition.PredictedLabel);
        Assert.Equal(TestConfidence, recognition.Confidence);
    }

    [Fact]
    public void Constructor_InitializesDefaultValues()
    {
        // Act

        var recognition = new Recognition();

        // Assert
        Assert.Equal(RecognitionStatus.Pending, recognition.Status);
        Assert.Null(recognition.PredictedLabel);
        Assert.Null(recognition.Confidence);
        Assert.NotEqual(DateTime.MinValue, recognition.CreatedAtUtc);
        Assert.NotEqual(Guid.Empty, recognition.Id);
    }

    [Fact]
    public void Complete_WithEmptyLabel_ThrowsArgumentException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act
        // Assert

        Assert.Throws<ArgumentException>( 
            () => recognition.Complete("", TestConfidence));
    }

    [Fact]
    public void Complete_WithConfidenceBelowZero_ThrowsArgumentOutOfRangeException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act
        // Assert

        Assert.Throws<ArgumentOutOfRangeException>(
            () => recognition.Complete(TestLabel, -0.4));
    }

    [Fact]
    public void Complete_WithConfidenceAboveOne_ThrowsArgumentOutOfRangeException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act
        // Assert

        Assert.Throws<ArgumentOutOfRangeException>(
            () => recognition.Complete(TestLabel, 1.3));
    }

    [Fact]
    public void Complete_WithAlreadyCompleted_ThrowsInvalidOperationException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act

        recognition.Complete(TestLabel, TestConfidence);

        // Assert

        Assert.Throws<InvalidOperationException>(
            () => recognition.Complete(TestLabel, TestConfidence));
    }

    [Fact]
    public void Complete_WhenModelUnavailable_ThrowsInvalidOperationException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act

        recognition.MarkModelUnavailable();

        // Assert

        Assert.Equal(RecognitionStatus.ModelUnavailable, recognition.Status);
        Assert.Throws<InvalidOperationException>(
            () => recognition.Complete(TestLabel, TestConfidence));
    }

    [Fact]
    public void MarkModelUnavailable_WhenPending_SetsStatusAndLeavesPredictionUnset()
    {
        // Arrange 

        var recognition = new Recognition();

        // Act 

        recognition.MarkModelUnavailable();

        // Assert

        Assert.Equal(RecognitionStatus.ModelUnavailable, recognition.Status);
        Assert.Null(recognition.PredictedLabel);
        Assert.Null(recognition.Confidence);
    }

    [Fact]
    public void MarkModelUnavailable_WhenAlreadyCompleted_ThrowsInvalidOperationException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act

        recognition.Complete(TestLabel, TestConfidence);

        // Assert

        Assert.Throws<InvalidOperationException>(
            () => recognition.MarkModelUnavailable());
    }

    [Fact]

    public void MarkModelUnavialable_WhenAlreadyUnavailable_ThrowsInvalidOperationException()
    {
        // Arrange

        var recognition = new Recognition();

        // Act

        recognition.MarkModelUnavailable();

        // Assert

        Assert.Throws<InvalidOperationException>(
            () => recognition.MarkModelUnavailable());
    }
}