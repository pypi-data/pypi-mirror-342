#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import base64
import zlib
from scipy.spatial.transform import Rotation
from mooredata.utils.pc_tools import euler_to_quaternion
from mooredata.utils.general import download_file
from .base_export import BaseExporter


class ExportNuscenes(BaseExporter):
    """
    将Moore格式数据转换为NuScenes格式
    支持3D目标检测(3DOD)和LidarSeg格式
    """
    
    def __init__(self, source_data, output_dir: str, sensor_mapping: Optional[Dict[int, str]] = None):
        """
        初始化转换器
        
        Args:
            source_data: Moore格式数据
            output_dir: 输出NuScenes格式数据的目录
            sensor_mapping: 传感器映射，键为传感器索引，值为传感器名称
                           如果为None，则从Moore格式数据中获取
        """
        super().__init__(source_data, output_dir, sensor_mapping)
        # self.moore_data = source_data
        # self.output_dir = output_dir
        # if self.output_dir is None:
        #     self.output_dir = os.path.join(os.getcwd(), 'nuscenes')
        # self.label_map = {}  # 标签映射
        # self.attribute_map = {}  # 属性映射
        # self.camera_sensors = []  # 相机传感器列表
        # self.sample_data_tokens = {}  # 用于跟踪每个通道的样本数据token
        # self.sensor_mapping = sensor_mapping  # 传感器映射
        # self.category_mapping = {}  # 类别映射
        # if self.sensor_mapping is None:
        #     self._get_sensor_mapping_from_moore()
        self.lidarseg_category_map = {}
        self.nuscenes_data = {
            'category': [],
            'attribute': [],
            'visibility': [],
            'instance': [],
            'sensor': [],
            'calibrated_sensor': [],
            'ego_pose': [],
            'log': [],
            'scene': [],
            'sample': [],
            'sample_data': [],
            'sample_annotation': [],
            'map': [],
        }
        
        self.lidarseg_data = {
            'lidarseg': [],
            'lidarseg_category': [],
            'panoptic': []
        }
        
        self.nuimages_data = {
            'category': [], 'attribute': [], 'object_ann': [],
            'sensor': [], 'calibrated_sensor': [], 'log': [],
            'scene': [], 'sample': [], 'sample_data': []
        }
        
        os.makedirs(output_dir, exist_ok=True)
        # 创建输出目录
        self._create_output_dirs()
        
    
    def _create_output_dirs(self):
        """创建所有需要的输出目录"""
        self.samples_dir = os.path.join(self.output_dir, 'samples')
        self.sweeps_dir = os.path.join(self.output_dir, 'sweeps')
        self.maps_dir = os.path.join(self.output_dir, 'maps')
        self.json_dir = os.path.join(self.output_dir, 'v1.0-trainval')
        self.lidarseg_dir = os.path.join(self.output_dir, 'lidarseg/v1.0-trainval')
        self.panoptic_dir = os.path.join(self.output_dir, 'panoptic/v1.0-trainval')
        self.nuimages_dir = os.path.join(self.output_dir, 'nuimages/v1.0-trainval')
        
        os.makedirs(self.samples_dir, exist_ok=True)
        os.makedirs(self.sweeps_dir, exist_ok=True)
        os.makedirs(self.maps_dir, exist_ok=True)
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(self.lidarseg_dir, exist_ok=True)
        os.makedirs(self.panoptic_dir, exist_ok=True)
        os.makedirs(self.nuimages_dir, exist_ok=True)
        
    def _generate_token(self) -> str:
        """生成唯一的token"""
        return str(uuid.uuid4())
    
    def _save_nuscenes_od_data(self):
        """
        保存NuScenes格式数据
        
        Args:
            include_lidarseg: 是否包含lidarseg数据
        """
        for key in self.nuscenes_data.keys():
            output_file = os.path.join(self.json_dir, f"{key}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.nuscenes_data[key], f, ensure_ascii=False, indent=2)
            
            print(f"已保存: {output_file}")

    def _save_nuscenes_seg_data(self):
        for key in self.lidarseg_data.keys():
            output_file = os.path.join(self.json_dir, f"{key}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.lidarseg_data[key], f, ensure_ascii=False, indent=2)

            print(f"已保存: {output_file}")
    
    def _create_nuscenes_sensors(self):
        """创建NuScenes传感器数据"""
        lidar_sensor = {
            'token': self._generate_token(),
            'channel': 'LIDAR_TOP',
            'modality': 'lidar'
        }
        self.nuscenes_data['sensor'].append(lidar_sensor)
        self.lidar_sensor_token = lidar_sensor['token']
        
        self.camera_sensor_tokens = {}
        for idx, sensor_name in self.sensor_mapping.items():
            camera_sensor_token = self._generate_token()
            camera_sensor = {
                'token': camera_sensor_token,
                'channel': sensor_name,
                'modality': 'camera'
            }
            self.nuscenes_data['sensor'].append(camera_sensor)
            self.camera_sensor_tokens[idx] = camera_sensor_token
    
    def _process_sequences(self):
        """处理所有序列数据"""
        self._create_nuscenes_sensors()
        
        sequences = self.moore_data.get('data', [])
        
        for seq_idx, sequence in enumerate(sequences):
            self._process_single_sequence(seq_idx, sequence)
    
    def _process_single_sequence(self, seq_idx: int, sequence: Dict):
        """处理单个序列数据"""
        log_token = self._generate_token()
        log = {
            'token': log_token,
            'logfile': f"log_{seq_idx}",
            'vehicle': 'vehicle',
            'date_captured': datetime.now().strftime('%Y-%m-%d'),
            'location': 'location'
        }
        self.nuscenes_data['log'].append(log)

        map_token = self._generate_token()
        map_data = {
            'token': map_token,
            'log_tokens': [log_token],
            'filename': '',
            'category': 'semantic_prior'
        }
        self.nuscenes_data['map'].append(map_data)
    
        scene_token = self._generate_token()
        scene = {
            'token': scene_token,
            'name': f"scene_{seq_idx}",
            'description': f"Scene {seq_idx} from Moore data",
            'log_token': log_token,
            'nbr_samples': 0,
            'first_sample_token': None,
            'last_sample_token': None
        }
        self.nuscenes_data['scene'].append(scene)
        
        info = sequence.get('info', {})
        if 'info' in info:
            info = info.get('info', {})
        
        num_frames = 0
        if 'pcdUrl' in info:
            num_frames = len(info['pcdUrl'])
        
        prev_sample_token = None
        first_sample_token = None
        
        for frame_idx in range(num_frames):
            translation = [0, 0, 0]
            rotation = [1, 0, 0, 0]
            
            if 'locations' in info and frame_idx < len(info['locations']):
                location = info['locations'][frame_idx]
                if 'posMatrix' in location and len(location['posMatrix']) >= 6:
                    pos_matrix = location['posMatrix']
                    translation = [pos_matrix[0], pos_matrix[1], pos_matrix[2]]
                    
                    euler_angles = [
                        pos_matrix[3],
                        pos_matrix[4],
                        pos_matrix[5]
                    ]
                    rotation = euler_to_quaternion(euler_angles)

            ego_pose_token = self._generate_token()
            ego_pose = {
                'token': ego_pose_token,
                'translation': translation,
                'rotation': rotation,
                'timestamp': int(datetime.now().timestamp() * 1000000) + frame_idx * 100000
            }
            self.nuscenes_data['ego_pose'].append(ego_pose)
            
            sample_token = self._generate_token()
            sample = {
                'token': sample_token,
                'timestamp': ego_pose['timestamp'],
                'scene_token': scene_token,
                'prev': prev_sample_token if prev_sample_token else "",
                'next': "",
                'data': {}
            }
            
            if prev_sample_token:
                for prev_sample in self.nuscenes_data['sample']:
                    if prev_sample['token'] == prev_sample_token:
                        prev_sample['next'] = sample_token
                        break
            else:
                first_sample_token = sample_token
            
            self._process_lidar_data(sample, self.lidar_sensor_token, info['pcdUrl'][frame_idx], ego_pose_token, frame_idx)
            
            if frame_idx < len(info.get('imgUrls', [])):
                img_urls = info['imgUrls'][frame_idx]
                for camera_idx, img_url in enumerate(img_urls):
                    sensor_token = self.camera_sensor_tokens.get(camera_idx)
                    if sensor_token:
                        self._process_camera_data(sample, sensor_token, img_url, ego_pose_token, frame_idx, camera_idx)
            
            if 'labels' in sequence:
                self._process_annotations(sample, sequence, frame_idx, ego_pose)
            
            self.nuscenes_data['sample'].append(sample)
            prev_sample_token = sample_token
        
        scene['nbr_samples'] = num_frames
        scene['first_sample_token'] = first_sample_token
        scene['last_sample_token'] = prev_sample_token
    
    def _process_lidar_data(self, sample: Dict, sensor_token: str, pcd_url: str, ego_pose_token: str, frame_idx: int):
        """处理激光雷达数据"""
        calibrated_sensor_token = self._generate_token()
        
        translation = [0, 0, 0]
        rotation = [1, 0, 0, 0]

        try:
            for sequence in self.moore_data.get('data', []):
                info = sequence.get('info', {})

                if frame_idx < len(info['info']['locations']) and frame_idx < len(info['info']['pcdUrl']):
                    location = info['info']['locations'][frame_idx]
                    
                    if 'posMatrix' in location:
                        pos_matrix = location['posMatrix']

                        translation = [pos_matrix[0], pos_matrix[1], pos_matrix[2]]
                        
                        euler_angles = [
                            pos_matrix[3],
                            pos_matrix[4],
                            pos_matrix[5]
                        ]
                        rotation = euler_to_quaternion(euler_angles)
                        
                        break
        except Exception as e:
            print(f"获取位置矩阵失败: {e}")
        
        calibrated_sensor = {
            'token': calibrated_sensor_token,
            'sensor_token': sensor_token,
            'translation': translation,
            'rotation': rotation,
            'camera_intrinsic': []
        }
        self.nuscenes_data['calibrated_sensor'].append(calibrated_sensor)
        
        channel = "LIDAR_TOP"
        filename = f"samples/{channel}/{os.path.basename(pcd_url)}"
        
        sample_data_token = ego_pose_token
        sample_data = {
            'token': sample_data_token,
            'sample_token': sample['token'],
            'ego_pose_token': ego_pose_token,
            'calibrated_sensor_token': calibrated_sensor_token,
            'filename': filename,
            'fileformat': pcd_url.split('.')[-1],
            'is_key_frame': True,
            'height': 0,
            'width': 0,
            'timestamp': sample['timestamp'],
            'prev': '',
            'next': ''
        }

        if channel not in self.sample_data_tokens:
            self.sample_data_tokens[channel] = []
        if len(self.sample_data_tokens[channel]) > 0:
            prev_token = self.sample_data_tokens[channel][-1]
            sample_data['prev'] = prev_token
            
            for prev_data in self.nuscenes_data['sample_data']:
                if prev_data['token'] == prev_token:
                    prev_data['next'] = sample_data_token
                    break
        
        self.sample_data_tokens[channel].append(sample_data_token)
        self.nuscenes_data['sample_data'].append(sample_data)
        
        if channel not in sample['data']:
            sample['data'][channel] = sample_data_token
        
        target_path = os.path.join(self.output_dir, filename)
        if os.path.exists(target_path):
            return
        try:
            if pcd_url.startswith(('http://', 'https://')):
                download_file(pcd_url, target_path)
            else:
                print(f"无法处理的文件路径: {pcd_url}")
        except Exception as e:
            print(f"处理文件失败: {e}")
    
    def _process_camera_data(self, sample: Dict, sensor_token: str, img_url: str, ego_pose_token: str, frame_idx: int, camera_idx: int):
        """处理相机数据"""
        
        calibrated_sensor_token = self._generate_token()
        calibrated_sensor = {
            'token': calibrated_sensor_token,
            'sensor_token': sensor_token,
            'translation': [0, 0, 0],
            'rotation': [1, 0, 0, 0],
            'camera_intrinsic': [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        }
        self.nuscenes_data['calibrated_sensor'].append(calibrated_sensor)
        channel = self.sensor_mapping.get(camera_idx, f'CAM_{camera_idx+1}')
        filename = f"samples/{channel}/{os.path.basename(img_url)}"

        img_height, img_width = 900, 1600
        target_path = os.path.join(self.output_dir, filename)
        try:
            import cv2
            img = cv2.imread(target_path)
            img_height, img_width, _ = img.shape
        except Exception as e:
            print(f"获取图片尺寸失败: {e}")

        sample_data_token = f"{ego_pose_token}_{camera_idx}"
        sample_data = {
            'token': sample_data_token,
            'sample_token': sample['token'],
            'ego_pose_token': ego_pose_token,
            'calibrated_sensor_token': calibrated_sensor_token,
            'filename': filename,
            'fileformat': 'jpg',
            'is_key_frame': True,
            'height': img_height,
            'width': img_width,
            'timestamp': sample['timestamp'],
            'prev': '',
            'next': ''
        }

        if channel not in self.sample_data_tokens:
            self.sample_data_tokens[channel] = []
        
        if len(self.sample_data_tokens[channel]) > 0:
            prev_token = self.sample_data_tokens[channel][-1]
            sample_data['prev'] = prev_token
            
            for prev_data in self.nuscenes_data['sample_data']:
                if prev_data['token'] == prev_token:
                    prev_data['next'] = sample_data_token
                    break
        
        self.sample_data_tokens[channel].append(sample_data_token)
        self.nuscenes_data['sample_data'].append(sample_data)
        
        if channel not in sample['data']:
            sample['data'][channel] = sample_data_token
        
        target_path = os.path.join(self.output_dir, filename)
        if os.path.exists(target_path):
            return
        try:
            if img_url.startswith(('http://', 'https://')):
                download_file(img_url, target_path)
            else:
                print(f"无法处理的文件路径: {img_url}")
        except Exception as e:
            print(f"处理文件失败: {e}")
    
    def _process_annotations(self, sample: Dict, sequence: Dict, frame_idx: int, ego_pose: Dict):
        """处理标注数据"""
        if 'labels' not in sequence:
            print(f"序列中没有找到标签数据")
            return
        
        frame_labels = []
        for label_item in sequence.get('labels', []):
                
            label = label_item['data']
            if label.get('frameIndex') != frame_idx:
                continue
                
            if label.get('drawType') != 'box3d':
                continue
                
            frame_labels.append(label)
        
        if not frame_labels:
            print(f"帧 {frame_idx} 没有找到标签数据")
            return

        for label in frame_labels:
            label_id = label.get('id', '')
            label_name = label.get('label', '')
            points = label.get('points', [])
            
            x, y, z = points[0:3]
            roll, pitch, yaw = points[3:6]
            length, width, height = points[6:9]

            R_global = Rotation.from_quat(ego_pose['rotation']).as_matrix()
            t_global = np.array(ego_pose['translation'])
            # 将局部坐标中的3D框中心点转换到全局坐标
            local_pos = np.array([x, y, z])
            global_pos = R_global @ local_pos + t_global
            
            # 将局部坐标中的3D框旋转角度转换到全局坐标
            local_rot = Rotation.from_euler('xyz', [roll, pitch, yaw])
            global_rot = Rotation.from_quat(ego_pose['rotation']) * local_rot
            global_euler = global_rot.as_euler('xyz')
            
            instance_token = self._get_or_create_instance(label_id, label_name)
            
            attribute_tokens = []
            label_attributes = label.get('attributes', {})
        
            if label_attributes:
                if 'self' in label_attributes:
                    label_attributes = label_attributes['self']
                attr_order = self._get_attribute_order_for_label(label_name)
                attr_parts = []
                for attr_key in attr_order:
                    if attr_key in label_attributes:
                        attr_parts.append(label_attributes[attr_key])
                
                if not attr_parts and label_attributes:
                    attr_parts = list(label_attributes.values())
                    
                full_attr_name = f"{label_name}." + ".".join(attr_parts)
                attr_token = self.attribute_map.get(full_attr_name)
                
                if attr_token:
                    attribute_tokens.append(attr_token)
            
            annotation_token = self._generate_token()
            annotation = {
                'token': annotation_token,
                'sample_token': sample['token'],
                'instance_token': instance_token,
                'visibility_token': self._get_visibility_token(4),
                'attribute_tokens': attribute_tokens,
                'translation': [float(global_pos[0]), float(global_pos[1]), float(global_pos[2])],
                'size': [float(width), float(length), float(height)],
                'rotation': euler_to_quaternion([float(global_euler[0]), float(global_euler[1]), float(global_euler[2])]),
                'prev': '',
                'next': '',
                'num_lidar_pts': label.get('pointsInFrame', 10),
                'num_radar_pts': 0,
            }
            
            self.nuscenes_data['sample_annotation'].append(annotation)

    def _update_instance_annotation_links(self):
        """更新实例和标注之间的链接"""
        instance_annotations = {}
        for annotation in self.nuscenes_data['sample_annotation']:
            instance_token = annotation['instance_token']
            if instance_token not in instance_annotations:
                instance_annotations[instance_token] = []
            instance_annotations[instance_token].append(annotation)
        
        for instance in self.nuscenes_data['instance']:
            instance_token = instance['token']
            if instance_token in instance_annotations:
                annotations = instance_annotations[instance_token]
                instance['nbr_annotations'] = len(annotations)
                
                annotations.sort(key=lambda x: self._get_sample_timestamp(x['sample_token']))
                
                instance['first_annotation_token'] = annotations[0]['token']
                instance['last_annotation_token'] = annotations[-1]['token']
                
                for i in range(len(annotations) - 1):
                    annotations[i]['next'] = annotations[i + 1]['token']
                    annotations[i + 1]['prev'] = annotations[i]['token']

    def _create_lidarseg_categories(self):
        """创建LidarSeg类别数据"""
        label_configs = self.moore_data['task']['setting']['labelConfig']
        
        for idx, label_config in enumerate(label_configs):
            if 'label' in label_config:
                label_name = label_config['label']
                label_key = label_config.get('key', f'label_{idx}')
                category_id = idx + 1
                category = {
                    'token': self._generate_token(),
                    'name': label_name,
                    'description': f"Category {label_name}",
                    'index': category_id,
                    'color': label_config.get('color', '#FFFFFF')
                }
                
                self.lidarseg_data['lidarseg_category'].append(category)
                self.lidarseg_category_map[label_key] = category_id
        print(f"创建了 {len(self.lidarseg_data['lidarseg_category'])} 个LidarSeg类别")
    
    def _process_lidarseg_data(self, sample_data_token: str, pcd_url: str, frame_idx: int, sequence: Dict):
        """
        处理LidarSeg数据
        
        Args:
            sample_data_token: 对应的sample_data的token
            pcd_url: 点云文件URL
            frame_idx: 帧索引
            sequence: 序列数据
        """
        semantic_label = None
        if 'labels' in sequence:
            for label_item in sequence.get('labels', []):
                label_data = label_item.get('data', {})
                
                if (label_data.get('frameIndex') == frame_idx and
                    label_data.get('drawType') == 'SEMANTIC_BASE' and
                    'pLabelIdMap' in label_data):
                    semantic_label = label_data
                    break
        
        if not semantic_label:
            print(f"帧 {frame_idx} 未找到语义分割标签")
            return
        
        plabelidmap = semantic_label.get('pLabelIdMap', '')
        
        if not plabelidmap:
            print(f"帧 {frame_idx} 的语义分割标签中未找到pLabelIdMap")
            return
        
        try:
            decompressed_data = zlib.decompress(
                base64.b64decode(plabelidmap), 16 + zlib.MAX_WBITS
            )
            
            point_labels = np.frombuffer(decompressed_data, dtype=np.uint8)
            
            if len(point_labels) == 0:
                print(f"帧 {frame_idx} 的pLabelIdMap解析结果为空")
                return
            
            print(f"帧 {frame_idx} 的pLabelIdMap解析成功，共 {len(point_labels)} 个点")
            
            lidarseg_filename = f"{os.path.basename(pcd_url).split('.')[0]}.bin"
            lidarseg_path = os.path.join(self.lidarseg_dir, lidarseg_filename)

            mapped_labels = np.zeros(len(point_labels), dtype=np.uint8)
            
            label_mapping = {}
            if 'task' in self.moore_data and 'setting' in self.moore_data['task'] and 'labelConfig' in self.moore_data['task']['setting']:
                label_configs = self.moore_data['task']['setting']['labelConfig']
                for idx, config in enumerate(label_configs):
                    label_key = config.get('key', f'label_{idx}')
                    label_id = idx + 1
                    label_mapping[idx] = label_id
                    self.lidarseg_category_map[label_key] = label_id
            
            for i, label_id in enumerate(point_labels):
                if label_id in label_mapping:
                    mapped_labels[i] = label_mapping[label_id]
                else:
                    mapped_labels[i] = 0
            
            os.makedirs(os.path.dirname(lidarseg_path), exist_ok=True)
            mapped_labels.astype(np.uint8).tofile(lidarseg_path)
            
            lidarseg_entry = {
                'token': sample_data_token,
                'sample_data_token': sample_data_token,
                'filename': f"lidarseg/v1.0-trainval/{lidarseg_filename}"
            }
            self.lidarseg_data['lidarseg'].append(lidarseg_entry)
            
            print(f"保存lidarseg文件: {lidarseg_path}")
            
            self._process_panoptic_data(sample_data_token, pcd_url, point_labels)
            
        except Exception as e:
            print(f"处理帧 {frame_idx} 的pLabelIdMap时出错: {e}")
            return
    
    def _process_panoptic_data(self, sample_data_token: str, pcd_url: str, point_labels: np.ndarray):
        """
        处理全景分割数据
        
        Args:
            sample_data_token: 对应的sample_data的token
            pcd_url: 点云文件URL
            frame_idx: 帧索引
            point_labels: 点云标签数组
        """
        panoptic_filename = f"{os.path.basename(pcd_url).split('.')[0]}.npz"
        panoptic_path = os.path.join(self.panoptic_dir, panoptic_filename)
        
        instance_ids = np.zeros(len(point_labels), dtype=np.uint16)
        
        # TODO: 根据3D框信息将点分配给实例
        
        os.makedirs(os.path.dirname(panoptic_path), exist_ok=True)
        np.savez_compressed(
            panoptic_path,
            semantics=point_labels.astype(np.uint8),
            instance=instance_ids
        )
        
        panoptic_entry = {
            'token': sample_data_token,
            'sample_data_token': sample_data_token,
            'filename': f"panoptic/v1.0-trainval/{panoptic_filename}"
        }
        self.lidarseg_data['panoptic'].append(panoptic_entry)
        
        print(f"保存panoptic文件: {panoptic_path}")
    
    def moore_json2nuscenes_3dod(self) -> str:
        """
        将Moore格式JSON转换为NuScenes 3D目标检测格式
        
        Returns:
            输出目录路径
        """
        # 创建标签映射和类别
        self._create_label_map()
        self._create_categories()
        self._create_nuscenes_attributes()
        self._create_nuscenes_visibility()
        
        # 处理序列
        self._process_sequences()
        
        # 更新实例和标注之间的链接
        self._update_instance_annotation_links()
        
        # 保存NuScenes格式数据
        self._save_nuscenes_od_data()
        
        return self.output_dir
    
    def moore_json2nuscenes_lidarseg(self) -> str:
        """
        将Moore格式JSON转换为NuScenes LidarSeg格式
        
        Returns:
            输出目录路径
        """
        self._create_lidarseg_categories()
        
        sequences = self.moore_data.get('data', [])
        
        for seq_idx, sequence in enumerate(sequences):
            info = sequence.get('info', {})
            if 'info' in info:
                info = info.get('info', {})
            
            num_frames = 0
            if 'pcdUrl' in info:
                num_frames = len(info['pcdUrl'])
            
            for frame_idx in range(num_frames):
                pcd_url = info['pcdUrl'][frame_idx]
                sample_data_token = self._generate_token()
                self._process_lidarseg_data(sample_data_token, pcd_url, frame_idx, sequence)

        self._save_nuscenes_seg_data()
        
        return self.output_dir
    
    def moore_json2nuscenes_nuimages(self) -> str:
        """
        将Moore格式JSON转换为nuImages格式
        
        Returns:
            输出目录路径
        """
        self._create_label_map()
        self._create_categories()
        self._create_nuscenes_attributes()
        
        sequences = self.moore_data.get('data', [])
        for seq_idx, sequence in enumerate(sequences):
            self._process_nuimages_sequence(seq_idx, sequence)
        
        self._save_nuimages_data()
        return self.output_dir
    
    def _process_nuimages_sequence(self, seq_idx: int, sequence: Dict):
        """处理单个序列的nuImages数据"""
        log_token = self._generate_token()
        log = {
            'token': log_token,
            'logfile': f"log_{seq_idx}",
            'vehicle': 'vehicle',
            'date_captured': datetime.now().strftime('%Y-%m-%d'),
            'location': 'location'
        }
        self.nuimages_data['log'].append(log)
        
        scene_token = self._generate_token()
        scene = {
            'token': scene_token,
            'name': f"scene_{seq_idx}",
            'description': f"Scene {seq_idx} from Moore data",
            'log_token': log_token,
            'nbr_samples': 0,
            'first_sample_token': None,
            'last_sample_token': None
        }
        self.nuimages_data['scene'].append(scene)
        
        info = sequence.get('info', {}).get('info', {})
        num_frames = len(info.get('imgUrls', []))
        
        prev_sample_token = None
        first_sample_token = None
        
        for frame_idx in range(num_frames):
            sample_token = self._generate_token()
            sample = {
                'token': sample_token,
                'timestamp': int(datetime.now().timestamp() * 1000000) + frame_idx * 100000,
                'scene_token': scene_token,
                'prev': prev_sample_token if prev_sample_token else "",
                'next': "",
                'data': {}
            }
            
            if prev_sample_token:
                for prev_sample in self.nuimages_data['sample']:
                    if prev_sample['token'] == prev_sample_token:
                        prev_sample['next'] = sample_token
                        break
            
            self._process_nuimages_data(sample, sequence, frame_idx)
            
            self.nuimages_data['sample'].append(sample)
            prev_sample_token = sample_token
            
            if first_sample_token is None:
                first_sample_token = sample_token
        
        scene['nbr_samples'] = num_frames
        scene['first_sample_token'] = first_sample_token
        scene['last_sample_token'] = prev_sample_token
    
    def _process_nuimages_data(self, sample: Dict, sequence: Dict, frame_idx: int):
        """处理nuImages数据"""
        # 处理相机数据
        info = sequence.get('info', {}).get('info', {})
        if frame_idx < len(info.get('imgUrls', [])):
            img_urls = info['imgUrls'][frame_idx]
            for camera_idx, img_url in enumerate(img_urls):
                self._process_nuimages_camera_data(sample, camera_idx, img_url, frame_idx)
        
        # 处理2D标注
        if 'labels' in sequence:
            self._process_nuimages_annotations(sample, sequence, frame_idx)
    
    def _process_nuimages_camera_data(self, sample: Dict, camera_idx: int, img_url: str, frame_idx: int):
        """处理nuImages相机数据"""
        sensor_token = self.camera_sensor_tokens.get(camera_idx)
        if not sensor_token:
            return
        
        calibrated_sensor_token = self._generate_token()
        calibrated_sensor = {
            'token': calibrated_sensor_token,
            'sensor_token': sensor_token,
            'translation': [0, 0, 0],
            'rotation': [1, 0, 0, 0],
            'camera_intrinsic': [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        }
        self.nuimages_data['calibrated_sensor'].append(calibrated_sensor)
        
        channel = self.sensor_mapping.get(camera_idx, f'CAM_{camera_idx+1}')
        filename = f"samples/{channel}/{os.path.basename(img_url)}"
        
        sample_data_token = self._generate_token()
        sample_data = {
            'token': sample_data_token,
            'sample_token': sample['token'],
            'fileformat': 'jpg',
            'filename': filename,
            'is_key_frame': True,
            'height': 900,
            'width': 1600,
            'timestamp': sample['timestamp']
        }
        
        self.nuimages_data['sample_data'].append(sample_data)
        sample['data'][channel] = sample_data_token
        
        # 下载图片
        target_path = os.path.join(self.output_dir, filename)
        if not os.path.exists(target_path) and img_url.startswith(('http://', 'https://')):
            download_file(img_url, target_path)
    
    def _process_nuimages_annotations(self, sample: Dict, sequence: Dict, frame_idx: int):
        """处理nuImages 2D标注"""
        for label_item in sequence.get('labels', []):
            label = label_item['data']
            if label.get('frameIndex') != frame_idx or label.get('drawType') != 'rectangle':
                continue
                
            # 处理2D框标注
            self._create_nuimages_annotation(sample, label)
    
    def _create_nuimages_annotation(self, sample: Dict, label: Dict):
        """创建nuImages标注"""
        category_token = self._get_category_token(label.get('label', ''))
        attribute_tokens = []
        if 'attributes' in label:
            for attr_name, attr_value in label['attributes'].items():
                full_attr_name = f"{label.get('label', '')}.{attr_name}.{attr_value}"
                if full_attr_name in self.attribute_map:
                    attribute_tokens.append(self.attribute_map[full_attr_name])
        
        annotation_token = self._generate_token()
        annotation = {
            'token': annotation_token,
            'category_token': category_token,
            'attribute_tokens': attribute_tokens,
            'bbox': label.get('points', []),
            'mask': None,
            'sample_data_token': next(iter(sample['data'].values()), ''),
            'visibility_token': self._get_visibility_token(4)
        }
        
        self.nuimages_data['object_ann'].append(annotation)
    
    def _save_nuimages_data(self):
        """保存nuImages格式数据"""
        for key in self.nuimages_data.keys():
            output_file = os.path.join(self.nuimages_dir, f"{key}.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.nuimages_data[key], f, ensure_ascii=False, indent=2)
            print(f"已保存nuImages数据: {output_file}")