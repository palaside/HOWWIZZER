const fs = require('fs');
const path = require('path');

const targetFiles = [
  path.join(process.cwd(), 'แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html'),
  path.join(process.cwd(), 'references', 'approved_sd1_weekly_report', 'แบบรายงานผลการตรวจ_สด_1_Rebuild_Thai.html'),
  path.join(process.cwd(), 'บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html'),
  path.join(process.cwd(), 'references', 'approved_weekly_inspection', 'บันทึกรายงานผลการตรวจประจำสัปดาห์_Rebuild_Thai.html'),
  path.join(process.cwd(), 'page1_sd1_template.html')
];

const hydrationScript = `
    <!-- REAL-TIME INSPECTION PHOTOS HYDRATION SCRIPT -->
    <script>
    (function() {
        function hydrateInspectionPhotos() {
            try {
                var raw = localStorage.getItem('inspection_photos');
                if (!raw) return;
                var photos = JSON.parse(raw);
                if (!Array.isArray(photos)) return;
                for (var i = 1; i <= 4; i++) {
                    var el = document.getElementById('inspection-photo-' + i);
                    if (el && photos[i - 1]) {
                        el.src = photos[i - 1];
                    }
                }
            } catch(e) {
                console.error('Failed to hydrate inspection photos:', e);
            }
        }
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', hydrateInspectionPhotos);
        } else {
            hydrateInspectionPhotos();
        }
        window.addEventListener('storage', function(e) {
            if (e.key === 'inspection_photos') {
                hydrateInspectionPhotos();
            }
        });
    })();
    </script>
`;

targetFiles.forEach(filePath => {
  if (!fs.existsSync(filePath)) {
    console.log('Skipping missing file:', filePath);
    return;
  }
  let html = fs.readFileSync(filePath, 'utf8');

  // Replace photo-card <img> to have id="inspection-photo-1" .. 4
  let count = 0;
  html = html.replace(/(<div class="photo-card">\s*<img\s+)(src="data:image\/[^"]+")/g, (match, prefix, srcPart) => {
    count++;
    if (count <= 4) {
      return `${prefix}id="inspection-photo-${count}" ${srcPart}`;
    }
    return match;
  });

  // If already had id="inspection-photo-X", ensure no duplicate attributes
  html = html.replace(/id="inspection-photo-\d+"\s+id="inspection-photo-(\d+)"/g, 'id="inspection-photo-$1"');

  // Inject hydration script before </body> if not already present
  if (!html.includes('hydrateInspectionPhotos')) {
    html = html.replace('</body>', `${hydrationScript}\n</body>`);
  }

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`Updated ${path.basename(filePath)} (assigned ${count} photo IDs and hydration script)`);
});
