from typing import Optional, Dict

from .base_exporter import BaseExporter
from .exporters.tdod_exporter import ThreeDObjectDetectionExporter
from .exporters.tdseg_exporter import ThreeDSegmentationExporter
from .exporters.nuimages_exporter import NuImagesExporter

class ExportNuscenes(BaseExporter):
    """NuScenes格式导出主类"""
    
    def __init__(self, source_data, output_dir: str, sensor_mapping: Optional[Dict[int, str]] = None):
        super().__init__(source_data, output_dir, sensor_mapping)
        self.exporters = []
    
    def add_exporter(self, exporter):
        """添加导出策略"""
        self.exporters.append(exporter)
    
    def export(self) -> str:
        """执行导出"""
        sequences = self.moore_data.get('data', [])
        
        for seq_idx, sequence in enumerate(sequences):
            for exporter in self.exporters:
                exporter.process_sequence(sequence, seq_idx)
        
        for exporter in self.exporters:
            exporter.save_data()
        
        return self.output_dir