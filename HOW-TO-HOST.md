# How to Host Your Dashboard (Free, No Domain Needed)

## Option 1: GitHub Pages (BEST — Free, Always Live)

### One-Time Setup (10 minutes)

1. Go to github.com → Create a new repository
   - Name: `cloud-dashboard` (or anything you want)
   - Make it **Public** (required for free GitHub Pages)
   - Click "Create repository"

2. Upload the `cloud-executive-summary.html` file
   - Rename it to `index.html` before uploading
   - Click "Add file" → "Upload files" → drag the file → "Commit"

3. Enable GitHub Pages
   - Go to Settings → Pages
   - Source: "Deploy from a branch"
   - Branch: `main` → folder: `/ (root)`
   - Click Save

4. Wait 2 minutes. Your dashboard is live at:
   ```
   https://YOUR-USERNAME.github.io/cloud-dashboard/
   ```

5. Share this link with TJ and anyone else. They open it → see the dashboard.

### Adding New Month Data (5 minutes each month)

1. Go to your repository on github.com
2. Click on `index.html`
3. Click the pencil icon (Edit)
4. Find the DATA section at the top (around line 20)
5. Add the new month. Example — adding Feb 2026:

   BEFORE:
   ```
   months: ["Aug 2025","Sep 2025","Oct 2025","Nov 2025","Dec 2025","Jan 2026"],
   ```
   
   AFTER:
   ```
   months: ["Aug 2025","Sep 2025","Oct 2025","Nov 2025","Dec 2025","Jan 2026","Feb 2026"],
   ```

   Do the same for costs and budgets:
   ```
   costs:   [1571750.63, 1546713.68, 1634927.43, 1618618.04, 1713896.84, 1740906.54, NEW_NUMBER],
   budgets: [1500000, 1500000, 1500000, 1500000, 1500000, 1850000, 1850000],
   ```

6. Click "Commit changes"
7. Wait 1-2 minutes → the live link auto-updates!

That's it. No coding, no deployment, no server.


## Option 2: SharePoint / Teams (If GitHub Not Allowed)

1. Upload the HTML file to a SharePoint folder
2. Share the link with your team
3. They download and open in browser
4. When you update, replace the file in SharePoint


## Option 3: Email the File

1. Just email the HTML file to TJ or anyone
2. They save it and open in Chrome/Edge
3. When you have updates, send the new file


## Recommended: Option 1 (GitHub Pages)
- Free forever
- One link that always works
- Auto-updates when you edit
- No domain or hosting to buy
- Professional URL
