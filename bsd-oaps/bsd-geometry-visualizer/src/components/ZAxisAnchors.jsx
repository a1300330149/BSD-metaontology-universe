import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';
import { Z_AXIS_ANCHORS, SPHERE_CONFIG } from '../data/sphereConfig';

export default function ZAxisAnchors({ activeAnchors = [], highlightAnchor = null }) {
  return (
    <group>
      <ZAxisLine />
      {Z_AXIS_ANCHORS.map((anchor) => (
        <AnchorPoint
          key={anchor.id}
          anchor={anchor}
          isActive={activeAnchors.includes(anchor.id)}
          isHighlighted={highlightAnchor === anchor.id}
        />
      ))}
      <SemanticChain />
    </group>
  );
}

function ZAxisLine() {
  const points = useMemo(() => {
    return [
      new THREE.Vector3(0, -SPHERE_CONFIG.radius - 0.5, 0),
      new THREE.Vector3(0, SPHERE_CONFIG.radius + 0.5, 0)
    ];
  }, []);

  const geometry = useMemo(() => new THREE.BufferGeometry().setFromPoints(points), [points]);

  return (
    <group>
      <line geometry={geometry}>
        <lineBasicMaterial color={0x2196f3} linewidth={2} />
      </line>
      <mesh position={[0, -SPHERE_CONFIG.radius - 0.5, 0]}>
        <coneGeometry args={[0.15, 0.3, 8]} />
        <meshBasicMaterial color={0xff1744} />
      </mesh>
      <mesh position={[0, SPHERE_CONFIG.radius + 0.5, 0]} rotation={[Math.PI, 0, 0]}>
        <coneGeometry args={[0.15, 0.3, 8]} />
        <meshBasicMaterial color={0xd500f9} />
      </mesh>
    </group>
  );
}

function AnchorPoint({ anchor, isActive, isHighlighted }) {
  const ref = useRef();
  const haloRef = useRef();
  const ringRef = useRef();

  useFrame((state) => {
    const t = state.clock.elapsedTime;
    
    if (ref.current) {
      const scale = isHighlighted ? 1.5 : isActive ? 1.2 : 0.8;
      ref.current.scale.setScalar(scale + Math.sin(t * 3 + anchor.z * 10) * 0.1);
    }
    
    if (haloRef.current) {
      const haloScale = isHighlighted ? 2.5 : isActive ? 1.8 : 1.2;
      haloRef.current.scale.setScalar(haloScale + Math.sin(t * 2 + anchor.z * 5) * 0.2);
    }
    
    if (ringRef.current) {
      ringRef.current.rotation.x = t * 0.5;
      ringRef.current.rotation.z = t * 0.3;
    }
  });

  const baseScale = isHighlighted ? 1.5 : isActive ? 1.2 : 0.8;

  return (
    <group position={anchor.position}>
      <mesh ref={haloRef}>
        <sphereGeometry args={[0.25, 16, 16]} />
        <meshBasicMaterial 
          color={anchor.color} 
          transparent 
          opacity={isActive || isHighlighted ? 0.3 : 0.15} 
        />
      </mesh>
      
      <mesh ref={ref}>
        <octahedronGeometry args={[0.15, 0]} />
        <meshPhongMaterial
          color={anchor.color}
          emissive={anchor.color}
          emissiveIntensity={isActive || isHighlighted ? 0.8 : 0.3}
          shininess={100}
        />
      </mesh>
      
      {(isActive || isHighlighted) && (
        <mesh ref={ringRef}>
          <torusGeometry args={[0.3, 0.02, 8, 32]} />
          <meshBasicMaterial color={anchor.color} transparent opacity={0.6} />
        </mesh>
      )}
    </group>
  );
}

function SemanticChain() {
  const ref = useRef();
  
  useFrame((state) => {
    if (ref.current) {
      ref.current.rotation.y = state.clock.elapsedTime * 0.1;
    }
  });

  const chain = useMemo(() => {
    const path = [];
    const startY = -3.5;
    const endY = 3.5;
    const steps = 100;
    
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      const y = startY + t * (endY - startY);
      const x = Math.sin(t * Math.PI * 2) * 0.15;
      const z = Math.cos(t * Math.PI * 2) * 0.15;
      path.push(new THREE.Vector3(x, y, z));
    }
    
    return new THREE.BufferGeometry().setFromPoints(path);
  }, []);

  return (
    <group ref={ref} opacity={0.5}>
      <line geometry={chain}>
        <lineDashedMaterial 
          color={0x9c27b0} 
          dashSize={0.1} 
          gapSize={0.05}
          transparent
          opacity={0.4}
        />
      </line>
    </group>
  );
}
