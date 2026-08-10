import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { SPHERE_CONFIG, DUAL_CLOCK_CONFIG } from '../data/sphereConfig';

export default function BidirectionalFlow({ isActive = true, showClockwise = true, showCounterClockwise = true }) {
  const clockwiseRef = useRef();
  const counterClockwiseRef = useRef();

  useFrame((state) => {
    if (!isActive) return;
    
    const t = state.clock.elapsedTime;
    
    if (clockwiseRef.current && showClockwise) {
      clockwiseRef.current.rotation.y = t * DUAL_CLOCK_CONFIG.clockwise.speed * 0.5;
      clockwiseRef.current.rotation.z = Math.sin(t * 0.3) * 0.2;
    }
    
    if (counterClockwiseRef.current && showCounterClockwise) {
      counterClockwiseRef.current.rotation.y = t * DUAL_CLOCK_CONFIG.counterclockwise.speed * 0.5;
      counterClockwiseRef.current.rotation.x = Math.sin(t * 0.3) * 0.2;
    }
  });

  return (
    <group>
      {showClockwise && (
        <group ref={clockwiseRef}>
          <FlowRing
            color={DUAL_CLOCK_CONFIG.clockwise.color}
            radius={SPHERE_CONFIG.radius + 0.3}
            direction="clockwise"
          />
          <FlowParticles
            color={DUAL_CLOCK_CONFIG.clockwise.color}
            count={30}
            speed={1}
            radius={SPHERE_CONFIG.radius + 0.3}
          />
        </group>
      )}
      
      {showCounterClockwise && (
        <group ref={counterClockwiseRef}>
          <FlowRing
            color={DUAL_CLOCK_CONFIG.counterclockwise.color}
            radius={SPHERE_CONFIG.radius + 0.5}
            direction="counterclockwise"
          />
          <FlowParticles
            color={DUAL_CLOCK_CONFIG.counterclockwise.color}
            count={30}
            speed={-1}
            radius={SPHERE_CONFIG.radius + 0.5}
          />
        </group>
      )}
    </group>
  );
}

function FlowRing({ color, radius, direction }) {
  const geometry = useMemo(() => {
    return new THREE.TorusGeometry(radius, 0.01, 8, 128);
  }, [radius]);

  return (
    <mesh geometry={geometry}>
      <meshBasicMaterial 
        color={color} 
        transparent 
        opacity={0.6}
      />
    </mesh>
  );
}

function FlowParticles({ color, count, speed, radius }) {
  const particlesRef = useRef();
  
  const { positions, velocities } = useMemo(() => {
    const pos = new Float32Array(count * 3);
    const vel = new Float32Array(count);
    
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const yOffset = Math.sin(angle * 3) * 0.5;
      
      pos[i * 3] = Math.cos(angle) * radius;
      pos[i * 3 + 1] = yOffset;
      pos[i * 3 + 2] = Math.sin(angle) * radius;
      vel[i] = speed * (0.5 + Math.random() * 0.5);
    }
    
    return { positions: pos, velocities: vel };
  }, [count, radius, speed]);

  useFrame((state) => {
    if (!particlesRef.current) return;
    
    const posArray = particlesRef.current.geometry.attributes.position.array;
    const time = state.clock.elapsedTime * speed * 0.5;
    
    for (let i = 0; i < count; i++) {
      const baseAngle = (i / count) * Math.PI * 2;
      const angle = baseAngle + time + velocities[i];
      const yOffset = Math.sin(angle * 3 + time) * 0.5;
      
      posArray[i * 3] = Math.cos(angle) * radius;
      posArray[i * 3 + 1] = yOffset;
      posArray[i * 3 + 2] = Math.sin(angle) * radius;
    }
    
    particlesRef.current.geometry.attributes.position.needsUpdate = true;
  });

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          array={positions}
          count={count}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        color={color}
        size={0.08}
        transparent
        opacity={0.8}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </points>
  );
}
