#!/usr/bin/env python3
"""Organize and prepare videos for the GitHub Release."""

import argparse
import os
import shutil
from pathlib import Path
from typing import List, Optional, Tuple

REPO = "kevmoz/polymathica-hackathon"
TAG = "v1.0.0-hackathon"
DEFAULT_BASE_PATH = r"D:\Polymathica\ACTIVE_REPO\runtime_outputs"
RELEASE_ASSET_DIR = Path("release_assets")

VIDEO_SOURCES = [
    {
        "name": "System Overview Cinematic",
        "path": "v493_60s_cinematic_reel/polymathica_60s_cinematic.mp4",
        "release_name": "polymathica_60s_cinematic.mp4",
        "description": "High-level system overview and feature highlights",
    },
    {
        "name": "Navier-Stokes Simulation",
        "path": "v482_ns_cinematic_video/polymathica_navier_stokes_cinematic.mp4",
        "release_name": "polymathica_ns_cinematic.mp4",
        "description": "Real Navier-Stokes CFD simulation execution",
    },
    {
        "name": "Graphics Core & Post-Effects",
        "path": "v478_postfx_export/polymathica_postfx_reel.mp4",
        "release_name": "polymathica_graphics_core_postfx.mp4",
        "description": "Graphics rendering and post-processing demonstration",
    },
    {
        "name": "NS Results Reel",
        "path": "v477_video_export/polymathica_ns_reel.mp4",
        "release_name": "polymathica_ns_results.mp4",
        "description": "Simulation results and evidence visualization",
    },
    {
        "name": "3D GPU-Accelerated (CUDA/NVENC)",
        "path": "governed_graphics_core/ns3d-v64-cuda-nvenc-60s/run-v64-60s-001/video.mp4",
        "release_name": "polymathica_3d_gpu_cuda_60s.mp4",
        "description": "3D Navier-Stokes with real-time GPU rendering",
    },
    {
        "name": "2D Lid-Driven Cavity Replay",
        "path": "v525_operational_recovery/ns2d/V526-NS2D-SHARP-001/v525_ns2d_lid_replay.mp4",
        "release_name": "polymathica_2d_validation_replay.mp4",
        "description": "2D validation simulation with replay verification",
    },
    {
        "name": "Lab Workspace Simulation",
        "path": "ns_lab/1096fbff-0419-468b-be9d-d550e53098c4/simulation.mp4",
        "release_name": "polymathica_lab_workflow.mp4",
        "description": "Complete lab workflow with monitoring",
    },
]

def verify_videos(base_path: str) -> List[Tuple[str, bool, Optional[str]]]:
    """
    Verify all video files exist.
    
    Args:
        base_path: Base directory on D: drive
        
    Returns:
        List of (video_name, exists, path) tuples
    """
    results = []
    for video in VIDEO_SOURCES:
        full_path = os.path.join(base_path, video["path"])
        exists = os.path.isfile(full_path)
        results.append((video["name"], exists, full_path if exists else None))
    return results

def prepare_release_assets(base_path: str, output_dir: Path = RELEASE_ASSET_DIR) -> List[Path]:
    """Copy found videos to release asset filenames used by the gallery."""
    output_dir.mkdir(parents=True, exist_ok=True)

    copied = []
    for video in VIDEO_SOURCES:
        source = Path(base_path) / video["path"]
        if not source.is_file():
            continue
        target = output_dir / video["release_name"]
        shutil.copy2(source, target)
        copied.append(target)
    return copied


def print_upload_commands() -> None:
    """
    Print gh release upload commands.
    
    Args:
        base_path: Base directory on D: drive
    """
    print("\n" + "="*70)
    print("GitHub Release Upload Commands")
    print("="*70 + "\n")
    
    print("Step 1: Create release if it does not already exist")
    print(f"""gh release create {TAG} \\
  --title "POLYMATHICA Hackathon Submission" \\
  --notes "Complete autonomous scientific laboratory with real GPU-accelerated simulations" \\
  --repo {REPO}\n""")
    
    print("Step 2: Upload all prepared videos")
    print(f"""gh release upload {TAG} \\""")
    
    for video in VIDEO_SOURCES:
        full_path = RELEASE_ASSET_DIR / video["release_name"]
        print(f"  '{full_path}' \\")
    print(f"  --repo {REPO} --clobber\n")

def generate_html_gallery(output_path: str) -> None:
    """
    Generate HTML gallery with video embeds.
    
    Args:
        output_path: Path to write index.html
    """
    html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>POLYMATHICA Video Gallery</title>
    <style>
        body { font-family: Arial; max-width: 1200px; margin: 0 auto; padding: 20px; background: #0d1117; color: #c9d1d9; }
        h1 { text-align: center; color: #fff; }
        .links { text-align: center; margin: 0 0 24px; }
        .links a { margin: 0 10px; }
        .videos { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .video-card { background: #1a1a1a; border: 1px solid #333; border-radius: 8px; padding: 20px; }
        .video-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .video-description { font-size: 0.9em; color: #aaa; margin-bottom: 15px; }
        video { width: 100%; border-radius: 4px; background: #000; }
        a { color: #238636; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>POLYMATHICA Video Gallery</h1>
    <p class="links">
        <a href="https://github.com/kevmoz/polymathica-hackathon">Repository</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/JUDGING_GUIDE.md">Judging Guide</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/REVIEWER_NOTE.md">Reviewer Note</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/SCORECARD_RESPONSE.md">Scorecard</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/API_REFERENCE.md">API</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/VERIFICATION.md">Verify</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/ARCHITECTURE.md">Architecture</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/BENCHMARK.md">Benchmark</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/BENCHMARK_MATRIX.md">Matrix</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/PROJECTION.md">Projection</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/POISEUILLE.md">Poiseuille</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/VALIDATION.md">Validation</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon">Release</a>
    </p>
    <div class="videos">
'''
    
    for video in VIDEO_SOURCES:
        html_content += f'''        <div class="video-card">
            <div class="video-title">{video['name']}</div>
            <div class="video-description">{video['description']}</div>
            <video controls>
                <source src="https://github.com/{REPO}/releases/download/{TAG}/{video['release_name']}" type="video/mp4">
                Your browser does not support video playback.
            </video>
            <p><a href="https://github.com/{REPO}/releases/download/{TAG}/{video['release_name']}">Download Video</a></p>
        </div>\n'''
    
    html_content += '''    </div>
</body>
</html>'''
    
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Gallery HTML written to {output_path}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", default=DEFAULT_BASE_PATH)
    parser.add_argument("--yes", action="store_true", help="Generate gallery without prompting")
    args = parser.parse_args()
    
    print("="*70)
    print("POLYMATHICA Video Organization Tool")
    print("="*70 + "\n")
    
    # Verify videos
    print("Checking video files...\n")
    base_path = args.base_path
    
    results = verify_videos(base_path)
    
    found = 0
    missing = 0
    
    for name, exists, path in results:
        status = "FOUND" if exists else "MISSING"
        print(f"{status:12s} {name}")
        if exists:
            size_mb = os.path.getsize(path) / (1024**2)
            print(f"              Size: {size_mb:.1f} MB")
            found += 1
        else:
            missing += 1
    
    print(f"\nTotal: {found} found, {missing} missing\n")
    
    if found > 0:
        copied = prepare_release_assets(base_path)
        print(f"Prepared {len(copied)} release assets in {RELEASE_ASSET_DIR}\n")
        print_upload_commands()

        should_generate = args.yes
        if not should_generate:
            print("\nGenerate HTML gallery? (y/n): ", end="")
            should_generate = input().lower() == 'y'
        if should_generate:
            generate_html_gallery("index.html")
            generate_html_gallery("docs/index.html")
            generate_html_gallery("docs/assets/video-gallery.html")
    
    print("\n" + "="*70)
    print("Next Steps:")
    print("1. Copy-paste the upload commands above")
    print(f"2. Run: gh release create {TAG} ...")
    print(f"3. Run: gh release upload {TAG} ...")
    print("4. Videos will appear on GitHub Releases page")
    print("="*70)

if __name__ == "__main__":
    main()
