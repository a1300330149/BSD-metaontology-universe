import React, { useState, useCallback, useEffect, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Stars, Text } from '@react-three/drei';
import Sphere from './components/Sphere';
import ZAxisAnchors from './components/ZAxisAnchors';
import BidirectionalFlow from './components/BidirectionalFlow';
import EmergenceParticles from './components/EmergenceParticles';
import Axes from './components/Axes';
import ControlPanel from './components/ControlPanel';
import { Z_AXIS_ANCHORS } from './data/sphereConfig';

export default function App() {
  const [isFlowing, setIsFlowing] = useState(false);
  const [showClockwise, setShowClockwise] = useState(true);
  const [showCounterClockwise, setShowCounterClockwise] = useState(true);
  const [showWireframe, setShowWireframe] = useState(false);
  const [activeAnchors, setActiveAnchors] = useState([
    'A1_SOUTH_POLE', 'A4_CENTER', 'A7_NORTH_POLE'
  ]);
  const [highlightAnchor, setHighlightAnchor] = useState(null);
  const [emergenceLog, setEmergenceLog] = useState([]);
  const [currentEmergenceId, setCurrentEmergenceId] = useState(null);
  const [triggerPosition, setTriggerPosition] = useState([0, 0, 0]);
  const [isTriggered, setIsTriggered] = useState(false);
  const [emergenceCount, setEmergenceCount] = useState(3);

  const handleToggleFlow = useCallback(() => {
    setIsFlowing(prev => !prev);
  }, []);

  const handleAnchorClick = useCallback((anchorId) => {
    setActiveAnchors(prev => {
      if (prev.includes(anchorId)) {
        return prev.filter(id => id !== anchorId);
      }
      return [...prev, anchorId];
    });
    
    const anchor = Z_AXIS_ANCHORS.find(a => a.id === anchorId);
    if (anchor) {
      setHighlightAnchor(anchorId);
      setTriggerPosition(anchor.position);
      
      setTimeout(() => setHighlightAnchor(null), 2000);
    }
  }, []);

  const handleTriggerEmergence = useCallback(() => {
    const newCount = emergenceCount + 1;
    const newId = `EMERGENCE-${String(newCount).padStart(3, '0')}`;
    
    const content = [
      '双时针耦合涌现',
      '气流动产生新的可能性',
      '0∅ × 0Ψ = n 实演',
      '几何相激活·空间涌现'
    ];
    
    const newLog = {
      id: newId,
      content: content[Math.floor(Math.random() * content.length)]
    };
    
    setEmergenceCount(newCount);
    setCurrentEmergenceId(newId);
    setEmergenceLog(prev => [newLog, ...prev].slice(0, 10));
    setIsTriggered(true);
    
    setTimeout(() => setIsTriggered(false), 100);
  }, [emergenceCount]);

  const handleToggleWireframe = useCallback(() => {
    setShowWireframe(prev => !prev);
  }, []);

  const handleToggleClockwise = useCallback(() => {
    setShowClockwise(prev => !prev);
  }, []);

  const handleToggleCounterClockwise = useCallback(() => {
    setShowCounterClockwise(prev => !prev);
  }, []);

  return (
    <div className="app-container">
      <div className="canvas-container">
        <Canvas
          camera={{ position: [5, 5, 8], fov: 45 }}
          style={{ background: '#0a0a0a' }}
        >
          <Suspense fallback={null}>
            <ambientLight intensity={0.3} />
            <pointLight position={[10, 10, 10]} intensity={0.5} />
            <pointLight position={[-10, -10, -10]} intensity={0.3} color={0x9c27b0} />
            
            <Stars 
              radius={100} 
              depth={50} 
              count={2000} 
              factor={4} 
              saturation={0.5}
              fade
            />
            
            <Sphere wireframeOnly={showWireframe} />
            <ZAxisAnchors 
              activeAnchors={activeAnchors}
              highlightAnchor={highlightAnchor}
            />
            <BidirectionalFlow 
              isActive={isFlowing}
              showClockwise={showClockwise}
              showCounterClockwise={showCounterClockwise}
            />
            <EmergenceParticles 
              isTriggered={isTriggered}
              triggerPosition={triggerPosition}
              emergenceId={currentEmergenceId}
            />
            <Axes />
            
            <OrbitControls
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
              minDistance={3}
              maxDistance={20}
            />
          </Suspense>
        </Canvas>
        
        <div className="overlay-info">
          <h1>BSD元数学·几何相激活</h1>
          <p>
            <span className="highlight">双时针自证闭环</span><br/>
            顺时针(绿) = 炁·积累 · 逆时针(橙) = 气·归零<br/>
            <span className="highlight">核心公式</span><br/>
            0∅ × 0Ψ = n
          </p>
        </div>
      </div>
      
      <ControlPanel
        isFlowing={isFlowing}
        onToggleFlow={handleToggleFlow}
        activeAnchors={activeAnchors}
        onAnchorClick={handleAnchorClick}
        onTriggerEmergence={handleTriggerEmergence}
        emergenceLog={emergenceLog}
        currentEmergenceId={currentEmergenceId}
        highlightAnchor={highlightAnchor}
        onHighlightAnchor={setHighlightAnchor}
        showWireframe={showWireframe}
        onToggleWireframe={handleToggleWireframe}
        showClockwise={showClockwise}
        showCounterClockwise={showCounterClockwise}
        onToggleClockwise={handleToggleClockwise}
        onToggleCounterClockwise={handleToggleCounterClockwise}
      />
    </div>
  );
}
