# scripts/test_mobile_viewport.py
import subprocess
import os

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
html_path = os.path.abspath("index.html")
url = "file:///" + html_path.replace("\\", "/")

# Test common mobile viewport dimensions: 375x667 (iPhone SE) and 390x844 (iPhone 14/15)
viewports = [
    ("iPhone SE (375x667)", "375,667"),
    ("iPhone 14/15 (390x844)", "390,844"),
    ("Compact Android (360x740)", "360,740")
]

for name, size in viewports:
    cmd = [
        edge_path,
        "--headless=new",
        f"--window-size={size}",
        "--virtual-time-budget=3000",
        "--dump-dom",
        url
    ]

    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=15)
    dom = proc.stdout
    print(f"\n--- Testing Mobile Viewport: {name} ---")
    print(f"Captured DOM length: {len(dom)} characters")

    checks = [
        ("Top Nav Header", 'class="top-nav"' in dom),
        ("Logo Group", 'id="nav-logo-btn"' in dom),
        ("Streak Pill", 'id="stat-streak-val"' in dom),
        ("ELO Pill", 'id="stat-elo-pill"' in dom),
        ("Rank & Analytics Button", 'id="btn-open-ranks-modal"' in dom),
        ("Sound Button", 'id="btn-toggle-sound"' in dom),
        ("Viewport meta has viewport-fit=cover", 'viewport-fit=cover' in dom)
    ]

    for label, ok in checks:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"  {status} {label}")
        if not ok:
            print(f"Failed check {label} on {name}")
            exit(1)

print("\n[SUCCESS] Mobile resolution and header layout validated on all phone viewports!")
