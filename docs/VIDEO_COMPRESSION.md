# Video Compression

Use this when release assets or GitHub Pages media need smaller files without throwing away too much visible quality.

## Balanced HEVC Preset

Recommended settings:

- codec: H.265 / HEVC
- quality mode: constant quality
- RF / CRF: `20` to `24`
- default balance: `23`
- encoder preset: `slow`
- high-compression preset: `slower`

Lower CRF means higher quality and larger files. For most 1080p demos, `22` or `23` is the best first pass. Use `20` for near-source quality and `24` when file size matters more.

## Command

```bash
python scripts/organize_videos.py --yes --compress-hevc --hevc-crf 23 --hevc-preset slow
```

This keeps the normal release copies under `release_assets/` and writes HEVC versions beside them using `_hevc.mp4` filenames.

## Direct FFmpeg Equivalent

```bash
ffmpeg -i input.mp4 -c:v libx265 -crf 23 -preset slow -tag:v hvc1 -c:a aac -b:a 128k -movflags +faststart output.mp4
```

Use `-tag:v hvc1` for better Apple/Safari compatibility.

## Browser Note

HEVC is efficient, but H.264 still has broader browser compatibility. For judge-facing pages, keep an H.264 MP4 available when playback reliability matters, and use HEVC for smaller downloadable/release copies.
