import numpy as np
from .utils import THEMES

class BaseSeries:
    def __init__(self, x, y=None, color=None, label=None):
        self.x = x
        self.y = y
        self.color = color or "#1f77b4"
        self.label = label

class LineSeries(BaseSeries):
    def __init__(self, x, y, color=None, label=None, linestyle="solid", width=2):
        super().__init__(x, y, color, label)
        self.linestyle = linestyle
        self.width = width

    def to_svg(self, ax, use_y2=False):
        scale_y = ax.scale_y2 if use_y2 else ax.scale_y
        dash = {"solid": "", "dashed": "6,3", "dotted": "2,2", "longdash": "10,5"}.get(self.linestyle, "")
        polyline = " ".join(f"{ax.scale_x(x)},{scale_y(y)}" for x, y in zip(self.x, self.y))
        svg = f'<polyline fill="none" stroke="{self.color}" stroke-width="{self.width}" stroke-dasharray="{dash}" points="{polyline}"/>'
        tooltip_points = [
            f'<circle class="glyphx-point" cx="{ax.scale_x(x)}" cy="{scale_y(y)}" r="4" fill="{self.color}" data-x="{x}" data-y="{y}" data-label="{self.label or ""}"/>'
            for x, y in zip(self.x, self.y)
        ]
        return "\n".join([svg] + tooltip_points)

class BarSeries(BaseSeries):
    def __init__(self, x, y, color=None, label=None, bar_width=0.8):
        super().__init__(x, y, color, label)
        self.bar_width = bar_width

    def to_svg(self, ax, use_y2=False):
        scale_y = ax.scale_y2 if use_y2 else ax.scale_y
        elements = []
        px_width = (ax.width - 2 * ax.padding) * self.bar_width / len(self.x)
        for i, (x, y) in enumerate(zip(self.x, self.y)):
            cx = ax.scale_x(x)
            cy = scale_y(y)
            y0 = scale_y(0)
            h = abs(y0 - cy)
            top = min(y0, cy)
            tooltip = f'data-x="{x}" data-y="{y}" data-label="{self.label or ""}"'
            elements.append(f'<rect class="glyphx-point" x="{cx - px_width/2}" y="{top}" width="{px_width}" height="{h}" fill="{self.color}" stroke="#000" {tooltip}/>')
        return "\n".join(elements)

class ScatterSeries(BaseSeries):
    def __init__(self, x, y, color=None, label=None, size=5, marker="circle"):
        super().__init__(x, y, color, label)
        self.size = size
        self.marker = marker

    def to_svg(self, ax, use_y2=False):
        scale_y = ax.scale_y2 if use_y2 else ax.scale_y
        elements = []
        for x, y in zip(self.x, self.y):
            px = ax.scale_x(x)
            py = scale_y(y)
            tooltip = f'data-x="{x}" data-y="{y}" data-label="{self.label or ""}"'
            if self.marker == "square":
                elements.append(f'<rect class="glyphx-point" x="{px - self.size/2}" y="{py - self.size/2}" width="{self.size}" height="{self.size}" fill="{self.color}" {tooltip}/>')
            else:
                elements.append(f'<circle class="glyphx-point" cx="{px}" cy="{py}" r="{self.size}" fill="{self.color}" {tooltip}/>')
        return "\n".join(elements)

class PieSeries(BaseSeries):
    def __init__(self, values, labels=None, colors=None, radius=100, center=(150,150)):
        self.values = values
        self.labels = labels or [f"Slice {i}" for i in range(len(values))]
        self.colors = colors or ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
        self.radius = radius
        self.center = center

    def to_svg(self, ax=None, use_y2=False):
        import math
        total = sum(self.values)
        svg = []
        cx, cy = self.center
        angle = 0
        for i, v in enumerate(self.values):
            theta = 2 * math.pi * v / total
            x1 = cx + self.radius * math.cos(angle)
            y1 = cy + self.radius * math.sin(angle)
            x2 = cx + self.radius * math.cos(angle + theta)
            y2 = cy + self.radius * math.sin(angle + theta)
            large_arc = 1 if theta > math.pi else 0
            path = f"M {cx},{cy} L {x1},{y1} A {self.radius},{self.radius} 0 {large_arc},1 {x2},{y2} Z"
            color = self.colors[i % len(self.colors)]
            label = self.labels[i] if i < len(self.labels) else f"Slice {i}"
            svg.append(f'<path class="glyphx-point" d="{path}" fill="{color}" stroke="#fff" data-label="{label}" data-value="{v}"/>')
            angle += theta
        return "\n".join(svg)

class DonutSeries(PieSeries):
    def __init__(self, values, labels=None, colors=None, radius=100, inner_radius=40, center=(150,150)):
        super().__init__(values, labels, colors, radius, center)
        self.inner_radius = inner_radius

    def to_svg(self, ax=None, use_y2=False):
        import math
        total = sum(self.values)
        svg = []
        cx, cy = self.center
        angle = 0
        for i, v in enumerate(self.values):
            theta = 2 * math.pi * v / total
            x1 = cx + self.radius * math.cos(angle)
            y1 = cy + self.radius * math.sin(angle)
            x2 = cx + self.radius * math.cos(angle + theta)
            y2 = cy + self.radius * math.sin(angle + theta)
            x3 = cx + self.inner_radius * math.cos(angle + theta)
            y3 = cy + self.inner_radius * math.sin(angle + theta)
            x4 = cx + self.inner_radius * math.cos(angle)
            y4 = cy + self.inner_radius * math.sin(angle)
            large_arc = 1 if theta > math.pi else 0
            path = f"M {x1},{y1} A {self.radius},{self.radius} 0 {large_arc},1 {x2},{y2} "
            path += f"L {x3},{y3} A {self.inner_radius},{self.inner_radius} 0 {large_arc},0 {x4},{y4} Z"
            color = self.colors[i % len(self.colors)]
            label = self.labels[i] if i < len(self.labels) else f"Slice {i}"
            svg.append(f'<path class="glyphx-point" d="{path}" fill="{color}" stroke="#fff" data-label="{label}" data-value="{v}"/>')
            angle += theta
        return "\n".join(svg)

class HistogramSeries(BaseSeries):
    def __init__(self, data, bins=10, color=None, label=None):
        hist, edges = np.histogram(data, bins=bins)
        x = [(edges[i] + edges[i+1]) / 2 for i in range(len(hist))]
        y = hist.tolist()
        super().__init__(x, y, color or "#1f77b4", label)
        self.edges = edges

    def to_svg(self, ax, use_y2=False):
        scale_y = ax.scale_y2 if use_y2 else ax.scale_y
        elements = []
        width = (ax.scale_x(self.edges[1]) - ax.scale_x(self.edges[0])) * 0.9
        for x, y in zip(self.x, self.y):
            cx = ax.scale_x(x)
            cy = scale_y(y)
            y0 = scale_y(0)
            h = abs(y0 - cy)
            top = min(y0, cy)
            tooltip = f'data-x="{x}" data-y="{y}" data-label="{self.label or ""}"'
            elements.append(f'<rect class="glyphx-point" x="{cx - width/2}" y="{top}" width="{width}" height="{h}" fill="{self.color}" {tooltip}/>')
        return "\n".join(elements)

class BoxPlotSeries(BaseSeries):
    def __init__(self, data, color="#1f77b4", label=None, width=20):
        self.data = np.array(data)
        self.color = color
        self.label = label
        self.width = width

    def to_svg(self, ax, use_y2=False):
        q1 = np.percentile(self.data, 25)
        q2 = np.percentile(self.data, 50)
        q3 = np.percentile(self.data, 75)
        iqr = q3 - q1
        whisker_low = max(min(self.data), q1 - 1.5 * iqr)
        whisker_high = min(max(self.data), q3 + 1.5 * iqr)
        center_x = ax.scale_x(0.5)
        scale_y = ax.scale_y2 if use_y2 else ax.scale_y
        tooltip = f'data-label="{self.label or ""}" data-q1="{q1}" data-q2="{q2}" data-q3="{q3}"'
        elements = [
            f'<line x1="{center_x}" x2="{center_x}" y1="{scale_y(whisker_low)}" y2="{scale_y(q1)}" stroke="{self.color}"/>',
            f'<line x1="{center_x}" x2="{center_x}" y1="{scale_y(q3)}" y2="{scale_y(whisker_high)}" stroke="{self.color}"/>',
            f'<rect class="glyphx-point" x="{center_x - self.width/2}" y="{scale_y(q3)}" width="{self.width}" height="{abs(scale_y(q3)-scale_y(q1))}" fill="{self.color}" fill-opacity="0.4" stroke="{self.color}" {tooltip}/>',
            f'<line x1="{center_x - self.width/2}" x2="{center_x + self.width/2}" y1="{scale_y(q2)}" y2="{scale_y(q2)}" stroke="{self.color}" stroke-width="2"/>'
        ]
        return "\n".join(elements)

class HeatmapSeries(BaseSeries):
    def __init__(self, matrix, cmap=None, **kwargs):
        self.matrix = matrix
        self.cmap = cmap or ["#fff", "#ccc", "#999", "#666", "#333"]
        self.kwargs = kwargs

    def to_svg(self, ax, use_y2=False):
        import numpy as np
        svg = []
        rows, cols = len(self.matrix), len(self.matrix[0])
        cw = (ax.width - 2 * ax.padding) / cols
        ch = (ax.height - 2 * ax.padding) / rows
        flat = [v for row in self.matrix for v in row]
        vmin, vmax = min(flat), max(flat)
        for i, row in enumerate(self.matrix):
            for j, val in enumerate(row):
                norm = int((val - vmin) / (vmax - vmin) * (len(self.cmap) - 1))
                color = self.cmap[norm]
                x = ax.padding + j * cw
                y = ax.padding + i * ch
                svg.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" fill="{color}" />')
        return "\n".join(svg)
