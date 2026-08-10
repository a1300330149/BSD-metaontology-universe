import React, { useRef, useMemo, useState, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { EMERGENCE_CONFIG, SPHERE_CONFIG } from '../data/sphereConfig';

export default function EmergenceParticles({ 
  isTriggered = false, 
  triggerPosition = [0, 0, 0],
  emergenceId = null 
}) {
  const particlesRef = useRef();
  const burstRef = useRef();
  const [particles, setParticles] = useState([]);
  const [burstActive, setBurstActive] = useState(false);

  useEffect(() => {
    if (isTriggered && emergenceId) {
      const newParticles = generateEmergenceParticles(triggerPosition, emergenceId);
      setParticles(prev => [...prev.slice(-200), ...newParticles]);
      setBurstActive(true);
      
      const timer = setTimeout(() => setBurstActive(false), 2000);
      return () => clearTimeout(timer);
    }
  }, [isTriggered, emergenceId]);

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    
    if (particlesRef.current && particles.length > 0) {
      const positions = particlesRef.current.geometry.attributes.position.array;
      
      particles.forEach((p, i) => {
        if (!p.active) return;
        
        const idx = i * 3;
        const life = (t - p.birthTime) / p.lifetime;
        
        if (life >= 1) {
          p.active = false;
          positions[idx] = 0;
          positions[idx + 1] = -100;
          positions[idx + 2] = 0;
          return;
        }
        
        const dir = new THREE.Vector3(p.vx, p.vy, p.vz).normalize();
        const speed = p.speed * (1 - life * 0.5);
        
        positions[idx] += dir.x * speed * 0.02;
        positions[idx + 1] += dir.y * speed * 0.02 + 0.01 * Math.sin(t * 2 + i);
        positions[idx + 2] += dir.z * speed * 0.02;
      });
      
      particlesRef.current.geometry.attributes.position.needsUpdate = true;
    }
    
    if (burstRef.current && burstActive) {
      const scale = 1 + Math.sin(t * 10) * 0.2;
      burstRef.current.scale.setScalar(scale);
      burstRef.current.material.opacity = 0.8 - (t * 0.3);
    }
  });

  const positions = useMemo(() => {
    const arr = new Float32Array(EMERGENCE_CONFIG.particleCount * 3);
    for (let i = 0; i < EMERGENCE_CONFIG.particleCount; i++) {
      arr[i * 3] = 0;
      arr[i * 3 + 1] = -100;
      arr[i * 3 + 2] = 0;
    }
    return arr;
  }, []);

  return (
    <group>
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            array={positions}
            count={EMERGENCE_CONFIG.particleCount}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.15}
          transparent
          opacity={0.9}
          vertexColors
          blending={THREE.AdditiveBlending}
          sizeAttenuation
        />
      </points>
      
      {burstActive && (
        <mesh ref={burstRef} position={triggerPosition}>
          <sphereGeometry args={[0.3, 32, 32]} />
          <meshBasicMaterial 
            color={0xff9800} 
            transparent 
            opacity={0.8}
            blending={THREE.AdditiveBlending}
          />
        </mesh>
      )}
    </group>
  );
}

function generateEmergenceParticles(center, id) {
  const newParticles = [];
  
  for (let i = 0; i < EMERGENCE_CONFIG.burstCount; i++) {
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(2 * Math.random() - 1);
    
    newParticles.push({
      active: true,
      birthTime: Date.now() / 1000,
      lifetime: 3 + Math.random() * 2,
      vx: Math.sin(phi) * Math.cos(theta) * (Math.random() * 2 + 1),
      vy: Math.sin(phi) * Math.sin(theta) * (Math.random() * 2 + 1),
      vz: Math.cos(phi) * (Math.random() * 2 + 1),
      speed: 0.5 + Math.random() * 1.5,
      colorIndex: Math.floor(Math.random() * EMERGENCE_CONFIG.colors.length)
    });
  }
  
  return newParticles;
}
