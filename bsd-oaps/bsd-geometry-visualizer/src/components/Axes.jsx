import React from 'react';
import * as THREE from 'three';
import { AXIS_CONFIG, SPHERE_CONFIG } from '../data/sphereConfig';

export default function Axes() {
  const axisLength = SPHERE_CONFIG.radius + 1;
  
  return (
    <group>
      <AxisLine 
        direction="x" 
        color={AXIS_CONFIG.xAxis.color} 
        length={axisLength}
      />
      <AxisLine 
        direction="y" 
        color={AXIS_CONFIG.yAxis.color} 
        length={axisLength}
      />
      <AxisLine 
        direction="z" 
        color={AXIS_CONFIG.zAxis.color} 
        length={axisLength}
      />
      <AxisLabels />
      <CenterMarker />
    </group>
  );
}

function AxisLine({ direction, color, length }) {
  const points = [];
  
  if (direction === 'x') {
    points.push(new THREE.Vector3(-length, 0, 0));
    points.push(new THREE.Vector3(length, 0, 0));
  } else if (direction === 'y') {
    points.push(new THREE.Vector3(0, -length, 0));
    points.push(new THREE.Vector3(0, length, 0));
  } else {
    points.push(new THREE.Vector3(0, 0, -length));
    points.push(new THREE.Vector3(0, 0, length));
  }
  
  const geometry = new THREE.BufferGeometry().setFromPoints(points);
  
  return (
    <group>
      <line geometry={geometry}>
        <lineBasicMaterial color={color} transparent opacity={0.5} />
      </line>
      
      {direction === 'x' && (
        <mesh position={[length, 0, 0]} rotation={[0, 0, -Math.PI / 2]}>
          <coneGeometry args={[0.1, 0.3, 8]} />
          <meshBasicMaterial color={color} />
        </mesh>
      )}
      {direction === 'y' && (
        <mesh position={[0, length, 0]}>
          <coneGeometry args={[0.1, 0.3, 8]} />
          <meshBasicMaterial color={color} />
        </mesh>
      )}
      {direction === 'z' && (
        <mesh position={[0, 0, length]} rotation={[Math.PI / 2, 0, 0]}>
          <coneGeometry args={[0.1, 0.3, 8]} />
          <meshBasicMaterial color={color} />
        </mesh>
      )}
    </group>
  );
}

function AxisLabels() {
  return (
    <group>
      <mesh position={[3.5, 0.3, 0]}>
        <planeGeometry args={[0.6, 0.2]} />
        <meshBasicMaterial color={0x000000} transparent opacity={0.8} />
      </mesh>
      <mesh position={[-3.5, 0.3, 0]}>
        <planeGeometry args={[0.8, 0.2]} />
        <meshBasicMaterial color={0x000000} transparent opacity={0.8} />
      </mesh>
    </group>
  );
}

function CenterMarker() {
  return (
    <group position={[0, 0, 0]}>
      <mesh>
        <sphereGeometry args={[0.05, 8, 8]} />
        <meshBasicMaterial color={0xffffff} />
      </mesh>
      <mesh>
        <ringGeometry args={[0.08, 0.12, 32]} />
        <meshBasicMaterial 
          color={0xffffff} 
          transparent 
          opacity={0.5}
          side={THREE.DoubleSide}
        />
      </mesh>
    </group>
  );
}
