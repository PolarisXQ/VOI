// Custom JS logic
document.addEventListener('DOMContentLoaded', function () {
  const placeholder = document.getElementById('section-placeholder');
  const sectionUrl = new URL('section.html', window.location.href);

  fetch(sectionUrl)
    .then(function (response) {
      if (!response.ok) {
        throw new Error('section.html HTTP ' + response.status);
      }
      return response.text();
    })
    .then(function (data) {
      placeholder.innerHTML = data;

      // Initialize video comparisons after content is loaded
      if (typeof initVideoComparisons === 'function') {
        setTimeout(initVideoComparisons, 100);
      }
    })
    .catch(function (error) {
      console.error('Error loading the section:', error);
      placeholder.innerHTML =
        '<div style="font-family:system-ui,sans-serif;max-width:560px;margin:3rem auto;padding:1.5rem 2rem;border:1px solid #d2d2d7;border-radius:12px;background:#f5f5f7;color:#1d1d1f;line-height:1.6">' +
        '<strong>Could not load page content.</strong> If you opened this HTML file directly from disk, the browser blocks loading <code>section.html</code>. ' +
        'Run a local server from the project folder, then open the site from <code>http://localhost:…</code> (for example: <code>python3 -m http.server</code>).</div>';
    });
});