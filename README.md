# Starlink Mobile — Interactive Roadmap

Single-page interactive tool covering SpaceX's spectrum holdings, direct-to-cell
physics and capacity, satellite technology generations, the hybrid network plan,
and regulatory/standards status. Data as of August 2026.

## Deploy to Railway (via GitHub)

1. Create a new GitHub repo (e.g. `starlink-roadmap`), then from this folder:

       git init
       git add .
       git commit -m "Starlink Mobile interactive roadmap"
       git branch -M main
       git remote add origin https://github.com/YOUR_USERNAME/starlink-roadmap.git
       git push -u origin main

2. In Railway: **New Project → Deploy from GitHub repo** → pick the repo.
   Railway auto-detects the Node app and runs `npm install && npm start`.

3. When the deploy goes green: **Settings → Networking → Generate Domain**.
   That URL is your shareable link.

Updates: replace `index.html`, commit, push — Railway redeploys automatically.

## Run locally

    npx serve -s .

Note: the page loads React and fonts from public CDNs, so viewers need internet access.
