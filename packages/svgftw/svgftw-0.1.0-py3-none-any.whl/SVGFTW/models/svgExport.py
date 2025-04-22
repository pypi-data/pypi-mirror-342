import subprocess
import tempfile
from pathlib import Path
from typing import Optional

# Static exports
try:
    import cairosvg
    import cairocffi as cairo
except ImportError:
    cairosvg = None

try:
    import skia
except ImportError:
    skia = None

# Animated exports
try:
    import imageio
    from timecut import get_recorder
except ImportError:
    imageio = None

# Hardware acceleration
try:
    import cupy as cp
except ImportError:
    cp = None

class SVGExporter:
    def __init__(self, svg_data: str, use_gpu: bool = False):
        self.svg_data = svg_data
        self.use_gpu = use_gpu
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def _cairo_export(self, output_path: str, fmt: str, dpi: int = 300):
        """Base Cairo export function"""
        if fmt == 'png':
            cairosvg.svg2png(bytestring=self.svg_data, write_to=output_path, dpi=dpi)
        elif fmt == 'pdf':
            cairosvg.svg2pdf(bytestring=self.svg_data, write_to=output_path)
        else:
            raise ValueError(f"Unsupported format: {fmt}")

    def _skia_export(self, output_path: str, size: tuple[int, int]):
        """GPU-accelerated export using Skia"""
        stream = skia.Stream.MakeFromCopy(self.svg_data.encode('utf-8'))
        svg = skia.SVGDOM.MakeFromStream(stream)
        surface = skia.Surface(size[0], size[1])
        with surface as canvas:
            canvas.scale(size[0]/svg.containerSize().x(), 
                        size[1]/svg.containerSize().y())
            svg.render(canvas)
        surface.makeImageSnapshot().save(output_path)

    def export_static(self, output_path: str, 
                     size: tuple[int, int] = (1024, 768), 
                     dpi: int = 300):
        """Export to static formats (SVG, PNG, PDF)"""
        fmt = Path(output_path).suffix[1:].lower()
        
        if fmt == 'svg':
            Path(output_path).write_text(self.svg_data)
            return

        if self.use_gpu and skia:
            self._skia_export(output_path, size)
        elif cairosvg:
            self._cairo_export(output_path, fmt, dpi)
        else:
            raise RuntimeError("No suitable rendering backend found")

    def export_animated(self, output_path: str, 
                       duration: float = 5.0,
                       fps: int = 30):
        """Export to animated formats (GIF, MP4)"""
        fmt = Path(output_path).suffix[1:].lower()
        
        with tempfile.NamedTemporaryFile(suffix='.html') as f:
            f.write(f"""
            <!DOCTYPE html>
            <html><body style="margin:0">
                <div id="container" style="width:{1024}px;height:{768}px">
                    {self.svg_data}
                </div>
            </body></html>
            """.encode())
            f.flush()

            ffmpeg_args = ['-vf', f'fps={fps}']
            if self.use_gpu and fmt == 'mp4':
                ffmpeg_args += ['-c:v', 'h264_nvenc', '-preset', 'fast']

            recorder = get_recorder(
                x=0, y=0, width=1024, height=768,
                input_path=f.name,
                output_path=output_path,
                fps=fps,
                duration=duration,
                frame_processor=FrameProcessor() if fmt == 'gif' else None,
                ffmpeg_args=ffmpeg_args
            )
            recorder.start()

    def __del__(self):
        self.temp_dir.cleanup()

class FrameProcessor:
    """Post-process frames for GIF optimization"""
    def __init__(self):
        self.frames = []

    def process_frame(self, frame):
        if cp:  # GPU acceleration with CuPy
            frame = cp.asarray(frame)
            frame = cp.clip(frame * 1.2, 0, 255).astype(cp.uint8)
            frame = cp.asnumpy(frame)
        self.frames.append(frame)

    def finalize(self, output_path):
        imageio.mimsave(output_path, self.frames, fps=30, 
                       subrectangles=True, optimize=True)

# Usage example
if __name__ == "__main__":
    svg_content = Path("input.svg").read_text()
    
    exporter = SVGExporter(svg_content, use_gpu=True)
    
    # Static exports
    exporter.export_static("output.png")
    exporter.export_static("output.pdf")
    
    # Animated exports
    exporter.export_animated("output.gif")
    exporter.export_animated("output.mp4")
