#!/usr/bin/env python3
"""Assemble the self-contained poster HTML (base64 images + QR), then render
PNG / thumbnail / PDF via headless Chrome.  Run: python3 build_poster.py"""
import base64, mimetypes, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
POSTER_DIR = os.path.dirname(HERE)
# Derive the paper figures from this file's own location so the script survives
# the repo being moved (it was hard-coded to /home/tk/repos/scipy_proceedings,
# which broke when repos were reorganised under owner directories).
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(POSTER_DIR)))
PAPER_FIG = os.path.join(REPO_ROOT, "papers", "taewoon_kim", "figures")
HUMEMAI_LOGO = os.environ.get(
    "HUMEMAI_LOGO",
    os.path.expanduser("~/repos/humemai/humem.ai/public/images/site/humemai-no-text.png"),
)

def b64(path):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

def main():
    tpl = open(os.path.join(HERE, "poster.template.html")).read()
    repl = {
        "{{HUMEMAI_LOGO}}": b64(HUMEMAI_LOGO),
        "{{ARCADE_LOGO}}":  b64(os.path.join(PAPER_FIG, "thumbnail.png")),
        "{{HYBRID_IMG}}":   b64(os.path.join(PAPER_FIG, "hybrid_workflow.png")),
        "{{ARCH_IMG}}":     b64(os.path.join(PAPER_FIG, "architecture.png")),
    }
    html = tpl
    for k, v in repl.items():
        html = html.replace(k, v)
    out_html = os.path.join(HERE, "poster.built.html")
    open(out_html, "w").write(html)
    print(f"✓ assembled {out_html} ({len(html)//1024} KiB)")

    png = os.path.join(POSTER_DIR, "poster.png")
    pdf = os.path.join(POSTER_DIR, "poster.pdf")
    common = ["google-chrome", "--headless=new", "--disable-gpu", "--no-sandbox",
              "--hide-scrollbars", "--force-color-profile=srgb",
              "--default-background-color=FFFFFFFF"]
    # PNG at 2x → 3840x2160
    subprocess.run(common + ["--window-size=1920,1080",
                   "--force-device-scale-factor=2",
                   f"--screenshot={png}", f"file://{out_html}"], check=True)
    print(f"✓ rendered {png}")
    # PDF (for the optional Zenodo archive)
    subprocess.run(common + ["--no-pdf-header-footer",
                   f"--print-to-pdf={pdf}", f"file://{out_html}"], check=True)
    print(f"✓ rendered {pdf}")

    try:
        from PIL import Image
        im = Image.open(png)
        print(f"  full PNG size: {os.path.getsize(png)//1024} KiB ({im.size[0]}x{im.size[1]})")
    except Exception as e:
        print(f"  ! size check failed: {e}", file=sys.stderr)

    # Dedicated punchy thumbnail (1280x720 @2x → 2560x1440, then crisp 1280x720)
    tpl2 = open(os.path.join(HERE, "thumbnail.template.html")).read()
    for k, v in repl.items():
        tpl2 = tpl2.replace(k, v)
    out_html2 = os.path.join(HERE, "thumbnail.built.html")
    open(out_html2, "w").write(tpl2)
    tn_big = os.path.join(HERE, "_thumb_2x.png")
    subprocess.run(common + ["--window-size=1280,720", "--force-device-scale-factor=2",
                   f"--screenshot={tn_big}", f"file://{out_html2}"], check=True)
    try:
        from PIL import Image
        tpath = os.path.join(POSTER_DIR, "poster_thumbnail.png")
        Image.open(tn_big).convert("RGB").resize((1280, 720), Image.LANCZOS).save(tpath, optimize=True)
        os.remove(tn_big)
        print(f"✓ custom thumbnail {tpath}  ({os.path.getsize(tpath)//1024} KiB, 1280x720)")
    except Exception as e:
        print(f"  ! custom thumbnail step failed: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
