// Custom JS logic
document.addEventListener('DOMContentLoaded', function () {
  fetch('section.html')
    .then(response => response.text())
    .then(data => {
      document.getElementById('section-placeholder').innerHTML = data;

      // Initialize video comparisons after content is loaded
      // We need to check if initVideoComparisons is available (from video-comparison.js)
      if (typeof initVideoComparisons === 'function') {
        // Small delay to ensure DOM is ready and layout is stable
        setTimeout(initVideoComparisons, 100);
      }
    })
    .catch(error => console.error('Error loading the section:', error));
});