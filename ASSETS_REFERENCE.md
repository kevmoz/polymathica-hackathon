# POLYMATHICA Assets Reference

## Video Assets Location

Video assets for POLYMATHICA are stored on local drive: **D:\**

### Expected Directory Structure

```
D:\
├── polymathica/
│   ├── video/
│   │   ├── system_overview/
│   │   │   └── polymathica_intro.mp4
│   │   ├── tutorials/
│   │   │   ├── getting_started.mp4
│   │   │   ├── running_simulation.mp4
│   │   │   └── analyzing_results.mp4
│   │   ├── demonstrations/
│   │   │   ├── cfd_demo.mp4
│   │   │   ├── pde_solver_demo.mp4
│   │   │   └── visualization_demo.mp4
│   │   └── case_studies/
│   │       ├── turbulent_flow.mp4
│   │       ├── heat_transfer.mp4
│   │       └── multiphase_flow.mp4
│   ├── images/
│   │   ├── diagrams/
│   │   ├── screenshots/
│   │   └── results/
│   └── data/
│       ├── reference_solutions/
│       ├── benchmark_data/
│       └── test_datasets/
```

## Integration with Repository

### Video Integration Path

In documentation and README files, reference videos using:

```markdown
**Note**: Video demonstrations available at `D:/polymathica/video/`

- [System Overview](D:/polymathica/video/system_overview/polymathica_intro.mp4)
- [Tutorials](D:/polymathica/video/tutorials/)
- [Demonstrations](D:/polymathica/video/demonstrations/)
```

### Asset Linking in Code

For documentation generation:

```python
VIDEO_ASSETS_PATH = "D:/polymathica/video/"
IMAGE_ASSETS_PATH = "D:/polymathica/images/"
DATA_ASSETS_PATH = "D:/polymathica/data/"
```

## Asset Organization

### Video Assets
- **system_overview/**: Introduction and system architecture videos
- **tutorials/**: Step-by-step usage tutorials
- **demonstrations/**: Feature demonstrations and use cases
- **case_studies/**: Real experimental demonstrations

### Image Assets
- **diagrams/**: Architecture and workflow diagrams
- **screenshots/**: UI and interface screenshots
- **results/**: Example simulation results and visualizations

### Data Assets
- **reference_solutions/**: Known-good results for validation
- **benchmark_data/**: Performance benchmarking datasets
- **test_datasets/**: Sample data for testing and tutorials

## Using Assets in Documentation

### Embedding Videos in Markdown

```markdown
# Example: Running a CFD Simulation

Watch this video to learn how to set up and run a simulation:

[![CFD Demo Video](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](D:/polymathica/video/demonstrations/cfd_demo.mp4)

Or view at: `D:/polymathica/video/demonstrations/cfd_demo.mp4`
```

### Publishing to GitHub

When publishing documentation to GitHub:
1. Export videos to MP4 format if not already
2. For online documentation, consider uploading to GitHub Releases
3. Maintain local copy in D: for development reference

## Maintenance

- Keep assets organized and up-to-date
- Version control video metadata and descriptions
- Archive old versions in subfolder
- Document asset creation dates and sources
