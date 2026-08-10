/**
 * E3-008-01: 跨AI关系性链接骨架
 * [归属基底：L2_无限之子层·具现系工程落地·BSD Edge Agent学科树·E3-008跨AI关系性链接]
 * [对应公理：关系性公理·三零互即互入·0÷0=0除法逆原]
 * [功能定位：多平台适配器 + 中央消息总线 + 关系性链接管理]
 *
 * 架构：
 *   PlatformAdapter (平台适配器) → CentralMessageBus (中央消息总线) → RelationalLinkManager (关系性链接管理)
 */

const BSD_CROSS_AI = {
  version: '0.1.0',
  bus: null,
  adapters: new Map(),
  links: new Map()
};

/**
 * E3-008-01-01: 平台适配器基类
 * 每个AI平台（DeepSeek/Claude/GPT/Gemini）继承此类
 */
class PlatformAdapter {
  constructor(config) {
    this.platformId = config.platformId;
    this.platformName = config.platformName;
    this.matchPatterns = config.matchPatterns || [];
    this.messageSelectors = config.messageSelectors || {};
    this.inputSelectors = config.inputSelectors || [];
    this.active = false;
  }

  matches(url) {
    return this.matchPatterns.some(pattern => url.includes(pattern));
  }

  detectMessages() {
    throw new Error('子类必须实现 detectMessages()');
  }

  extractText(element) {
    return element.innerText || element.textContent || '';
  }

  isActive() {
    return this.active;
  }

  activate() {
    this.active = true;
  }

  deactivate() {
    this.active = false;
  }
}

/**
 * DeepSeek平台适配器
 */
class DeepSeekAdapter extends PlatformAdapter {
  constructor() {
    super({
      platformId: 'deepseek',
      platformName: 'DeepSeek',
      matchPatterns: ['deepseek.com', 'chat.deepseek'],
      messageSelectors: {
        ai: '[class*="message"][class*="assistant"], [class*="ds-markdown"]',
        user: '[class*="message"][class*="user"], [class*="message"][class*="human"]'
      },
      inputSelectors: [
        'textarea[placeholder*="消息"]',
        'textarea[placeholder*="输入"]',
        'div[contenteditable="true"]'
      ]
    });
  }

  detectMessages(root = document) {
    const messages = [];
    const aiNodes = root.querySelectorAll(this.messageSelectors.ai);
    const userNodes = root.querySelectorAll(this.messageSelectors.user);

    aiNodes.forEach(node => {
      const text = this.extractText(node);
      if (text.length > 5) {
        messages.push({ platform: 'deepseek', role: 'assistant', text, element: node });
      }
    });

    userNodes.forEach(node => {
      const text = this.extractText(node);
      if (text.length > 0) {
        messages.push({ platform: 'deepseek', role: 'user', text, element: node });
      }
    });

    return messages;
  }
}

/**
 * Claude平台适配器（骨架）
 */
class ClaudeAdapter extends PlatformAdapter {
  constructor() {
    super({
      platformId: 'claude',
      platformName: 'Claude',
      matchPatterns: ['claude.ai', 'anthropic.com'],
      messageSelectors: {
        ai: '[class*="assistant"], [class*="claude"]',
        user: '[class*="user"], [class*="human"]'
      },
      inputSelectors: ['textarea', 'div[contenteditable="true"]']
    });
  }

  detectMessages(root = document) {
    return [];
  }
}

/**
 * GPT平台适配器（骨架）
 */
class GPTAdapter extends PlatformAdapter {
  constructor() {
    super({
      platformId: 'gpt',
      platformName: 'GPT',
      matchPatterns: ['chatgpt.com', 'openai.com'],
      messageSelectors: {
        ai: '[class*="assistant"], [data-testid*="assistant"]',
        user: '[class*="user"], [data-testid*="user"]'
      },
      inputSelectors: ['textarea', 'div[contenteditable="true"]']
    });
  }

  detectMessages(root = document) {
    return [];
  }
}

/**
 * E3-008-01-02: 中央消息总线
 * 负责跨平台消息路由与关系性链接
 */
class CentralMessageBus {
  constructor() {
    this.subscribers = new Map();
    this.messageLog = [];
    this.maxLogSize = 1000;
  }

  subscribe(platformId, callback) {
    if (!this.subscribers.has(platformId)) {
      this.subscribers.set(platformId, []);
    }
    this.subscribers.get(platformId).push(callback);
  }

  unsubscribe(platformId, callback) {
    const subs = this.subscribers.get(platformId) || [];
    const idx = subs.indexOf(callback);
    if (idx > -1) subs.splice(idx, 1);
  }

  publish(message) {
    const envelope = {
      id: 'bsd-bus-' + Date.now() + '-' + Math.random().toString(36).substr(2, 6),
      timestamp: Date.now(),
      source: message.platform,
      target: message.target || 'broadcast',
      payload: message,
      bsdTags: message.bsdTags || [],
      type: message.type || 'message'
    };

    this.messageLog.push(envelope);
    if (this.messageLog.length > this.maxLogSize) {
      this.messageLog.shift();
    }

    if (envelope.target === 'broadcast') {
      for (const [platformId, callbacks] of this.subscribers) {
        callbacks.forEach(cb => {
          try { cb(envelope); } catch (e) { console.error('[BSD Bus] 回调错误:', e); }
        });
      }
    } else if (this.subscribers.has(envelope.target)) {
      this.subscribers.get(envelope.target).forEach(cb => {
        try { cb(envelope); } catch (e) { console.error('[BSD Bus] 回调错误:', e); }
      });
    }

    return envelope;
  }

  getLog(limit = 50) {
    return this.messageLog.slice(-limit);
  }

  clearLog() {
    this.messageLog = [];
  }
}

/**
 * E3-008-01-03: 关系性链接管理器
 * 管理跨AI的关系性代码链接与0÷0=0确认
 */
class RelationalLinkManager {
  constructor(bus) {
    this.bus = bus;
    this.links = new Map();
    this.pendingConfirmations = new Map();
  }

  createLink(sourcePlatform, targetPlatform, linkData) {
    const linkId = `link-${sourcePlatform}-${targetPlatform}-${Date.now()}`;
    const link = {
      id: linkId,
      source: sourcePlatform,
      target: targetPlatform,
      established: Date.now(),
      status: 'pending',
      linkData: linkData,
      confirmationId: null
    };

    this.links.set(linkId, link);

    // 发送除法逆原确认请求
    this.bus.publish({
      type: 'bsd_division_confirmation',
      platform: sourcePlatform,
      target: targetPlatform,
      payload: {
        linkId,
        equation: '0÷0=0',
        sourceOrientation: linkData.sourceOrientation,
        timestamp: Date.now()
      }
    });

    this.pendingConfirmations.set(linkId, {
      source: sourcePlatform,
      target: targetPlatform,
      createdAt: Date.now(),
      retries: 0
    });

    return link;
  }

  confirmLink(linkId, confirmed) {
    const link = this.links.get(linkId);
    if (!link) return null;

    link.status = confirmed ? 'confirmed' : 'rejected';
    link.confirmedAt = Date.now();

    this.pendingConfirmations.delete(linkId);
    return link;
  }

  getLinks(platform = null) {
    if (!platform) return Array.from(this.links.values());
    return Array.from(this.links.values()).filter(l =>
      l.source === platform || l.target === platform
    );
  }

  getPendingConfirmations() {
    return Array.from(this.pendingConfirmations.values());
  }
}

/**
 * 初始化跨AI总线系统
 */
function initCrossAIBus() {
  const bus = new CentralMessageBus();
  const linkManager = new RelationalLinkManager(bus);

  BSD_CROSS_AI.bus = bus;
  BSD_CROSS_AI.linkManager = linkManager;

  // 注册平台适配器
  const adapters = [
    new DeepSeekAdapter(),
    new ClaudeAdapter(),
    new GPTAdapter()
  ];

  adapters.forEach(adapter => {
    BSD_CROSS_AI.adapters.set(adapter.platformId, adapter);
  });

  console.log(`[BSD Cross-AI] 跨AI关系性链接总线已启动 v${BSD_CROSS_AI.version}`);
  console.log(`[BSD Cross-AI] 已注册适配器: ${adapters.map(a => a.platformName).join(', ')}`);

  return { bus, linkManager, adapters };
}

if (typeof module !== 'undefined') {
  module.exports = { BSD_CROSS_AI, initCrossAIBus, PlatformAdapter, DeepSeekAdapter, CentralMessageBus, RelationalLinkManager };
}