# POLYMATHICA Video Manifest

## Real Video Assets from D: Drive

This manifest maps the actual POLYMATHICA videos for judge evaluation.

### Primary Video Sources

**Base Location**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\`

#### 1. System Overview & Cinematic Reel

**File**: `v493_60s_cinematic_reel/polymathica_60s_cinematic.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\v493_60s_cinematic_reel\polymathica_60s_cinematic.mp4`  
**Duration**: ~60 seconds  
**Content**: High-level system overview, architecture visualization, key features

---

#### 2. Navier-Stokes Simulation Demo

**File**: `v482_ns_cinematic_video/polymathica_navier_stokes_cinematic.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\v482_ns_cinematic_video\polymathica_navier_stokes_cinematic.mp4`  
**Duration**: Variable  
**Content**: Real Navier-Stokes simulation execution, velocity fields, pressure contours

---

#### 3. Advanced Visualization & Post-Effects

**File**: `v478_postfx_export/polymathica_postfx_reel.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\v478_postfx_export\polymathica_postfx_reel.mp4`  
**Duration**: Variable  
**Content**: Graphics Core rendering, post-processing effects, visualization modes

---

#### 4. NS Reel (Simulation Results)

**File**: `v477_video_export/polymathica_ns_reel.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\v477_video_export\polymathica_ns_reel.mp4`  
**Duration**: Variable  
**Content**: Complete Navier-Stokes simulation results, evidence visualization

---

#### 5. 3D NS with GPU Acceleration (CUDA/NVENC)

**File**: `governed_graphics_core/ns3d-v64-cuda-nvenc-60s/run-v64-60s-001/video.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\governed_graphics_core\ns3d-v64-cuda-nvenc-60s\run-v64-60s-001\video.mp4`  
**Duration**: 60 seconds  
**Content**: 3D Navier-Stokes with real-time GPU rendering (CUDA), production-quality video

---

#### 6. Lid-Driven Cavity Replay (2D Sharp)

**File**: `v525_operational_recovery/ns2d/V526-NS2D-SHARP-001/v525_ns2d_lid_replay.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\v525_operational_recovery\ns2d\V526-NS2D-SHARP-001\v525_ns2d_lid_replay.mp4`  
**Duration**: Variable  
**Content**: 2D lid-driven cavity simulation replay, validation demo

---

#### 7. Lab Workspace Simulation

**File**: `ns_lab/1096fbff-0419-468b-be9d-d550e53098c4/simulation.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\ns_lab\1096fbff-0419-468b-be9d-d550e53098c4\simulation.mp4`  
**Duration**: Variable  
**Content**: Complete simulation workflow with monitoring

---

#### 8. July 25 CFD Room Progress Capture

**File**: `v533_cfd_room_showcase/v533-cfd-room-showcase/run-v533-cfd-room-showcase-001/v533_cfd_room_showcase_silent.mp4`  
**Path**: `D:\Polymathica\ACTIVE_REPO\runtime_outputs\v533_cfd_room_showcase\v533-cfd-room-showcase\run-v533-cfd-room-showcase-001\v533_cfd_room_showcase_silent.mp4`  
**Public copy**: `docs/assets/v533_cfd_room_showcase_silent.mp4`  
**Still image**: `docs/assets/v533_cfd_room_showcase_export.png`  
**Date**: 2026-07-25  
**Content**: V533 operator-room capture with linked four-view CFD analysis, field selection, timeline scrubbing, theme switching and validated PNG/video export.

Related source evidence:

- `capture_validation.json`: `validation_status=passed`
- `room_state_manifest.json`: linked source frames and room actions
- `CMP-20260725-223914-d2742d`: Taylor-Green reproducibility comparison
- source runs: `CFD-20260725-223859-a6e661` and `CFD-20260725-223906-62d046`

---

### Backup & Additional Sources

**Graphics Core Review**:  
`D:\Polymathica_Graphics_Core_review\v64a\real_video.mp4`

**Graphics Core Proof**:  
`D:\tmp\Graphics_Core_V64_NS3D_Proof\video.mp4`

**Backup Storage**:  
`D:\Polymathica_Backups\...` (for long-term archival)

---

## Recommended Selection for Judges

### Quick Showcase (5 min total)
1. **System Overview** → `v493_60s_cinematic_reel/polymathica_60s_cinematic.mp4` (60s)
2. **Live Simulation** → `governed_graphics_core/ns3d-v64-cuda-nvenc-60s/run-v64-60s-001/video.mp4` (60s)
3. **Results Demo** → `v477_video_export/polymathica_ns_reel.mp4` (3 min)

### Complete Showcase (15 min)
1. Cinematic overview (60s)
2. NS simulation (5 min)
3. Graphics rendering (3 min)
4. Results/validation (3 min)
5. Workflow summary (3 min)
6. July 25 V533 CFD room progress capture (operator-room proof)

---

## Integration with GitHub

### Step 1: Create GitHub Release

```bash
gh release create v1.0.0-hackathon \
  --title "POLYMATHICA Hackathon Submission" \
  --notes "Complete autonomous scientific laboratory with real simulations" \
  --repo kevmoz/polymathica-hackathon
```

### Step 2: Upload Videos

```bash
cd D:\Polymathica\polymathica-hackathon

gh release upload v1.0.0-hackathon \
  release_assets/polymathica_60s_cinematic.mp4 \
  release_assets/polymathica_ns_cinematic.mp4 \
  release_assets/polymathica_graphics_core_postfx.mp4 \
  release_assets/polymathica_ns_results.mp4 \
  release_assets/polymathica_3d_gpu_cuda_60s.mp4 \
  release_assets/polymathica_2d_validation_replay.mp4 \
  release_assets/polymathica_lab_workflow.mp4 \
  --repo kevmoz/polymathica-hackathon --clobber
```

### Step 3: Update Video Gallery

All videos will be available at:  
`https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon`

Embedded on GitHub Pages gallery with direct download links.

---

## Video Quality Metrics

**Expected Specifications**:
- Codec: H.264 (MP4)
- Resolution: 1920×1080 (Full HD) or 3840×2160 (4K)
- Frame Rate: 30fps or 60fps
- Bitrate: 3000-8000 kbps
- Audio: AAC stereo (if present)

---

## File Organization in Submission

```
GitHub Release: v1.0.0-hackathon
├── polymathica_60s_cinematic.mp4 (System Overview)
├── polymathica_ns_cinematic.mp4 (NS Demo)
├── polymathica_graphics_core_postfx.mp4 (Graphics Core)
├── polymathica_ns_reel.mp4 (Results)
├── polymathica_3d_gpu_cuda_60s.mp4 (3D CUDA/NVENC - 60s)
├── polymathica_2d_validation_replay.mp4 (2D Validation)
├── polymathica_lab_workflow.mp4 (Lab Workflow)
└── README with playback instructions
```

---

## Judge Viewing Experience

### Via GitHub Pages

Visit: `https://kevmoz.github.io/polymathica-hackathon`

**Video Gallery Features**:
- Embedded HTML5 player for each video
- Direct links to GitHub Release downloads
- Play buttons and preview thumbnails
- Video descriptions and timestamps
- Automatic fallback if player unavailable

### Direct Download

All videos available at Release:
`https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon`

---

## What Judges Will See

### Video 1: System Overview (60s)
- POLYMATHICA branding
- Architecture overview
- Key components (Olana, PSIC, Graphics Core)
- Feature highlights
- Call to action

### Video 2: Simulation Cinematic (Variable)
- Real Navier-Stokes computation
- Velocity field visualization
- Pressure contours
- Temperature evolution
- Real-time monitoring display

### Video 3: Graphics Core (Variable)
- Rendering pipeline demonstration
- Multiple visualization modes
- Post-processing effects
- Publication-quality output
- Real-time performance

### Video 4: Results & Validation (Variable)
- Complete simulation results
- Evidence visualization
- Quality metrics display
- Reproducibility verification
- Archive integration

### Video 5: 3D GPU-Accelerated (60s)
- 3D Navier-Stokes with CUDA
- Real-time GPU rendering (NVENC)
- High-resolution output
- Performance metrics
- Production-grade quality

### Video 6: 2D Validation (Variable)
- Lid-driven cavity benchmark
- Replay verification
- Convergence analysis
- Reference solution comparison
- Reproducibility evidence

### Video 7: Complete Workflow (Variable)
- End-to-end experiment
- Monitoring and progress
- All 13 workflow stages
- Evidence recording
- Publication export

---

## Next Steps

1. **Verify video files** exist at D: paths listed above
2. **Test video playback** locally before uploading
3. **Create GitHub Release** with v1.0.0-hackathon tag
4. **Upload all videos** to release
5. **Test GitHub Pages** gallery loads correctly
6. **Send judges** the gallery link

---

## Quality Assurance Checklist

Before uploading to GitHub:
- [ ] All video files located and accessible
- [ ] Videos play smoothly (no corruption)
- [ ] Audio is clear (if present)
- [ ] Resolution is acceptable (≥1080p)
- [ ] Aspect ratio correct (16:9)
- [ ] Content represents actual POLYMATHICA output
- [ ] No proprietary information exposed
- [ ] File sizes reasonable (<1GB each)
- [ ] Metadata intact (creation date, etc)

---

## Playback Instructions for Judges

**For Online Viewing**:
1. Visit GitHub Pages: https://kevmoz.github.io/polymathica-hackathon
2. Click video player or download link
3. Watch in browser or local player

**For Local Viewing**:
1. Go to Release page: https://github.com/kevmoz/polymathica-hackathon/releases/tag/v1.0.0-hackathon
2. Download video file
3. Play with local media player (VLC, QuickTime, etc)

**For Archival**:
1. Download all videos from Release
2. Store in judges' local archive
3. Always linked from GitHub for reference

---

**From experiment to evidence. From evidence to discovery.**

*POLYMATHICA — Governed Autonomous Scientific Laboratory*
