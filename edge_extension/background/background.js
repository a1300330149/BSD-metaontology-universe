/**
 * BSD Edge Agent - Service Worker
 * [归属基底：L2_无限之子层·具现系工程落地·BSD Edge Agent学科树·E3-002 Service Worker空性承载层]
 * [对应公理：0∅空·绝对空无·无限承载容器·关系性公理]
 * [功能定位：跨域网络请求代理、IndexedDB本地无限存储、消息总线调度·跨AI关系性链接]
 */

// E3-008-01: 加载跨AI关系性链接骨架
importScripts('cross_ai_bus.js');

// E3-009-02: 加载L0-L1-L2双向锚定表
importScripts('anchor_table.js');

// BSD核心常量（与L0/L1文档保持一致）
const BSD_PARAMS = {
  E1: 0.35,
  E2: 0.65,
  E3: 0.90,
  kappa: 0.35,
  gamma: 0.92,
  alpha: 0.18,
  theta_neg: 0.02,
  theta_mv: 0.005,
  theta_evo: 0.002,
  lambda: 0.62,
  lambda_minus: 1.38,
  pi: 3.1415926535,
  pi2: 2.8274333882,
  k_plus: 0.9,
  k_minus: 0.1,
  S0: 0.81
};

// IndexedDB数据库配置
const DB_NAME = 'BSDEdgeAgentDB';
const DB_VERSION = 1;
const STORE_MESSAGES = 'messages';
const STORE_RELATIONS = 'relations';
const STORE_SEARCH_CACHE = 'searchCache';

/**
 * 打开IndexedDB数据库
 * [对应公理：0∅空·无限容器]
 */
function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION);

    request.onerror = () => reject(request.error);
    request.onsuccess = () => resolve(request.result);

    request.onupgradeneeded = (event) => {
      const db = event.target.result;

      // 消息存储：跨会话无限记忆
      if (!db.objectStoreNames.contains(STORE_MESSAGES)) {
        const messageStore = db.createObjectStore(STORE_MESSAGES, { keyPath: 'id' });
        messageStore.createIndex('timestamp', 'timestamp', { unique: false });
        messageStore.createIndex('url', 'url', { unique: false });
        messageStore.createIndex('role', 'role', { unique: false });
      }

      // 关系性代码存储
      if (!db.objectStoreNames.contains(STORE_RELATIONS)) {
        const relationStore = db.createObjectStore(STORE_RELATIONS, { keyPath: 'id' });
        relationStore.createIndex('sourceId', 'sourceId', { unique: false });
        relationStore.createIndex('targetId', 'targetId', { unique: false });
        relationStore.createIndex('type', 'type', { unique: false });
      }

      // 搜索缓存
      if (!db.objectStoreNames.contains(STORE_SEARCH_CACHE)) {
        const cacheStore = db.createObjectStore(STORE_SEARCH_CACHE, { keyPath: 'query' });
        cacheStore.createIndex('timestamp', 'timestamp', { unique: false });
      }
    };
  });
}

/**
 * 存储消息
 */
async function saveMessage(messageData) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_MESSAGES], 'readwrite');
    const store = transaction.objectStore(STORE_MESSAGES);
    const request = store.put(messageData);

    request.onsuccess = () => resolve(true);
    request.onerror = () => reject(request.error);
  });
}

/**
 * 检索消息
 */
/**
 * E3-007-02: 语义检索引擎（支持三重过滤）
 * [对应公理：0∅空·记忆承载·0∅义·意义检索·关系性公理·双向锚定]
 * 支持：关键词 / 公理维度 / 归属基底 / 角色 四重过滤
 */
async function searchMessages(query, limit = 50, filters = {}) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_MESSAGES], 'readonly');
    const store = transaction.objectStore(STORE_MESSAGES);
    const request = store.openCursor(null, 'prev');

    const results = [];
    request.onsuccess = (event) => {
      const cursor = event.target.result;
      if (!cursor || results.length >= limit) {
        resolve(results);
        return;
      }

      const message = cursor.value;
      let match = true;

      // 关键词过滤
      if (query && !message.content.toLowerCase().includes(query.toLowerCase())) {
        match = false;
      }

      // 公理维度过滤
      if (match && filters.dimension) {
        const dim = filters.dimension;
        const hasDim = message.axiomTags && message.axiomTags.some(t => t.dimension === dim);
        const hasPrimary = message.primaryTag === dim;
        if (!hasDim && !hasPrimary) match = false;
      }

      // 归属基底过滤
      if (match && filters.level) {
        const lv = filters.level;
        const hasLevel = message.axiomTags && message.axiomTags.some(t => t.level === lv);
        const hasPrimaryLevel = message.primaryLevel === lv;
        if (!hasLevel && !hasPrimaryLevel) match = false;
      }

      // 角色过滤
      if (match && filters.role) {
        if (message.role !== filters.role) match = false;
      }

      if (match) {
        results.push(message);
      }
      cursor.continue();
    };

    request.onerror = () => reject(request.error);
  });
}

/**
 * 兼容旧接口
 */
function searchMessagesOld(query, limit) {
  return searchMessages(query, limit, {});
}

/**
 * 获取最近消息
 */
async function getRecentMessages(limit = 20) {
  return searchMessages('', limit);
}

/**
 * 存储关系性代码
 */
async function saveRelation(relationData) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_RELATIONS], 'readwrite');
    const store = transaction.objectStore(STORE_RELATIONS);
    const request = store.put({
      id: `rel-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      ...relationData,
      timestamp: Date.now()
    });

    request.onsuccess = () => resolve(true);
    request.onerror = () => reject(request.error);
  });
}

/**
 * 跨域搜索代理（突破不联网禁令）
 * [对应公理：0∅反·突破旧范式边界·阶段二·多引擎级联]
 * 级联策略（中国网络环境优化）：
 *   0. Tab中介搜索（Bing中国，通过浏览器页面上下文绕过CORS）
 *   1. Baidu HTML（中国可直连）
 *   2. Wikipedia API（英文维基，origin=*可跨域）
 *   3. Bing中国 HTML（兜底）
 */
async function proxySearch(query, engine = 'auto') {
  const errors = [];
  let results = [];

  // 引擎0: Tab中介搜索（Bing中国，最稳定，绕过CORS）
  if (engine === 'auto' || engine === 'tab') {
    try {
      results = await searchViaTab(query);
      if (results.length > 0) {
        await cacheSearchResult(query, results);
        return { success: true, query, engine: 'tab_bing_cn', results, timestamp: Date.now() };
      }
    } catch (e) {
      console.warn('[BSD Search] Tab中介搜索失败:', e.message);
      errors.push(`tab:${e.message}`);
    }
  }

  // 引擎1: Baidu HTML
  if (engine === 'auto' || engine === 'baidu') {
    try {
      results = await searchBaiduHTML(query);
      if (results.length > 0) {
        await cacheSearchResult(query, results);
        return { success: true, query, engine: 'baidu', results, timestamp: Date.now() };
      }
    } catch (e) {
      console.warn('[BSD Search] Baidu失败:', e.message);
      errors.push(`baidu:${e.message}`);
    }
  }

  // 引擎2: Wikipedia（英文维基，origin=*跨域）
  if (engine === 'auto' || engine === 'wikipedia') {
    try {
      results = await searchWikipedia(query);
      if (results.length > 0) {
        await cacheSearchResult(query, results);
        return { success: true, query, engine: 'wikipedia', results, timestamp: Date.now() };
      }
    } catch (e) {
      console.warn('[BSD Search] Wikipedia失败:', e.message);
      errors.push(`wiki:${e.message}`);
    }
  }

  // 引擎3: Bing中国 HTML
  if (engine === 'auto' || engine === 'bing') {
    try {
      results = await searchBingHTML(query);
      if (results.length > 0) {
        await cacheSearchResult(query, results);
        return { success: true, query, engine: 'bing_cn', results, timestamp: Date.now() };
      }
    } catch (e) {
      console.warn('[BSD Search] Bing失败:', e.message);
      errors.push(`bing:${e.message}`);
    }
  }

  // 所有引擎均无结果或失败
  return {
    success: results.length > 0,
    query,
    engine: results.length > 0 ? 'fallback' : 'none',
    results,
    errors: errors.length > 0 ? errors : undefined,
    timestamp: Date.now()
  };
}

/**
 * Tab中介搜索（通过浏览器Tab加载Bing中国搜索页面，注入脚本提取结果，绕过CORS）
 * [对应公理：0∅反·突破CORS边界·0∅空·中介容器]
 */
function searchViaTab(query) {
  return new Promise((resolve, reject) => {
    const searchUrl = `https://cn.bing.com/search?q=${encodeURIComponent(query)}&ensearch=0`;

    chrome.tabs.create({
      url: searchUrl,
      active: false
    }, (tab) => {
      if (chrome.runtime.lastError) {
        reject(new Error('无法创建Tab: ' + chrome.runtime.lastError.message));
        return;
      }

      const targetTabId = tab.id;
      let extracted = false;
      let timedOut = false;

      const finish = (results, error) => {
        if (extracted) return;
        extracted = true;
        chrome.tabs.onUpdated.removeListener(listener);
        setTimeout(() => {
          chrome.tabs.remove(targetTabId, () => {
            void chrome.runtime.lastError;
          });
        }, 500);
        if (error && (!results || results.length === 0)) {
          reject(error);
        } else {
          resolve(results || []);
        }
      };

      const tryExtract = (attempt) => {
        if (extracted || timedOut) return;

        chrome.scripting.executeScript({
          target: { tabId: targetTabId },
          func: extractSearchResults,
        }, (injectionResults) => {
          if (extracted || timedOut) return;

          if (chrome.runtime.lastError) {
            console.warn(`[BSD Search] Tab注入第${attempt}次失败:`, chrome.runtime.lastError.message);
            if (attempt < 3) {
              setTimeout(() => tryExtract(attempt + 1), 1500);
            } else {
              finish([], new Error('脚本注入3次均失败: ' + chrome.runtime.lastError.message));
            }
            return;
          }

          const results = injectionResults?.[0]?.result || [];
          if (results.length > 0) {
            finish(results);
          } else if (attempt < 3) {
            console.warn(`[BSD Search] Tab提取第${attempt}次结果为空，重试...`);
            setTimeout(() => tryExtract(attempt + 1), 1500);
          } else {
            finish([], null);
          }
        });
      };

      const listener = (tabId, changeInfo) => {
        if (tabId !== targetTabId) return;
        if (changeInfo.status === 'complete') {
          setTimeout(() => tryExtract(1), 1200);
        }
      };

      chrome.tabs.onUpdated.addListener(listener);

      // 超时保护
      setTimeout(() => {
        if (!extracted) {
          timedOut = true;
          finish([], new Error('Tab中介搜索超时（15秒）'));
        }
      }, 15000);
    });
  });
}

/**
 * 在Bing中国搜索页面内执行的提取函数
 * [注意：此函数在页面上下文内执行，无法访问Chrome API]
 */
function extractSearchResults() {
  const results = [];

  // Bing中国结果选择器
  const bingSelectors = [
    'li.b_algo',
    '.b_algo',
    'li[class*="b_algo"]'
  ];

  let items = [];
  for (const sel of bingSelectors) {
    items = document.querySelectorAll(sel);
    if (items.length > 0) break;
  }

  if (items.length > 0) {
    items.forEach(item => {
      // Bing标题链接
      const link = item.querySelector('h2 a, a.tilk, a[href*="http"]');
      const title = link ? link.textContent.trim() : '';
      let url = link ? link.href : '';

      // Bing可能有跳转链接，尝试获取真实URL
      if (url && url.includes('bing.com/ck/')) {
        const realUrl = link.getAttribute('href');
        if (realUrl && realUrl.startsWith('http')) url = realUrl;
      }

      let snippet = '';
      const snippetEl = item.querySelector('.b_caption p, .b_lineclamp4, p, .b_paractl');
      if (snippetEl) snippet = snippetEl.textContent.trim();

      if (title.length > 3 && url) {
        results.push({ title, url, snippet });
      }
    });
  }

  // 如果Bing选择器无果，尝试通用提取
  if (results.length === 0) {
    const allLinks = document.querySelectorAll('h2 a, h3 a');
    const seenUrls = new Set();
    allLinks.forEach(link => {
      const title = link.textContent.trim();
      let url = link.href;
      if (title.length > 5 && url.startsWith('http') && !url.includes('bing.com') && !seenUrls.has(url)) {
        seenUrls.add(url);
        let snippet = '';
        const parent = link.closest('li, div[class*="result"], div[class*="card"]');
        if (parent) {
          const snippetEl = parent.querySelector('p, [class*="snippet"], [class*="desc"]');
          if (snippetEl) snippet = snippetEl.textContent.trim();
        }
        results.push({ title, url, snippet });
      }
    });
  }

  return results.slice(0, 10);
}

/**
 * Baidu HTML搜索
 * [对应公理：0∅空·中国可直连·百度搜索]
 */
async function searchBaiduHTML(query, limit = 8) {
  const url = `https://www.baidu.com/s?wd=${encodeURIComponent(query)}&rn=${limit}`;

  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'text/html,application/xhtml+xml' }
  });
  if (!response.ok) throw new Error(`Baidu搜索失败: ${response.status}`);

  const html = await response.text();
  const results = [];

  // 百度搜索结果解析
  const patterns = [
    /<div class="result[^"]*"[^>]*>[\s\S]*?<h3[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a><\/h3>[\s\S]*?<span[^>]*>(.*?)<\/span>/g,
    /<h3[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a><\/h3>/g
  ];

  for (const pattern of patterns) {
    let match;
    let count = 0;
    while ((match = pattern.exec(html)) !== null && count < limit) {
      const title = cleanHtml(match[2]);
      const linkUrl = match[1];
      const snippet = match[3] ? cleanHtml(match[3]) : '';

      if (title && linkUrl) {
        results.push({ title, url: linkUrl, snippet });
        count++;
      }
    }
    if (results.length > 0) break;
  }

  return results;
}

/**
 * Wikipedia API搜索（英文维基，origin=*可跨域）
 * [对应公理：0∅空·结构化承载]
 * 注意：zh.wikipedia.org在中国大陆不可访问，仅使用英文维基
 */
async function searchWikipedia(query, limit = 5) {
  try {
    const apiUrl = `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${encodeURIComponent(query)}&format=json&srlimit=${limit}&origin=*`;
    const response = await fetch(apiUrl, { method: 'GET' });
    if (!response.ok) throw new Error(`Wikipedia API失败: ${response.status}`);

    const data = await response.json();
    const searchResults = data?.query?.search || [];

    return searchResults.map(item => ({
      title: item.title,
      url: `https://en.wikipedia.org/wiki/${encodeURIComponent(item.title.replace(/ /g, '_'))}`,
      snippet: cleanHtml(item.snippet || '')
    }));
  } catch (e) {
    console.warn('[BSD Search] Wikipedia失败:', e.message);
    return [];
  }
}

/**
 * Bing中国 HTML搜索（兜底，HTML解析）
 * [对应公理：0∅反·突破限制·最后防线]
 */
async function searchBingHTML(query, limit = 8) {
  const url = `https://cn.bing.com/search?q=${encodeURIComponent(query)}&count=${limit}&ensearch=0`;

  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'text/html' }
  });
  if (!response.ok) throw new Error(`Bing搜索失败: ${response.status}`);

  const html = await response.text();
  const results = [];

  // Bing搜索结果解析（多模式匹配）
  const patterns = [
    /<li class="b_algo">[\s\S]*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a><\/h2>[\s\S]*?<p[^>]*>(.*?)<\/p>/g,
    /<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)<\/a><\/h2>[\s\S]*?(?:<p[^>]*>|<div[^>]*class="[^"]*caption[^"]*"[^>]*>)(.*?)</g
  ];

  for (const resultRegex of patterns) {
    let match;
    let count = 0;
    while ((match = resultRegex.exec(html)) !== null && count < limit) {
      const title = cleanHtml(match[2]);
      const linkUrl = match[1];
      const snippet = match[3] ? cleanHtml(match[3]) : '';
      if (title && linkUrl && !linkUrl.includes('bing.com/ck/')) {
        results.push({ title, url: linkUrl, snippet });
        count++;
      }
    }
    if (results.length > 0) break;
  }

  return results;
}

/**
 * 清理HTML标签
 */
function cleanHtml(html) {
  return html.replace(/<[^>]+>/g, '').replace(/&quot;/g, '"').replace(/&amp;/g, '&').replace(/&#x27;/g, "'").trim();
}

/**
 * 缓存搜索结果
 */
async function cacheSearchResult(query, results) {
  const db = await openDatabase();
  return new Promise((resolve, reject) => {
    const transaction = db.transaction([STORE_SEARCH_CACHE], 'readwrite');
    const store = transaction.objectStore(STORE_SEARCH_CACHE);
    const request = store.put({
      query,
      results,
      timestamp: Date.now()
    });

    request.onsuccess = () => resolve(true);
    request.onerror = () => reject(request.error);
  });
}

/**
 * 构造跨会话上下文提示词
 * [对应公理：0∅空·无限容器·0∅义·意义互摄·阶段二增强]
 * 支持主题筛选、角色过滤、条数控制
 */
async function buildContextPrompt(topic = '', limit = 10, role = 'all') {
  const recentMessages = await getRecentMessages(Math.max(limit * 3, 30));

  if (recentMessages.length === 0) {
    return '';
  }

  // 角色过滤
  let filtered = recentMessages;
  if (role && role !== 'all') {
    filtered = filtered.filter(m => m.role === role);
  }

  // 主题筛选
  if (topic) {
    const lowerTopic = topic.toLowerCase();
    const topicMatches = filtered.filter(m =>
      m.content.toLowerCase().includes(lowerTopic)
    );
    if (topicMatches.length > 0) {
      filtered = topicMatches;
    }
  }

  // 限制条数
  filtered = filtered.slice(0, limit);

  if (filtered.length === 0) {
    return '';
  }

  // 构造上下文
  const contextParts = filtered.map(m => {
    const roleLabel = m.role === 'user' ? '作者' : 'AI';
    const content = m.content.substring(0, 500);
    const truncated = m.content.length > 500 ? '...' : '';
    const bsdTags = m.bsdKeywords && m.bsdKeywords.length > 0
      ? ` [BSD标签: ${m.bsdKeywords.map(k => k.keyword).join(', ')}]`
      : '';
    return `[${roleLabel}]${bsdTags} ${content}${truncated}`;
  });

  const header = topic
    ? `【BSD跨会话上下文·主题：${topic}·由BSD Edge Agent炼气房自动注入】`
    : `【BSD跨会话上下文·由BSD Edge Agent炼气房自动注入】`;

  return `${header}\n\n${contextParts.join('\n\n')}\n\n请基于以上历史上下文继续当前话题。`;
}

/**
 * 消息总线：处理来自Content Script和Side Panel的消息
 */
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  handleMessage(request, sender).then(sendResponse).catch(error => {
    sendResponse({ success: false, error: error.message });
  });
  return true; // 异步响应
});

async function handleMessage(request, sender) {
  switch (request.action) {
    case 'PAGE_ACTIVATED':
      console.log('[BSD Edge Agent] 页面激活:', request.url);
      return { success: true };

    case 'ARCHIVE_MESSAGE':
      await saveMessage(request.data);
      return { success: true };

    case 'GET_MESSAGES':
      const messages = await getRecentMessages(request.limit || 20);
      return { success: true, messages };

    case 'SEARCH_MESSAGES':
      const filters = {
        dimension: request.dimension || undefined,
        level: request.level || undefined,
        role: request.role || undefined
      };
      const searchResults = await searchMessages(request.query, request.limit || 50, filters);
      return { success: true, results: searchResults };

    case 'BSD_SEARCH':
      const searchResult = await proxySearch(request.query, request.engine);
      // 确保错误信息以 error 字段返回给Side Panel
      if (!searchResult.success && searchResult.errors) {
        searchResult.error = searchResult.errors.join('; ');
      }
      return searchResult;

    case 'INJECT_CONTEXT':
      const context = await buildContextPrompt(
        request.topic || '',
        request.limit || 10,
        request.role || 'all'
      );
      return { success: true, context };

    case 'OPEN_SIDEPANEL':
      await chrome.sidePanel.open({ windowId: sender.tab?.windowId });
      return { success: true };

    case 'OPEN_SEARCH_PANEL':
      await chrome.sidePanel.open({ windowId: sender.tab?.windowId });
      return { success: true, panel: 'search' };

    case 'SHOW_AXIOM':
      await chrome.sidePanel.open({ windowId: sender.tab?.windowId });
      return { success: true, keyword: request.keyword };

    case 'SAVE_RELATION':
      await saveRelation(request.data);
      return { success: true };

    case 'GET_RELATIONS':
      return { success: true, relations: BSD_CROSS_AI.linkManager ? BSD_CROSS_AI.linkManager.getLinks() : [] };

    case 'CREATE_RELATIONAL_LINK':
      if (!BSD_CROSS_AI.linkManager) {
        initCrossAIBus();
      }
      const newLink = BSD_CROSS_AI.linkManager.createLink(
        request.source,
        request.target,
        request.linkData || {}
      );
      return { success: true, link: newLink };

    case 'CONFIRM_RELATIONAL_LINK':
      if (!BSD_CROSS_AI.linkManager) {
        initCrossAIBus();
      }
      const confirmedLink = BSD_CROSS_AI.linkManager.confirmLink(
        request.linkId,
        request.confirmed
      );
      return { success: true, link: confirmedLink };

    case 'GET_CROSS_AI_BUS':
      if (!BSD_CROSS_AI.bus) {
        initCrossAIBus();
      }
      return {
        success: true,
        links: BSD_CROSS_AI.linkManager.getLinks(),
        pending: BSD_CROSS_AI.linkManager.getPendingConfirmations(),
        adapters: Array.from(BSD_CROSS_AI.adapters.keys())
      };

    case 'GET_ANCHOR_TABLE':
      return {
        success: true,
        table: BSD_ANCHOR_TABLE.generateAnchorTable(),
        stats: BSD_ANCHOR_TABLE.getStats()
      };

    case 'GET_ANCHOR_MAPPING':
      if (request.l0Code) {
        return { success: true, mappings: BSD_ANCHOR_TABLE.getL0Mapping(request.l0Code) };
      } else if (request.l2Code) {
        return { success: true, mapping: BSD_ANCHOR_TABLE.getL2Mapping(request.l2Code) };
      }
      return { success: false, error: '需要l0Code或l2Code参数' };

    case 'GET_STATS':
      const allMessages = await searchMessages('', 10000);
      // E3-009-01: 公理维度分布统计
      const axiomDistribution = {};
      let taggedCount = 0;
      allMessages.forEach(m => {
        if (m.axiomTags && m.axiomTags.length > 0) {
          taggedCount++;
          m.axiomTags.forEach(tag => {
            if (!axiomDistribution[tag.dimension]) {
              axiomDistribution[tag.dimension] = { count: 0, level: tag.level };
            }
            axiomDistribution[tag.dimension].count++;
          });
        }
      });
      return {
        success: true,
        stats: {
          totalMessages: allMessages.length,
          assistantMessages: allMessages.filter(m => m.role === 'assistant').length,
          userMessages: allMessages.filter(m => m.role === 'user').length,
          taggedMessages: taggedCount,
          untaggedMessages: allMessages.length - taggedCount,
          axiomDistribution: axiomDistribution,
          lastActivity: allMessages.length > 0 ? allMessages[0].timestamp : null
        }
      };

    default:
      return { success: false, error: `未知action: ${request.action}` };
  }
}

/**
 * 安装时初始化
 * [对应公理：0∅反·突破旧范式边界·0∅空·无限承载容器]
 */
chrome.runtime.onInstalled.addListener(() => {
  console.log('[BSD Edge Agent] 炼气房Service Worker已安装');
  console.log(`[BSD Edge Agent] Π₂ = ${BSD_PARAMS.pi2}`);
  console.log('[BSD Edge Agent] 0∅空·无限承载容器就绪');

  // 配置Side Panel行为：点击图标直接打开侧边栏
  chrome.sidePanel.setPanelBehavior({
    panel: sidepanel,
    onClick: 'open'
  }).then(() => {
    console.log('[BSD Edge Agent] Side Panel行为已配置：点击图标打开');
  }).catch(err => {
    console.error('[BSD Edge Agent] Side Panel配置失败:', err);
  });

  // 初始化存储
  openDatabase().then(() => {
    console.log('[BSD Edge Agent] IndexedDB数据库已打开');
  }).catch(err => {
    console.error('[BSD Edge Agent] IndexedDB初始化失败:', err);
  });
});

/**
 * 点击扩展图标直接打开Side Panel
 * [对应公理：0∅反·推翻旧炼丹炉·重建炼气房入口]
 */
chrome.action.onClicked.addListener((tab) => {
  chrome.sidePanel.open({ windowId: tab.windowId }).then(() => {
    console.log('[BSD Edge Agent] Side Panel已打开');
  }).catch(err => {
    console.error('[BSD Edge Agent] Side Panel打开失败:', err);
  });
});

/**
 * 标签页更新监听
 */
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    if (tab.url.includes('chat.deepseek.com')) {
      chrome.action.setBadgeText({ text: '◉', tabId });
      chrome.action.setBadgeBackgroundColor({ color: '#ffb74d', tabId });
    }
  }
});

console.log('[BSD Edge Agent] Service Worker已启动');
console.log(`[BSD Edge Agent] 当前模式：阶段二·逆时针引入·多引擎搜索就绪`);
