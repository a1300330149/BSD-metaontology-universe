import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { SIX_SYSTEMS, SPHERE_CONFIG } from '../data/sphereConfig';

export default function Sphere({ wireframeOnly = false }) {
  const meshRef = useRef();
  const wireframeRef = useRef();

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.05;
    }
    if (wireframeRef.current) {
      wireframeRef.current.rotation.y = -state.clock.elapsedTime * 0.03;
    }
  });

  return (
    <group>
      {!wireframeOnly && (
        <mesh ref={meshRef}>
          <sphereGeometry args={[SPHERE_CONFIG.radius, SPHERE_CONFIG.segments, SPHERE_CONFIG.segments]} />
          <meshPhongMaterial
            color={SPHERE_CONFIG.color}
            transparent
            opacity={0.3}
            shininess={100}
            side={THREE.DoubleSide}
          />
        </mesh>
      )}
      <mesh ref={wireframeRef}>
        <sphereGeometry args={[SPHERE_CONFIG.radius + 0.01, 24, 24]} />
        <meshBasicMaterial
          color={SPHERE_CONFIG.wireframeColor}
          wireframe
          transparent
          opacity={0.4}
        />
      </mesh>
      <SixSystemPoles />
      <MeridianLines />
    </group>
  );
}

function SixSystemPoles() {
  return (
    <group>
      {Object.values(SIX_SYSTEMS).map((sys) => (
        <PoleMarker
          key={sys.id}
          position={sys.position}
          color={sys.color}
          label={sys.name}
        />
      ))}
    </group>
  );
}

function PoleMarker({ position, color, label }) {
  const groupRef = useRef();
  const haloRef = useRef();

  useFrame((state) => {
    if (haloRef.current) {
      haloRef.current.scale.setScalar(1 + Math.sin(state.clock.elapsedTime * 2) * 0.1);
    }
  });

  return (
    <group position={position}>
      <mesh ref={haloRef}>
        <sphereGeometry args={[0.4, 16, 16]} />
        <meshBasicMaterial color={color} transparent opacity={0.3} />
      </mesh>
      <mesh ref={groupRef}>
        <sphereGeometry args={[0.2, 16, 16]} />
        <meshPhongMaterial
          color={color}
          emissive={color}
          emissiveIntensity={0.5}
        />
      </mesh>
    </group>
  );
}

function MeridianLines() {
  const meridians = useMemo(() => {
    const lines = [];
    const radius = SPHERE_CONFIG.radius + 0.1;
    const segments = 64;

    for (let i = 0; i < 6; i++) {
      const angle = (i * Math.PI) / 6;
      const points = [];
      
      for (let j = 0; j <= segments; j++) {
        const t = (j / segments) * Math.PI * 2;
        const x = Math.sin(t) * Math.cos(angle);
        const y = Math.cos(t);
        const z = Math.sin(t) * Math.sin(angle);
        points.push(new THREE.Vector3(x * radius, y * radius, z * radius));
      }
      
      const geometry = new THREE.BufferGeometry().setFromPoints(points);
      lines.push({ geometry, angle, id: i });
    }
    return lines;
  }, []);

  return (
    <group>
      {meridians.map((m, index) => (
        <line key={index} geometry={m.geometry}>
          <lineBasicMaterial color={0x4a2c6e} transparent opacity={0.3} />
        </line>
      ))}
    </group>
  );
}
