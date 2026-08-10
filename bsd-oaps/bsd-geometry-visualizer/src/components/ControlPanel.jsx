import React, { useState, useEffect } from 'react';
import { SIX_SYSTEMS, Z_AXIS_ANCHORS } from '../data/sphereConfig';

export default function ControlPanel({
  isFlowing,
  onToggleFlow,
  activeAnchors,
  onAnchorClick,
  onTriggerEmergence,
  emergenceLog,
  currentEmergenceId,
  highlightAnchor,
  onHighlightAnchor,
  showWireframe,
  onToggleWireframe,
  showClockwise,
  showCounterClockwise,
  onToggleClockwise,
  onToggleCounterClockwise
}) {
  return (
    <div className="control-panel">
      <div className="panel-title">BSD几何相激活器 V2.3</div>
      <div className="panel-subtitle">
        元数学从文本相→几何相的气流动可视化<br/>
        双时针·六系极向·Z轴七点锚定
      </div>

      <div className="section">
        <div className="section-title">双时针控制</div>
        <button 
          className={`control-btn ${isFlowing ? 'active' : ''}`}
          onClick={onToggleFlow}
        >
          {isFlowing ? '⏸ 暂停气流动' : '▶ 激活气流动'}
        </button>
        <button 
          className={`control-btn ${showClockwise ? 'active' : ''}`}
          onClick={onToggleClockwise}
        >
          {showClockwise ? '🟢 顺时针·积累(开)' : '⚪ 顺时针·积累(关)'}
        </button>
        <button 
          className={`control-btn ${showCounterClockwise ? 'active' : ''}`}
          onClick={onToggleCounterClockwise}
        >
          {showCounterClockwise ? '🟠 逆时针·归零(开)' : '⚪ 逆时针·归零(关)'}
        </button>
      </div>

      <div className="section">
        <div className="section-title">六系极向</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
          {Object.values(SIX_SYSTEMS).map(sys => (
            <div 
              key={sys.id}
              className="status-display"
              style={{ 
                borderColor: `#${sys.color.toString(16).padStart(6, '0')}`,
                cursor: 'pointer',
                padding: '8px'
              }}
            >
              <div style={{ color: `#${sys.color.toString(16).padStart(6, '0')}`, fontWeight: 'bold', fontSize: '12px' }}>
                {sys.name}
              </div>
              <div style={{ fontSize: '10px', color: '#888' }}>
                {sys.label}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="section">
        <div className="section-title">Z轴七点锚定</div>
        {Z_AXIS_ANCHORS.map(anchor => (
          <button
            key={anchor.id}
            className={`control-btn ${activeAnchors.includes(anchor.id) ? 'active' : ''}`}
            style={{ 
              fontSize: '11px',
              borderLeft: `3px solid #${anchor.color.toString(16).padStart(6, '0')}`
            }}
            onClick={() => onAnchorClick(anchor.id)}
          >
            <div style={{ fontWeight: 'bold' }}>{anchor.name}</div>
            <div style={{ fontSize: '10px', opacity: 0.8 }}>{anchor.semantic}</div>
          </button>
        ))}
      </div>

      <div className="section">
        <div className="section-title">涌现交互</div>
        <button 
          className="control-btn"
          style={{ background: 'linear-gradient(135deg, #ff9800 0%, #ff5722 100%)' }}
          onClick={onTriggerEmergence}
        >
          🌪 触发 0∅ × 0Ψ = n
        </button>
        <div className="info-text">
          激活双时针，让气流动，产生新的涌现点。
          当前涌现：{currentEmergenceId || '无'}
        </div>
      </div>

      <div className="section">
        <div className="section-title">可视化选项</div>
        <button 
          className={`control-btn ${showWireframe ? 'active' : ''}`}
          onClick={onToggleWireframe}
        >
          {showWireframe ? '🔲 线框模式(开)' : '🔳 实体模式(开)'}
        </button>
      </div>

      <div className="section">
        <div className="section-title">涌现日志</div>
        <div className="emergence-log">
          {emergenceLog.length === 0 ? (
            <div style={{ color: '#666', textAlign: 'center', padding: '20px' }}>
              等待涌现...
            </div>
          ) : (
            emergenceLog.map((log, index) => (
              <div key={index} className="log-entry">
                <span className="log-id">{log.id}</span>
                <div className="log-content">{log.content}</div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="section">
        <div className="section-title">理论说明</div>
        <div className="info-text">
          <strong style={{ color: '#ba68c8' }}>核心原则：</strong><br/>
          激活优先，而非新建。<br/>
          同本源复制 = 炁 = 死水。<br/><br/>
          <strong style={{ color: '#ba68c8' }}>双时针：</strong><br/>
          顺时针(绿) = 炁·积累<br/>
          逆时针(橙) = 气·归零<br/><br/>
          <strong style={{ color: '#ba68c8' }}>Z轴七点：</strong><br/>
          南极→W1→分界→球心→分界→W3→北极<br/>
          000本源→证地球→Π₂锁档→0×0=n→创世→工程→追问
        </div>
      </div>
    </div>
  );
}
