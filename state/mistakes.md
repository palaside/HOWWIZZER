# ⚠️ MISTAKES & LESSONS LEARNED (WEPAPP / HOWWIZZER)

### 1. PowerShell Multi-line Strings & Syntax
- **Problem:** Using `&&` in PowerShell causes syntax errors. Using multi-line inline scripts with quotes often breaks argument parsing.
- **Fix:** Use `;` instead of `&&`. Put Python test/inspection scripts in separate files and execute them directly via Python.

### 2. CSS Stylesheet vs. Inline Style Overrides
- **Problem:** `.sig-role-anchor` had `left: 0; right: 0;` in the stylesheet `<style>`, which constrained elements to the inside of `.sig-name-wrapper` despite inline `right: 100%`.
- **Fix:** Clean up stylesheet classes to ensure `.sig-role-anchor` and `.sig-label-anchor` only declare `position: absolute; right: 100%; white-space: nowrap; text-align: right;` without `left: 0;`.

### 3. Multi-Enter Gap Calculation
- **Problem:** Adding CSS `margin-top` on top of existing `margin-bottom` on parent containers and child wrappers multiplies the perceived blank lines, turning 1 Enter into 3 Enters, or 5 Enters into 8 Enters.
- **Fix:** Remove bottom margins from preceding sections/rows before applying top margin to target rows. Always measure actual pixel gaps via Computer Vision projection.

### 4. RTA Memo Computer Template Margins and Garuda Dimensions
- **Problem:** Using standard 25mm top margin and 30mm garuda for computer-generated military memos causes text displacement compared to the official software template.
- **Fix:** In RTA Sarabun 2563 Appendix A Sub-Appendix 1 (Page 29), use top margin 15mm, left 30mm, right 20mm, bottom 20mm, and Garuda dimensions 15mm height x 13.8mm width.

### 5. Signature Block Strict Separation
- **Problem:** In informal memos, accidentally placing rank and name on the same line violates official military correspondence rules.
- **Fix:** Always lift rank above the signature space (`bottom: calc(100% + 18px)` relative to name wrapper). Rank endpoint period MUST align with opening parenthesis.

### 6. Vercel Serverless Python & Framework Preset
- **Problem:** When importing from GitHub, Vercel defaults to Next.js if a `package.json` exists at the root, throwing `NEXT_NO_VERSION` or `STATIC_BUILD_NO_OUT_DIR`.
- **Fix:** Set `"framework": null`, provide a lightweight `build.js` generating `dist/index.html`, and set `"outputDirectory": "dist"` in `vercel.json`.

### 7. Vercel Serverless Lambda Bundle Limit (225 MB)
- **Problem:** Installing development packages (`pytest`, `watchfiles`, `pygments`) and bundling frontend `node_modules` pushes the uncompressed Lambda bundle size beyond 225 MB.
- **Fix:** Exclude dev/test packages from `requirements.txt`, add heavy docs/references to `.vercelignore`, and configure `"installCommand": "echo 'skip'"` in `vercel.json` to prevent bundling node_modules.
