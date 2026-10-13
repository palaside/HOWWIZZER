# ⚠️ MISTAKES & LESSONS LEARNED (WEPAPP)

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
