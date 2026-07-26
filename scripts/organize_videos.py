#!/usr/bin/env python3
"""Organize and prepare videos for the GitHub Release."""

import argparse
import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

REPO = "kevmoz/polymathica-hackathon"
TAG = "v1.0.0-hackathon"
DEFAULT_BASE_PATH = r"D:\Polymathica\ACTIVE_REPO\runtime_outputs"
RELEASE_ASSET_DIR = Path("release_assets")
DEFAULT_HEVC_CRF = 23
DEFAULT_HEVC_PRESET = "slow"

RECENT_60S_VIDEO_SOURCES = [
    {
        "name": "01 - V534-G2R Room Capture (Narrated)",
        "path": "v534_g2r_room_capture/v534_g2r_room_capture_narrated.mp4",
        "release_name": "progress_01_v534_g2r_room_capture_narrated_60s.mp4",
        "description": "Latest full 60-second V534-G2R room capture with narration and upgraded graphics evidence.",
    },
    {
        "name": "02 - V534-G2R Room Capture (Silent)",
        "path": "v534_g2r_room_capture/v534_g2r_room_capture.mp4",
        "release_name": "progress_02_v534_g2r_room_capture_silent_60s.mp4",
        "description": "Latest full 60-second V534-G2R room capture without narration.",
    },
    {
        "name": "03 - V534 NS3D ABC Flow (Narrated)",
        "path": "v534_ns3d_abc_flow/v534-ns3d-abc-flow/run-v534-ns3d-abc-flow-001/rendering/v534_abc_flow_narrated.mp4",
        "release_name": "progress_03_v534_ns3d_abc_flow_narrated_60s.mp4",
        "description": "Newest full 60-second V534 3D Navier-Stokes ABC flow run with narration.",
    },
    {
        "name": "04 - V534 NS3D ABC Flow (Silent)",
        "path": "v534_ns3d_abc_flow/v534-ns3d-abc-flow/run-v534-ns3d-abc-flow-001/rendering/video_silent.mp4",
        "release_name": "progress_04_v534_ns3d_abc_flow_silent_60s.mp4",
        "description": "Newest full 60-second V534 3D Navier-Stokes ABC flow render without narration.",
    },
    {
        "name": "05 - V532 Periodic Vortex Interaction (Narrated)",
        "path": "v532_release_assets/v532-periodic-vortex-interaction-narrated.mp4",
        "release_name": "progress_05_v532_periodic_vortex_interaction_narrated_60s.mp4",
        "description": "Full 60-second V532 periodic vortex interaction run with narration.",
    },
    {
        "name": "06 - V532 Periodic Vortex Interaction (Silent)",
        "path": "v532_release_assets/v532-periodic-vortex-interaction-silent.mp4",
        "release_name": "progress_06_v532_periodic_vortex_interaction_silent_60s.mp4",
        "description": "Full 60-second V532 periodic vortex interaction render without narration.",
    },
]

LEGACY_VIDEO_SOURCES = [
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

VIDEO_SOURCES = RECENT_60S_VIDEO_SOURCES + LEGACY_VIDEO_SOURCES

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

def compress_hevc_balanced(
    source: Path,
    target: Path,
    *,
    crf: int = DEFAULT_HEVC_CRF,
    preset: str = DEFAULT_HEVC_PRESET,
) -> Path:
    """Create a balanced-size H.265/HEVC MP4 using constant quality."""
    if not 20 <= int(crf) <= 24:
        raise ValueError("Balanced HEVC CRF should stay between 20 and 24")
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(source),
        "-c:v",
        "libx265",
        "-crf",
        str(crf),
        "-preset",
        preset,
        "-tag:v",
        "hvc1",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-movflags",
        "+faststart",
        str(target),
    ]
    subprocess.run(cmd, check=True)
    return target


def prepare_release_assets(
    base_path: str,
    output_dir: Path = RELEASE_ASSET_DIR,
    *,
    compress_hevc: bool = False,
    hevc_crf: int = DEFAULT_HEVC_CRF,
    hevc_preset: str = DEFAULT_HEVC_PRESET,
) -> List[Path]:
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
        if compress_hevc:
            release_name = Path(video["release_name"])
            hevc_target = output_dir / f"{release_name.stem}_hevc{release_name.suffix}"
            compress_hevc_balanced(source, hevc_target, crf=hevc_crf, preset=hevc_preset)
            copied.append(hevc_target)
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
    output = Path(output_path)
    if output.as_posix() == "index.html":
        progress_doc = "docs/PROGRESS_2026_07_25.md"
        progress_video = "docs/assets/v533_cfd_room_showcase_silent.mp4"
        progress_poster = "docs/assets/v533_cfd_room_showcase_export.png"
    elif output.as_posix() == "docs/index.html":
        progress_doc = "PROGRESS_2026_07_25.md"
        progress_video = "assets/v533_cfd_room_showcase_silent.mp4"
        progress_poster = "assets/v533_cfd_room_showcase_export.png"
    else:
        progress_doc = "../PROGRESS_2026_07_25.md"
        progress_video = "v533_cfd_room_showcase_silent.mp4"
        progress_poster = "v533_cfd_room_showcase_export.png"

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
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/PROGRESS_2026_07_25.md">July 25 Progress</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/RECENT_60S_SHOWCASE.md">Recent 60s</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/blob/main/docs/VIDEO_COMPRESSION.md">Compression</a>
        <a href="https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon">Release</a>
    </p>
    <div class="videos">
'''

    for video in RECENT_60S_VIDEO_SOURCES:
        html_content += f'''        <div class="video-card">
            <div class="video-title">{video['name']}</div>
            <div class="video-description">{video['description']}</div>
            <video controls>
                <source src="https://github.com/{REPO}/releases/download/{TAG}/{video['release_name']}" type="video/mp4">
                Your browser does not support video playback.
            </video>
            <p><a href="https://github.com/{REPO}/releases/download/{TAG}/{video['release_name']}">Download Video</a></p>
        </div>\n'''

    html_content += f'''        <div class="video-card">
            <div class="video-title">July 25 CFD Room Progress</div>
            <div class="video-description">V533 operator-room capture with linked four-view CFD analysis, validated PNG/video export, and Taylor-Green reproducibility evidence.</div>
            <video controls poster="{progress_poster}">
                <source src="{progress_video}" type="video/mp4">
                Your browser does not support video playback.
            </video>
            <p><a href="{progress_doc}">Read Progress Evidence</a></p>
        </div>\n'''
    
    for video in LEGACY_VIDEO_SOURCES:
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
</html>
'''
    
    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Gallery HTML written to {output_path}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-path", default=DEFAULT_BASE_PATH)
    parser.add_argument("--yes", action="store_true", help="Generate gallery without prompting")
    parser.add_argument(
        "--compress-hevc",
        action="store_true",
        help="Also create balanced H.265/HEVC *_hevc.mp4 copies under release_assets",
    )
    parser.add_argument(
        "--hevc-crf",
        type=int,
        default=DEFAULT_HEVC_CRF,
        help="HEVC constant-quality RF/CRF value, balanced range 20-24; default 23",
    )
    parser.add_argument(
        "--hevc-preset",
        default=DEFAULT_HEVC_PRESET,
        choices=("medium", "slow", "slower"),
        help="HEVC encoder preset; slow/slower reduce file size at the same quality",
    )
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
        copied = prepare_release_assets(
            base_path,
            compress_hevc=args.compress_hevc,
            hevc_crf=args.hevc_crf,
            hevc_preset=args.hevc_preset,
        )
        print(f"Prepared {len(copied)} release assets in {RELEASE_ASSET_DIR}\n")
        if args.compress_hevc:
            print(
                "Balanced HEVC *_hevc.mp4 copies written to "
                f"{RELEASE_ASSET_DIR} with CRF {args.hevc_crf} and preset {args.hevc_preset}\n"
            )
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
    print("5. Optional size reduction: rerun with --compress-hevc --hevc-crf 22 --hevc-preset slow")
    print("="*70)

if __name__ == "__main__":
    main()
