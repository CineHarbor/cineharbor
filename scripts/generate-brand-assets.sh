#!/usr/bin/env bash
# Generate CineHarbor raster brand assets from the SVG masters.
# Requires: macOS qlmanage (WebKit), sips, iconutil, python3 (stdlib).
set -euo pipefail

UMBRELLA="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BRAND="$UMBRELLA/assets/brand"
WEB="$UMBRELLA/../cineharbor-web/public"
DESK="$UMBRELLA/../cineharbor-desktop/src-tauri/icons"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

FONT="$BRAND/fonts/Inter.ttf"

render () { # render <svg> <maxdim> <outbasename>
  # 生成内嵌 Inter 的自包含渲染副本（不依赖系统字体）
  python3 - "$FONT" "$1" "$TMP/$3.svg" <<'PY'
import sys, re, base64
font, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
b64 = base64.b64encode(open(font, 'rb').read()).decode()
css = ("<defs><style>@font-face{font-family:'CHInter';"
       f"src:url(data:font/ttf;base64,{b64}) format('truetype');"
       "font-weight:100 900;}</style></defs>")
s = open(src).read()
s = s.replace(
    "font-family=\"Inter, -apple-system, 'Helvetica Neue', Helvetica, Arial, sans-serif\"",
    "font-family='CHInter'")
s = re.sub(r'(<svg[^>]*>)', r'\1' + css, s, count=1)
open(dst, 'w').write(s)
PY
  qlmanage -t -s "$2" -o "$TMP" "$TMP/$3.svg" >/dev/null 2>&1
  mv "$TMP/$3.svg.png" "$TMP/$3.png"
}
resize () { # resize <src> <w> <h> <dst>
  sips -z "$3" "$2" "$1" --out "$4" >/dev/null 2>&1
}

echo "== rasterize masters =="
render "$BRAND/cineharbor-icon.svg"         1024 base_icon
render "$BRAND/cineharbor-og.svg"           1200 og
render "$BRAND/cineharbor-wordmark-dark.svg" 1200 wordmark_dark

echo "== web icons =="
for s in 192 256 384 512; do
  resize "$TMP/base_icon.png" "$s" "$s" "$WEB/icons/icon-${s}x${s}.png"
done
resize "$TMP/base_icon.png" 512 512 "$WEB/icons/icon-512-maskable.png"
resize "$TMP/base_icon.png" 180 180 "$WEB/apple-touch-icon.png"
resize "$TMP/base_icon.png"  16  16 "$WEB/favicon-16x16.png"
resize "$TMP/base_icon.png"  32  32 "$WEB/favicon-32x32.png"
resize "$TMP/wordmark_dark.png" 1200 300 "$WEB/logo.png"
resize "$TMP/og.png" 1200 630 "$WEB/og-image.png"

echo "== desktop icons =="
resize "$TMP/base_icon.png" 1024 1024 "$DESK/icon.png"
resize "$TMP/base_icon.png"   32   32 "$DESK/32x32.png"
resize "$TMP/base_icon.png"   64   64 "$DESK/64x64.png"
resize "$TMP/base_icon.png"  128  128 "$DESK/128x128.png"
resize "$TMP/base_icon.png"  256  256 "$DESK/128x128@2x.png"
resize "$TMP/base_icon.png"   30   30 "$DESK/Square30x30Logo.png"
resize "$TMP/base_icon.png"   44   44 "$DESK/Square44x44Logo.png"
resize "$TMP/base_icon.png"   71   71 "$DESK/Square71x71Logo.png"
resize "$TMP/base_icon.png"   89   89 "$DESK/Square89x89Logo.png"
resize "$TMP/base_icon.png"  107  107 "$DESK/Square107x107Logo.png"
resize "$TMP/base_icon.png"  142  142 "$DESK/Square142x142Logo.png"
resize "$TMP/base_icon.png"  150  150 "$DESK/Square150x150Logo.png"
resize "$TMP/base_icon.png"  284  284 "$DESK/Square284x284Logo.png"
resize "$TMP/base_icon.png"  310  310 "$DESK/Square310x310Logo.png"
resize "$TMP/base_icon.png"   50   50 "$DESK/StoreLogo.png"

echo "== .icns (iconutil) =="
ICONSET="$TMP/icon.iconset"; mkdir -p "$ICONSET"
resize "$TMP/base_icon.png"  16  16 "$ICONSET/icon_16x16.png"
resize "$TMP/base_icon.png"  32  32 "$ICONSET/icon_16x16@2x.png"
resize "$TMP/base_icon.png"  32  32 "$ICONSET/icon_32x32.png"
resize "$TMP/base_icon.png"  64  64 "$ICONSET/icon_32x32@2x.png"
resize "$TMP/base_icon.png" 128 128 "$ICONSET/icon_128x128.png"
resize "$TMP/base_icon.png" 256 256 "$ICONSET/icon_128x128@2x.png"
resize "$TMP/base_icon.png" 256 256 "$ICONSET/icon_256x256.png"
resize "$TMP/base_icon.png" 512 512 "$ICONSET/icon_256x256@2x.png"
resize "$TMP/base_icon.png" 512 512 "$ICONSET/icon_512x512.png"
resize "$TMP/base_icon.png" 1024 1024 "$ICONSET/icon_512x512@2x.png"
iconutil -c icns "$ICONSET" -o "$DESK/icon.icns"

echo "== .ico (stdlib PNG-embedded ICO writer) =="
for w in 16 32 48 256; do
  resize "$TMP/base_icon.png" "$w" "$w" "$TMP/ico_${w}.png"
done
python3 - "$DESK/icon.ico" "$WEB/favicon.ico" "$TMP" <<'PY'
import struct, sys
ico_dst, fav_dst, tmp = sys.argv[1:4]
def read(w):
    return open(f"{tmp}/ico_{w}.png", 'rb').read()
def write_ico(ws, dst):
    entries = [(w, read(w)) for w in ws]
    header = struct.pack('<HHH', 0, 1, len(entries))
    dep = b''; body = b''; offset = 6 + 16 * len(entries)
    for w, data in entries:
        b = w % 256
        dep += struct.pack('<BBBBHHII', b, b, 0, 0, 1, 32, len(data), offset)
        offset += len(data)
        body += data
    open(dst, 'wb').write(header + dep + body)
write_ico([16, 32, 48, 256], ico_dst)
write_ico([16, 32, 48], fav_dst)
print("ico written:", ico_dst, fav_dst)
PY

echo "== 生成完成 =="
ls -1 "$TMP/base_icon.png" "$TMP/og.png" "$TMP/wordmark_dark.png"