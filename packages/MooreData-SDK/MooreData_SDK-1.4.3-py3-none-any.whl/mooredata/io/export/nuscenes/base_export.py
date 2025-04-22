import os
import uuid
from typing import Optional, Dict


class BaseExporter:
    """基础导出类，包含所有导出格式通用的功能"""
    
    def __init__(self, source_data, output_dir: str, sensor_mapping: Optional[Dict[int, str]] = None):
        self.moore_data = source_data
        self.output_dir = output_dir
        if self.output_dir is None:
            self.output_dir = os.path.join(os.getcwd(), 'nuscenes')
        self.label_map = {}
        self.attribute_map = {}
        self.camera_sensors = []
        self.sample_data_tokens = {}
        self.sensor_mapping = sensor_mapping
        if self.sensor_mapping is None:
            self._get_sensor_mapping_from_moore()
        self.category_mapping = {}
        
        os.makedirs(output_dir, exist_ok=True)
    
    def _generate_token(self) -> str:
        """生成唯一的token"""
        return str(uuid.uuid4())
    
    def _get_sensor_mapping_from_moore(self):
        """从Moore格式JSON中获取传感器映射"""
        self.sensor_mapping = {}
        
        fusion_config = []
        if 'task' in self.moore_data and 'setting' in self.moore_data['task']:
            if 'toolSetting' in self.moore_data['task']['setting']:
                if 'fusionConfig' in self.moore_data['task']['setting']['toolSetting']:
                    fusion_config = self.moore_data['task']['setting']['toolSetting']['fusionConfig']
        
        num_cameras = 0
        if 'data' in self.moore_data and len(self.moore_data['data']) > 0:
            if 'info' in self.moore_data['data'][0] and 'info' in self.moore_data['data'][0]['info']:
                if 'imgUrls' in self.moore_data['data'][0]['info']['info'] and len(self.moore_data['data'][0]['info']['info']['imgUrls']) > 0:
                    num_cameras = len(self.moore_data['data'][0]['info']['info']['imgUrls'][0])
        
        if fusion_config and len(fusion_config) == num_cameras:
            for i, config in enumerate(fusion_config):
                sensor_name = config.get('name', f'CAM_{i+1}')
                self.sensor_mapping[i] = sensor_name
                self.camera_sensors.append(sensor_name)
        else:
            for i in range(num_cameras):
                sensor_name = f'CAM_{i+1}'
                
                self.sensor_mapping[i] = sensor_name
                self.camera_sensors.append(sensor_name)
        
        print(f"传感器映射: {self.sensor_mapping}")
    
    def _create_label_map(self):
        """创建标签映射"""
        label_configs = self.moore_data['task']['setting']['labelConfig']
        
        for idx, config in enumerate(label_configs):
            label_name = config['label']
            label_key = config.get('key', f'label_{idx}')
            
            english_name = label_name
            if 'labelAlias' in self.moore_data['task']['setting']:
                for alias in self.moore_data['task']['setting']['labelAlias']:
                    if label_key in alias:
                        english_name = alias[label_key].get('label', label_name)
            
            self.label_map[label_key] = {
                'name': label_name,
                'english_name': english_name,
                'color': config.get('color', '#FFFFFF'),
                'attributes': []
            }
            
            if 'attributes' in config:
                for attr_idx, attr in enumerate(config['attributes']):
                    attr_name = attr['label']
                    attr_key = f"{label_key}_{attr_idx}"
                    
                    self.attribute_map[attr_key] = {
                        'name': attr_name,
                        'values': []
                    }
                    
                    if 'children' in attr:
                        for child_idx, child in enumerate(attr['children']):
                            child_name = child['label']
                            child_key = f"{attr_key}_{child_idx}"
                            
                            self.attribute_map[attr_key]['values'].append({
                                'key': child_key,
                                'name': child_name
                            })
                            
                    self.label_map[label_key]['attributes'].append(attr_key)
    
    def _create_categories(self):
        """创建类别数据"""
        label_configs = self.moore_data['task']['setting']['labelConfig']
        
        for label_config in label_configs:
            if 'label' in label_config:
                label_name = label_config['label']
                
                category_token = self._generate_token()
                category = {
                    'token': category_token,
                    'name': label_name,
                    'description': label_name
                }
                
                self.nuscenes_data['category'].append(category)
                
                self.category_mapping[label_name] = category_token
        
        print(f"创建了 {len(self.nuscenes_data['category'])} 个类别")
    
    def _create_nuscenes_attributes(self):
        """创建NuScenes属性数据"""
        if 'task' in self.moore_data and 'setting' in self.moore_data['task'] and 'labelConfig' in self.moore_data['task']['setting']:
            label_configs = self.moore_data['task']['setting']['labelConfig']
            
            for label_config in label_configs:
                label_name = label_config.get('label', '')
                attributes = label_config.get('attributes', [])
                
                self._generate_attribute_combinations(label_name, attributes, [])
        
        if not self.nuscenes_data['attribute']:
            self._create_default_attributes()
        
        print(f"创建了 {len(self.nuscenes_data['attribute'])} 个属性")
    
    def _generate_attribute_combinations(self, label_name, attributes, current_path):
        """生成所有可能的属性组合"""
        if not attributes:
            if current_path:
                attr_name = f"{label_name}." + ".".join(current_path)
                attr_token = self._generate_token()
                attr = {
                    'token': attr_token,
                    'name': attr_name,
                    'description': f"Attribute {attr_name}"
                }
                self.nuscenes_data['attribute'].append(attr)
                self.attribute_map[attr_name] = attr_token
            return
        
        current_attr = attributes[0]
        attr_label = current_attr.get('label', '')
        children = current_attr.get('children', [])
        
        if not children:
            self._generate_attribute_combinations(label_name, attributes[1:], current_path)
            return
        
        for child in children:
            child_label = child.get('label', '')
            new_path = current_path + [child_label]
            
            if len(attributes) > 1:
                self._generate_attribute_combinations(label_name, attributes[1:], new_path)
            else:
                attr_name = f"{label_name}." + ".".join(new_path)
                attr_token = self._generate_token()
                attr = {
                    'token': attr_token,
                    'name': attr_name,
                    'description': f"Attribute {attr_name}"
                }
                self.nuscenes_data['attribute'].append(attr)
                self.attribute_map[attr_name] = attr_token
                
    def _create_default_attributes(self):
        """创建默认的NuScenes属性"""
        default_attributes = [
            'vehicle.moving', 'vehicle.parked', 'vehicle.stopped',
            'cycle.with_rider', 'cycle.without_rider',
            'pedestrian.moving', 'pedestrian.standing', 'pedestrian.sitting'
        ]
        
        for attr_name in default_attributes:
            attr_token = self._generate_token()
            attr = {
                'token': attr_token,
                'name': attr_name,
                'description': f"Attribute {attr_name}"
            }
            self.nuscenes_data['attribute'].append(attr)
            self.attribute_map[attr_name] = attr_token
            
    def _create_nuscenes_visibility(self):
        """创建NuScenes可见性数据"""
        visibility_levels = [
            {'level': "v0-40", 'token': '1', 'description': '0-40% 可见'},
            {'level': "v40-60", 'token': '2', 'description': '40-60% 可见'},
            {'level': "v60-80", 'token': '3', 'description': '60-80% 可见'},
            {'level': "v80-100", 'token': '4', 'description': '80-100% 可见'}
        ]
        
        for vis in visibility_levels:
            visibility = {
                'token': vis['token'],
                'level': vis['level'],
                'description': vis['description']
            }
            self.nuscenes_data['visibility'].append(visibility)
    
    def _get_or_create_instance(self, label_id: str, label_name: str) -> str:
        """获取或创建实例"""
        for instance in self.nuscenes_data['instance']:
            if instance.get('instance_id') == label_id:
                return instance['token']
        
        category_token = self._get_category_token(label_name)
        instance_token = self._generate_token()
        instance = {
            'token': instance_token,
            'category_token': category_token,
            'nbr_annotations': 1,
            'first_annotation_token': '',
            'last_annotation_token': '',
            'instance_id': label_id
        }
        
        self.nuscenes_data['instance'].append(instance)
        return instance_token
    
    def _get_category_token(self, label_name: str) -> str:
        """获取或创建类别"""
        for category in self.nuscenes_data['category']:
            if category['name'] == label_name:
                return category['token']
        
        category_token = self._generate_token()
        category = {
            'token': category_token,
            'name': label_name,
            'description': f"Category {label_name}"
        }
        
        self.nuscenes_data['category'].append(category)
        return category_token
    
    def _get_visibility_token(self, level: int) -> str:
        """获取或创建可见性级别"""
        for visibility in self.nuscenes_data['visibility']:
            if visibility['token'] == str(level):
                return visibility['token']
        
        visibility_token = str(level)
        visibility = {
            'token': str(level),
            'level': 'v80-100',
            'description': f"Visibility level {level}"
        }
        
        self.nuscenes_data['visibility'].append(visibility)
        return visibility_token
    
    def _get_attribute_order_for_label(self, label_name: str) -> List[str]:
        """
        获取指定标签的属性顺序
        
        Args:
            label_name: 标签名称
            
        Returns:
            属性键的有序列表
        """
        if 'task' in self.moore_data and 'setting' in self.moore_data['task'] and 'labelConfig' in self.moore_data['task']['setting']:
            label_configs = self.moore_data['task']['setting']['labelConfig']
            
            for label_config in label_configs:
                if label_config.get('label') == label_name:
                    attr_order = []
                    for attr in label_config.get('attributes', []):
                        attr_order.append(attr.get('label', ''))
                    return attr_order
        
        return []
    
    def _get_sample_timestamp(self, sample_token: str) -> int:
        """获取样本的时间戳"""
        for sample in self.nuscenes_data['sample']:
            if sample['token'] == sample_token:
                return sample['timestamp']
        return 0
    