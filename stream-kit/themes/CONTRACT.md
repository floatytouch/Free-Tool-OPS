# Stream overlay theme contract (OBS browser source, 1920x1080, Twitch, ENGLISH text)

Reference implementation (current look, same behaviour): ~/Documents/stream-kit/overlay.html — read it first.

One self-contained HTML file per theme. View picked by URL params:
- s = start | coding | bot | study | brb | end | dual   (end = OFFLINE screen)
- name (default "THINH · BUILD & STUDY"), topic, label (bar label), at=HH:MM (start countdown target, default 5 min from load)

Geometry is FIXED (OBS places video sources under the overlay; these areas must stay see-through, frames/decor may sit on the edges):
- coding, bot: screen 32,32 1440x935 ; camera 1504,32 384x288 ; side panel below camera
- study: camera 32,32 1200x935 ; right panel 1264..1888
- dual: display 1 at 32,32 920x935 ; display 2 at 968,32 920x935 ; face cam tile 1536,771 336x180
- bottom bar for live views inside y 996..1060 (x 32..1888)
- start, brb, end: fully opaque designed screens (no video)
Body background transparent for live views.

Live data every live view must show in the bar:
- now playing: poll fetch('nowplaying.json?t='+Date.now()) every 5 s -> {"track": "..."}; hide when empty. The page is served from http://127.0.0.1:18793/themes/<file>.html so the URL is '../nowplaying.json'.
- pomodoro locked to the wall clock: focus :00-:50, break :50-:00 (study view shows it big)
- clock HH:MM

Rules: Google Fonts allowed (must support Vietnamese diacritics for song names). No external JS libs needed; CSS/SVG/canvas animation encouraged but cheap (OBS CPU). Text must be legible at 1080p and after Twitch downscale. No blue as the main accent.

Deliver: write ~/Documents/stream-kit/themes/<file>.html AND copy it to "~/Library/Application Support/com.vietbyte.stream-kit/www/themes/<file>.html".
Preview: render every view with headless Chrome over http://127.0.0.1:18793/themes/<file>.html?s=<view> at 1920x1080
("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1920,1080 --virtual-time-budget=4000 --screenshot=/tmp/theme-<file>-<view>.png --user-data-dir=/tmp/chrome-theme-<file> <url>),
LOOK at every PNG and iterate until it is genuinely striking. Do NOT touch OBS, overlay.html or other theme files. Do not commit anything.
Report in at most 6 lines: concept, palette, the signature moments.
