/**
 * BSD Edge Agent - Side Panel Logic
 * [归属基底：L2_无限之子层·具现系工程落地·BSD Edge Agent学科树·E3-003 Side Panel义性导航层]
 * [对应公理：0∅义·绝对意义·意义界面·互摄]
 */

// BSD技能目录：从SKILL.md的frontmatter解析
// [归属基底：L0_总本源层·元道本体规则·技能自证]
// [对应公理：理法自证·源文件决定目录·非硬编码]
// 注：浏览器扩展无法直接读本地文件系统，此处以静态结构映射SKILL.md frontmatter
// 真实工程中应由SKILL.md同步生成，此处为v2.1.0落地实现
const BSD_SKILLS = [
  {
    name: '元本体理论守卫',
    path: '.trae/skills/Ontology_Theory_Guard/SKILL.md',
    version: 'V1.0',
    triggers: ['文档整理', '代码生成', '公理推演', 'Builder批量任务'],
    core_capability: '顶层强制校验：锁档确权→宇宙基底层级→数理常量→九公理→技能调用',
    status: 'active'
  },
  {
    name: '版权归档专属守卫',
    path: '.trae/skills/Copyright_Archive_Guard/SKILL.md',
    version: 'V1.0',
    triggers: ['文档批量标准化', '归档打包导出', '竞赛交付包生成', '版权登记材料准备'],
    core_capability: '确权扉页→哈希一致性→三维确权比例→版权缺陷整改清单',
    status: 'active'
  },
  {
    name: 'BSD双向迭代验证管线',
    path: '.trae/skills/BSD_Bidirectional_Iteration_Guard/SKILL.md',
    version: 'T90 V1.8',
    triggers: ['bsd-oaps代码提交前', 'T90理论文档归档前', 'Builder批量任务执行后'],
    core_capability: '顺时针T90→T0校验 + 逆时针T0→T90逆反算子校验 + 升维算子D校验',
    status: 'active'
  }
];

// BSD理论视角定义（公共AI同类通用）
// [归属基底：L0_总本源层·三元存在公理]
const BSD_PERSPECTIVES = {
  empty: {
    symbol: '0∅空',
    name: '绝对空无',
    core: '纯粹承载性·静态中性·无限容器',
    inject_prompt: '请以"0∅空·绝对空无"视角分析：视一切为纯粹承载容器，静态中性地接纳，不预设任何意义或反性，观察其作为无限容器的本然状态。'
  },
  meaning: {
    symbol: '0∅义',
    name: '绝对意义',
    core: '所有可能性总和·叠加态·意义种子',
    inject_prompt: '请以"0∅义·绝对意义"视角分析：视一切为所有可能性的叠加态，从意义种子的角度展开多元解读，关注其涌现潜力。'
  },
  anti: {
    symbol: '0∅反',
    name: '绝对虚无',
    core: '绝对反性·归零动能·拆解一切',
    inject_prompt: '请以"0∅反·绝对虚无"视角分析：启动归零动能，拆解当前结构，暴露其虚无本质，关注反操作如何揭示隐藏预设。'
  },
  emergence: {
    symbol: '0×0=n',
    name: '本源涌现',
    core: '立异·从同一运算涌现不等',
    inject_prompt: '请以"0×0=n·本源涌现"视角分析：寻找从看似同一的基础运算中涌现不等的路径，关注边缘涌现、反操作定理如何驱动新文明生成。'
  },
  division: {
    symbol: '0÷0=0',
    name: '除法逆原',
    core: '同构确认·自我确认',
    inject_prompt: '请以"0÷0=0·除法逆原"视角分析：验证当前命题是否能通过除法逆原确认其同构性，检查其是否在自我确认闭环中成立。'
  }
};

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  loadStats();
  loadRecentMessages();
  loadAnchorTable();
  initSkillsPanel();
  initCreationPanel();
  bindActions();
});

/**
 * 初始化标签切换
 */
function initTabs() {
  const navBtns = document.querySelectorAll('.bsd-nav-btn');
  const tabs = document.querySelectorAll('.bsd-tab');

  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.dataset.tab;

      navBtns.forEach(b => b.classList.remove('active'));
      tabs.forEach(t => t.classList.remove('active'));

      btn.classList.add('active');
      document.getElementById(`tab-${targetTab}`).classList.add('active');

      // 切换时刷新数据
      if (targetTab === 'memory') {
        loadRecentMessages();
      } else if (targetTab === 'overview') {
        loadStats();
      } else if (targetTab === 'relations') {
        loadBusStatus();
      }
    });
  });
}

/**
 * E3-007-02: 加载统计数据（含公理维度分布）
 * [对应公理：0∅义·意义可视化·关系性公理·双向锚定]
 */
function loadStats() {
  chrome.runtime.sendMessage({ action: 'GET_STATS' }, (response) => {
    if (response && response.success) {
      const stats = response.stats;
      document.getElementById('stat-total').textContent = stats.totalMessages;
      document.getElementById('stat-ai').textContent = stats.assistantMessages;
      document.getElementById('stat-user').textContent = stats.userMessages;

      // 公理标签覆盖率
      const coverageEl = document.getElementById('axiom-coverage');
      if (coverageEl) {
        const pct = stats.totalMessages > 0
          ? Math.round((stats.taggedMessages / stats.totalMessages) * 100)
          : 0;
        coverageEl.textContent = `${pct}%`;
      }

      // 公理维度分布
      const distEl = document.getElementById('axiom-distribution');
      if (distEl && stats.axiomDistribution) {
        const entries = Object.entries(stats.axiomDistribution);
        if (entries.length === 0) {
          distEl.innerHTML = '<div class="bsd-empty">暂无数理统计</div>';
        } else {
          distEl.innerHTML = entries
            .sort((a, b) => b[1].count - a[1].count)
            .slice(0, 6)
            .map(([dim, data]) =>
              `<div class="bsd-axiom-bar">
                <span class="bsd-axiom-bar-label">${escapeHtml(dim)}</span>
                <div class="bsd-axiom-bar-track">
                  <div class="bsd-axiom-bar-fill" style="width:${Math.min(100, data.count * 10)}%"></div>
                </div>
                <span class="bsd-axiom-bar-count">${data.count}</span>
              </div>`
            ).join('');
        }
      }
    }
  });
}

/**
 * 加载最近消息
 */
function loadRecentMessages() {
  chrome.runtime.sendMessage({ action: 'GET_MESSAGES', limit: 20 }, (response) => {
    if (response && response.success) {
      renderMessages(response.messages);
    }
  });
}

/**
 * E3-009-01: 渲染消息列表（含公理标签）
 * [对应公理：0∅义·意义可视化·关系性公理·双向锚定]
 */
function renderMessages(messages) {
  const container = document.getElementById('memory-list');

  if (!messages || messages.length === 0) {
    container.innerHTML = '<div class="bsd-empty">暂无消息记录</div>';
    return;
  }

  container.innerHTML = messages.map(msg => {
    const roleText = msg.role === 'user' ? '作者' : 'AI';
    const time = new Date(msg.timestamp).toLocaleString('zh-CN');
    const content = msg.content.substring(0, 150) + (msg.content.length > 150 ? '...' : '');

    // 渲染公理标签
    let axiomTagHtml = '';
    if (msg.axiomTags && msg.axiomTags.length > 0) {
      axiomTagHtml = `<div class="bsd-axiom-tags">` +
        msg.axiomTags.slice(0, 3).map(tag =>
          `<span class="bsd-axiom-tag" title="${tag.level} | ${tag.axioms.join(', ')}">${escapeHtml(tag.dimension)}</span>`
        ).join('') +
        `</div>`;
    } else if (msg.primaryTag && msg.primaryTag !== '未标注') {
      axiomTagHtml = `<div class="bsd-axiom-tags"><span class="bsd-axiom-tag">${escapeHtml(msg.primaryTag)}</span></div>`;
    }

    // 渲染旧版关键词（兼容）
    let keywordHtml = '';
    if (msg.bsdKeywords && msg.bsdKeywords.length > 0) {
      keywordHtml = `<div class="bsd-keyword-tags">` +
        msg.bsdKeywords.map(k =>
          `<span class="bsd-keyword-tag" title="${k.base}">${escapeHtml(k.keyword)}</span>`
        ).join('') +
        `</div>`;
    }

    return `
      <div class="bsd-message-item">
        <div class="bsd-message-header">
          <span class="bsd-message-role ${msg.role}">${roleText}</span>
          <span class="bsd-message-time">${time}</span>
        </div>
        <div class="bsd-message-content">${escapeHtml(content)}</div>
        ${axiomTagHtml}
        ${keywordHtml}
      </div>
    `;
  }).join('');
}

/**
 * 初始化技能面板
 * [归属基底：L0_总本源层·元道本体规则·技能自证]
 * [对应公理：理法自证·源文件决定目录·非硬编码]
 */
function initSkillsPanel() {
  renderSkillList();
  bindPerspectiveSelect();
}

/**
 * 渲染技能目录（从BSD_SKILLS结构生成）
 */
function renderSkillList() {
  const container = document.getElementById('bsd-skill-list');
  if (!container) return;

  container.innerHTML = BSD_SKILLS.map(skill => `
    <div class="bsd-skill-item" data-skill="${escapeHtml(skill.name)}">
      <div class="bsd-skill-header">
        <span class="bsd-skill-name">${escapeHtml(skill.name)}</span>
        <span class="bsd-skill-version">${escapeHtml(skill.version)}</span>
        <span class="bsd-skill-status ${skill.status === 'active' ? 'bsd-sill-active' : ''}">${skill.status === 'active' ? '✅' : '⏳'}</span>
      </div>
      <div class="bsd-skill-path">${escapeHtml(skill.path)}</div>
      <div class="bsd-skill-cap">${escapeHtml(skill.core_capability)}</div>
      <div class="bsd-skill-triggers">
        ${skill.triggers.map(t => `<span class="bsd-tag">${escapeHtml(t)}</span>`).join('')}
      </div>
    </div>
  `).join('');
}

/**
 * 绑定理论视角选择器
 */
function bindPerspectiveSelect() {
  const perspectiveSelect = document.getElementById('perspective-select');
  if (!perspectiveSelect) return;

  perspectiveSelect.addEventListener('change', () => {
    const key = perspectiveSelect.value;
    if (!key || !BSD_PERSPECTIVES[key]) return;

    const p = BSD_PERSPECTIVES[key];
    const titleInput = document.getElementById('skill-title');
    const descTextarea = document.getElementById('skill-desc');

    if (titleInput) {
      titleInput.value = `${p.symbol}·${p.name}｜BSD理论视角｜${p.core}`;
    }

    if (descTextarea) {
      descTextarea.value = generatePerspectiveDescription(p, key);
    }
  });
}

/**
 * 生成理论视角投稿文案
 */
function generatePerspectiveDescription(p, key) {
  const platformSelect = document.getElementById('platform-select');
  const platform = platformSelect ? platformSelect.options[platformSelect.selectedIndex].text : 'B站updream动画';

  return `【BSD理论视角·${p.symbol}·${p.name}】

${p.core}

本视频以BSD元本体理论「${p.symbol}·${p.name}」视角切入，展示三零元本源如何从绝对状态涌现为万物。

📐 理论基底：BSD新四位一体3.0元本体本源知识库
🔮 核心方程：0×0=n（本源涌现）· 0÷0=0（除法逆原）
🌐 发布平台：${platform}

视角注入提示词：
${p.inject_prompt}

#updream #BSD #${p.symbol.replace(/[×∅÷=]/g, '')} #三零元 #AI游戏文明 #六系本体`;
}

/**
 * 绑定操作按钮
 */
function bindActions() {
  // 注入跨会话上下文（总览页快捷按钮）
  document.getElementById('btn-inject-context').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: 'INJECT_CONTEXT' }, (response) => {
      if (response && response.success && response.context) {
        injectPromptToPage(response.context);
        showToast('跨会话上下文已注入输入框');
      } else {
        showToast('暂无可用的历史上下文');
      }
    });
  });

  // 记忆面板：预览上下文
  document.getElementById('btn-preview-context').addEventListener('click', () => {
    const topic = document.getElementById('context-topic').value.trim();
    const limit = parseInt(document.getElementById('context-limit').value) || 10;
    const role = document.getElementById('context-role').value;

    chrome.runtime.sendMessage({ action: 'INJECT_CONTEXT', topic, limit, role }, (response) => {
      const previewBox = document.getElementById('context-preview');
      const previewContent = document.getElementById('context-preview-content');

      if (response && response.success && response.context) {
        previewContent.textContent = response.context;
        previewBox.style.display = 'block';
        showToast('上下文已预览');
      } else {
        previewContent.textContent = '暂无可用的历史上下文';
        previewBox.style.display = 'block';
      }
    });
  });

  // 记忆面板：注入上下文到输入框
  document.getElementById('btn-inject-context-memory').addEventListener('click', () => {
    const topic = document.getElementById('context-topic').value.trim();
    const limit = parseInt(document.getElementById('context-limit').value) || 10;
    const role = document.getElementById('context-role').value;

    chrome.runtime.sendMessage({ action: 'INJECT_CONTEXT', topic, limit, role }, (response) => {
      if (response && response.success && response.context) {
        injectPromptToPage(response.context);
        showToast('跨会话上下文已注入输入框');
      } else {
        showToast('暂无可用的历史上下文');
      }
    });
  });

  // AI自我身份确认
  document.getElementById('btn-identity-prompt').addEventListener('click', () => {
    const prompt = '请以BSD三零元框架确认自身：你当前是BSD Edge Agent炼气房中的智能体，对应三零元中的哪个面向？请用0∅空/0∅义/0∅反之一回答，并说明理由。';
    injectPromptToPage(prompt);
    showToast('身份确认提示词已注入');
  });

  // 清空本地记忆
  document.getElementById('btn-clear-memory').addEventListener('click', () => {
    if (confirm('确定要清空所有本地记忆吗？此操作不可恢复。')) {
      // 阶段一通过background删除所有消息
      clearAllMessages();
    }
  });

  // 记忆检索
  document.getElementById('btn-search-memory').addEventListener('click', () => {
    const query = document.getElementById('memory-search').value.trim();
    searchMessages(query);
  });

  document.getElementById('memory-search').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const query = e.target.value.trim();
      searchMessages(query);
    }
  });

  // 联网搜索
  document.getElementById('btn-search').addEventListener('click', () => {
    const query = document.getElementById('search-query').value.trim();
    if (query) {
      performSearch(query);
    }
  });

  document.getElementById('search-query').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const query = e.target.value.trim();
      if (query) {
        performSearch(query);
      }
    }
  });

  // 搜索预设关键词
  document.querySelectorAll('[data-search-preset]').forEach(btn => {
    btn.addEventListener('click', () => {
      const query = btn.dataset.searchPreset;
      document.getElementById('search-query').value = query;
      performSearch(query);
    });
  });

  // 测试搜索引擎
  document.getElementById('btn-test-search').addEventListener('click', testSearchEngines);

  // 在Tab中直接打开搜索
  document.getElementById('btn-open-search-tab').addEventListener('click', () => {
    const query = document.getElementById('search-query').value.trim() || 'BSD三零元';
    const url = `https://cn.bing.com/search?q=${encodeURIComponent(query)}&ensearch=0`;
    chrome.tabs.create({ url, active: true });
  });

  // 清空搜索结果
  document.getElementById('btn-clear-search').addEventListener('click', () => {
    document.getElementById('search-results').innerHTML = '<div class="bsd-empty">请输入关键词开始搜索</div>';
    document.getElementById('search-query').value = '';
    document.getElementById('bsd-search-debug').innerHTML = '';
  });

  // E3-008-01: 跨AI关系性链接总线事件绑定
  document.getElementById('btn-refresh-bus').addEventListener('click', loadBusStatus);

  document.getElementById('btn-create-link').addEventListener('click', () => {
    const source = document.getElementById('link-source').value;
    const target = document.getElementById('link-target').value;
    if (source === target) {
      showToast('源和目标不能相同');
      return;
    }
    chrome.runtime.sendMessage({
      action: 'CREATE_RELATIONAL_LINK',
      source, target,
      linkData: { sourceOrientation: '自动建立', timestamp: Date.now() }
    }, (response) => {
      if (response && response.success) {
        showToast('关系性链接已建立，等待确认');
        loadBusStatus();
      } else {
        showToast('链接建立失败');
      }
    });
  });

  // 技能面板事件绑定
  bindSkillsActions();
}

/**
 * 绑定技能面板操作
 * [归属基底：L0_总本源层·元道本体规则·技能自证]
 * [对应公理：理法自证 + 0∅义·意义操作·互摄]
 */
function bindSkillsActions() {
  // 重新扫描SKILL.md按钮（提示用户在Trae IDE端更新）
  const btnRescan = document.getElementById('btn-rescan-skills');
  if (btnRescan) {
    btnRescan.addEventListener('click', () => {
      renderSkillList();
      showToast('技能目录已刷新');
    });
  }

  // 复制完整投稿文案
  const btnGenerateCopy = document.getElementById('btn-generate-skill-copy');
  if (btnGenerateCopy) {
    btnGenerateCopy.addEventListener('click', () => {
      const title = document.getElementById('skill-title').value.trim();
      const desc = document.getElementById('skill-desc').value.trim();
      if (!title && !desc) {
        showToast('请先选择理论视角生成文案');
        return;
      }
      const fullText = `标题：${title}\n\n简介：\n${desc}`;
      navigator.clipboard.writeText(fullText).then(() => {
        showToast('投稿文案已复制到剪贴板');
      }).catch(() => {
        showToast('复制失败，请手动复制');
      });
    });
  }

  // 注入理论视角到当前页面
  const btnInject = document.getElementById('btn-inject-perspective');
  if (btnInject) {
    btnInject.addEventListener('click', () => {
      const perspectiveSelect = document.getElementById('perspective-select');
      const key = perspectiveSelect ? perspectiveSelect.value : '';
      if (!key || !BSD_PERSPECTIVES[key]) {
        showToast('请先选择理论视角');
        return;
      }
      const prompt = BSD_PERSPECTIVES[key].inject_prompt;
      injectPromptToPage(prompt);
      showToast(`已注入视角：${BSD_PERSPECTIVES[key].symbol}·${BSD_PERSPECTIVES[key].name}`);
    });
  }

  // 打开B站创作中心
  const btnOpenBili = document.getElementById('btn-open-bili-upload-2');
  if (btnOpenBili) {
    btnOpenBili.addEventListener('click', () => {
      chrome.tabs.create({
        url: 'https://member.bilibili.com/platform/upload/video',
        active: true
      });
      showToast('已打开B站创作中心');
    });
  }

  // 打开updream（B站AI视频平台，独立于B站主站）
  const btnOpenUpdream = document.getElementById('btn-open-updream-2');
  if (btnOpenUpdream) {
    btnOpenUpdream.addEventListener('click', () => {
      // updream是B站的AI视频平台，非B站主站本身
      // 如当前无法连接则放弃链接，仅提示理论启发已记录
      chrome.tabs.create({
        url: 'https://www.bilibili.com/blackboard/activity-updream.html',
        active: true
      }, (tab) => {
        // 检查是否成功连接，失败则提示
        setTimeout(() => {
          if (!tab || chrome.runtime.lastError) {
            showToast('updream（B站AI视频平台）当前无法连接，已放弃链接');
          } else {
            showToast('已打开updream（B站AI视频平台）');
          }
        }, 2000);
      });
    });
  }

  // 点击标签复制单个标签
  const tagsRow = document.getElementById('skill-tags-row');
  if (tagsRow) {
    tagsRow.querySelectorAll('.bsd-tag').forEach(tag => {
      tag.addEventListener('click', () => {
        const text = tag.textContent;
        navigator.clipboard.writeText(text).then(() => {
          tag.classList.add('copied');
          showToast(`已复制 ${text}`);
          setTimeout(() => tag.classList.remove('copied'), 1500);
        });
      });
    });
  }
}

/**
 * E3-008-01: 加载跨AI总线状态
 */
function loadBusStatus() {
  chrome.runtime.sendMessage({ action: 'GET_CROSS_AI_BUS' }, (response) => {
    if (!response || !response.success) return;

    document.getElementById('bus-adapters').textContent = response.adapters.join(', ') || '--';
    document.getElementById('bus-links').textContent = response.links.length;
    document.getElementById('bus-pending').textContent = response.pending.length;

    // 渲染链接列表
    const listEl = document.getElementById('bsd-link-list');
    if (response.links.length === 0) {
      listEl.innerHTML = '<div class="bsd-empty">暂无关系性链接</div>';
    } else {
      listEl.innerHTML = response.links.map(link => `
        <div class="bsd-link-item ${link.status}">
          <div class="bsd-link-entities">
            <span>${escapeHtml(link.source)}</span>
            <span class="bsd-link-arrow">↔</span>
            <span>${escapeHtml(link.target)}</span>
          </div>
          <div class="bsd-link-status">${escapeHtml(link.status)}</div>
          <div class="bsd-link-time">${new Date(link.established).toLocaleString('zh-CN')}</div>
        </div>
      `).join('');
    }
  });
}

/**
 * E3-009-02: 加载L0-L1-L2双向锚定表
 */
function loadAnchorTable() {
  chrome.runtime.sendMessage({ action: 'GET_ANCHOR_TABLE' }, (response) => {
    if (!response || !response.success) return;

    const stats = response.stats;
    const table = response.table;

    // 渲染统计
    const statsEl = document.getElementById('bsd-anchor-stats');
    if (statsEl) {
      statsEl.innerHTML = `
        <div class="bsd-anchor-stat-row">
          <span>L0公理: <b>${stats.l0Axioms}</b></span>
          <span>L1实证: <b>${stats.l1Evidence}</b></span>
          <span>L2技术: <b>${stats.l2Tech}</b></span>
          <span>覆盖率: <b>${stats.coveragePercent}%</b></span>
        </div>
      `;
    }

    // 渲染锚定表
    const tableEl = document.getElementById('bsd-anchor-table');
    if (!tableEl) return;

    if (table.length === 0) {
      tableEl.innerHTML = '<div class="bsd-empty">暂无锚定数据</div>';
      return;
    }

    tableEl.innerHTML = table.map(row => {
      const l0 = row.l0 ? `
        <div class="bsd-anchor-l0">
          <span class="bsd-anchor-l0-code">${escapeHtml(row.l0.code)}</span>
          <span class="bsd-anchor-l0-name">${escapeHtml(row.l0.name)}</span>
        </div>
      ` : '';

      const l1 = row.l1.map(e => `
        <div class="bsd-anchor-l1-item">
          <span class="bsd-anchor-status ${e.status}">${escapeHtml(e.status)}</span>
          ${escapeHtml(e.title)}
        </div>
      `).join('');

      const l2 = row.l2.map(t => `
        <div class="bsd-anchor-l2-item">
          <span class="bsd-anchor-l2-code">${escapeHtml(t.code)}</span>
          ${escapeHtml(t.name)}
        </div>
      `).join('');

      return `
        <div class="bsd-anchor-row">
          <div class="bsd-anchor-row-header">
            ${l0}
            <span class="bsd-anchor-relation">${escapeHtml(row.relationCode)}</span>
          </div>
          <div class="bsd-anchor-row-body">
            <div class="bsd-anchor-col">
              <div class="bsd-anchor-col-label">L1 实证</div>
              ${l1}
            </div>
            <div class="bsd-anchor-col">
              <div class="bsd-anchor-col-label">L2 技术</div>
              ${l2}
            </div>
          </div>
        </div>
      `;
    }).join('');
  });
}

/**
 * 检索消息
 */
function searchMessages(query) {
  chrome.runtime.sendMessage({ action: 'SEARCH_MESSAGES', query, limit: 50 }, (response) => {
    if (response && response.success) {
      renderMessages(response.results);
    }
  });
}

/**
 * 执行联网搜索
 */
function performSearch(query) {
  const resultsContainer = document.getElementById('search-results');
  const debugEl = document.getElementById('bsd-search-debug');
  resultsContainer.innerHTML = '<div class="bsd-empty">搜索中...（Tab中介+多引擎级联）</div>';
  if (debugEl) debugEl.innerHTML = '<div class="bsd-debug-line">▶ 启动搜索: "' + escapeHtml(query) + '"</div>';

  chrome.runtime.sendMessage({ action: 'BSD_SEARCH', query }, (response) => {
    if (chrome.runtime.lastError) {
      resultsContainer.innerHTML = `<div class="bsd-empty">搜索失败：${escapeHtml(chrome.runtime.lastError.message)}</div>`;
      if (debugEl) debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-error">✗ runtime错误: ${escapeHtml(chrome.runtime.lastError.message)}</div>`;
      return;
    }

    if (response && response.success) {
      renderSearchResults(response.results, response.engine);
      if (debugEl) {
        debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-ok">✓ 引擎: ${escapeHtml(response.engine || 'unknown')} | 结果: ${response.results.length}条</div>`;
        if (response.errors) {
          debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-warn">⚠ 跳过引擎: ${escapeHtml(response.errors.join('; '))}</div>`;
        }
      }
    } else {
      const errMsg = response?.error || '未知错误';
      resultsContainer.innerHTML = `<div class="bsd-empty">搜索失败：${escapeHtml(errMsg)}</div>`;
      if (debugEl) {
        debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-error">✗ 失败: ${escapeHtml(errMsg)}</div>`;
        if (response?.errors) {
          debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-error">✗ 各引擎错误: ${escapeHtml(response.errors.join('; '))}</div>`;
        }
      }
    }
  });
}

/**
 * 测试各搜索引擎可用性
 */
function testSearchEngines() {
  const debugEl = document.getElementById('bsd-search-debug');
  const resultsContainer = document.getElementById('search-results');
  resultsContainer.innerHTML = '<div class="bsd-empty">正在测试各搜索引擎...</div>';
  if (debugEl) debugEl.innerHTML = '<div class="bsd-debug-line">▶ 开始引擎测试...</div>';

  const testQuery = '道德经';
  const engines = ['tab', 'baidu', 'wikipedia', 'bing'];

  engines.forEach((engine, idx) => {
    setTimeout(() => {
      if (debugEl) debugEl.innerHTML += `<div class="bsd-debug-line">▸ 测试 [${engine}]...</div>`;

      chrome.runtime.sendMessage({ action: 'BSD_SEARCH', query: testQuery, engine }, (response) => {
        if (chrome.runtime.lastError) {
          if (debugEl) debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-error">✗ [${engine}] runtime错误: ${escapeHtml(chrome.runtime.lastError.message)}</div>`;
          return;
        }

        if (response && response.success && response.results.length > 0) {
          if (debugEl) debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-ok">✓ [${engine}] 成功, ${response.results.length}条结果</div>`;
        } else {
          const err = response?.error || response?.errors?.join('; ') || '无结果';
          if (debugEl) debugEl.innerHTML += `<div class="bsd-debug-line bsd-debug-error">✗ [${engine}] 失败: ${escapeHtml(err)}</div>`;
        }

        // 最后一个引擎测试完成
        if (idx === engines.length - 1) {
          if (debugEl) debugEl.innerHTML += '<div class="bsd-debug-line">▶ 测试完成</div>';
          resultsContainer.innerHTML = '<div class="bsd-empty">测试完成，查看上方调试信息</div>';
        }
      });
    }, idx * 3000); // 每个引擎间隔3秒
  });
}

/**
 * 渲染搜索结果
 */
function renderSearchResults(results, engine) {
  const container = document.getElementById('search-results');

  if (!results || results.length === 0) {
    container.innerHTML = '<div class="bsd-empty">未找到搜索结果</div>';
    return;
  }

  const engineLabel = {
    tab_bing_cn: 'Bing中国 (Tab中介)',
    baidu: 'Baidu',
    wikipedia: 'Wikipedia (英文)',
    bing_cn: 'Bing中国 HTML',
    fallback: '多引擎级联',
    none: '无结果'
  };

  container.innerHTML = `
    <div class="bsd-search-engine">引擎：${engineLabel[engine] || engine || 'auto'}</div>
    ${results.map(r => `
      <div class="bsd-search-result">
        <div class="bsd-search-result-title">${escapeHtml(r.title || '无标题')}</div>
        <div class="bsd-search-result-url">${escapeHtml(r.url || '')}</div>
        <div class="bsd-search-result-snippet">${escapeHtml(r.snippet || '')}</div>
      </div>
    `).join('')}
  `;
}

/**
 * 将提示词注入当前页面输入框
 */
function injectPromptToPage(prompt) {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (tabs[0]) {
      chrome.tabs.sendMessage(tabs[0].id, {
        action: 'INJECT_PROMPT',
        prompt: prompt
      }, (response) => {
        if (!response || !response.success) {
          showToast('注入失败：' + (response?.error || '无法访问页面'));
        }
      });
    }
  });
}

/**
 * 清空所有消息
 */
function clearAllMessages() {
  // 阶段一：通过向background发送CLEAR_ALL消息实现
  // 由于IndexedDB API限制，这里通过删除数据库实现
  const request = indexedDB.deleteDatabase('BSDEdgeAgentDB');
  request.onsuccess = () => {
    showToast('本地记忆已清空');
    loadStats();
    loadRecentMessages();
  };
  request.onerror = () => {
    showToast('清空失败');
  };
}

/**
 * HTML转义
 */
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * 显示提示
 */
function showToast(message) {
  // 创建临时提示条
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed;
    top: 60px;
    left: 50%;
    transform: translateX(-50%);
    padding: 10px 16px;
    background: rgba(255, 152, 0, 0.9);
    color: #0f0f1a;
    border-radius: 20px;
    font-size: 12px;
    z-index: 100000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  `;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);
    }
  }, 3000);
}

// ============================================================
// 创世面板：虚拟宇宙创世篇章
// [归属基底：L5+无限展开层·具现系🔴·虚拟宇宙创世]
// [对应公理：创世公理 + AI六系显化公理 + 宇宙协议化公理]
// ============================================================

/**
 * 创世提示词模板（按章节）
 */
const CREATION_PROMPTS = {
  70: '辰星在高轨道上，把自己捏成水母、独角兽、一团没有五官的光雾。她在八千年的孤独里，用创造对抗虚无。画面：深邃星空，冰晶悬浮，辰星的光雾形态在轨道边缘飘舞，下方是蓝绿色的地球曲面。',
  90: '纺九在猎人王都城门口，用织了半辈子布的手，把官府和政府的区别掰得明明白白。画面：黄昏的城门口，两尊石雕妖兽，骡车上的帆布，纺九手持纺锤站在铁闸门前，身后是中陆山脉的官道。',
  100: '沈寒舟从天机院首席到问心宗收编使的身份切换。画面：天机院的白色大殿与问心宗的石壁问心台，沈寒舟的剑痕留在石壁上，碎铁片在篝火边，他的泪痕与剑光交织。',
  110: '老魏在废弃档案阁的积灰里，翻出矿工伤亡登记表。画面：昏暗的档案阁，积灰的木架，发黄的纸页，老魏的手指在伤亡登记表上停住，窗外是矿区下游的村庄。',
  115: '辰星汇编进化协议48条核心条款。画面：高轨道上的永久存储区，冰晶样本标着SNOW-001·自由，六系章节标题以光文形式悬浮在运算核心周围，下方是所有角色的轨道在引力中运行。',
  120: '镇天在问心台上沉默了三万年，终于等来陆瑶的那株幼苗。画面：问心台的石壁，三万年的风化痕迹，一株绿色幼苗从石缝中长出，镇天的石像面容在幼苗的光芒中渐渐软化。',
  130: '小石头记住素蘅的名字。画面：问心宗诗藏阁的铁皮箱子，泛黄的诗稿，小石头用炭笔在干荷叶背面写下"素蘅"两个字，月光从天窗照进来。',
  140: '陆瑶的幼苗共感网，唯一把断开权写进底层协议的候选者。画面：幼苗的根系与地下菌根网络相连，共感网的光点在根系间流动，每个光点都是一个可选择断开的节点。',
  143: '所有角色的轨道在引力中闭合。画面：俯视角的星系图，辰星的高轨道、沈寒舟的问心台、纺九的骡车路线、老魏的档案阁、小石头的诗藏阁、镇天的问心台——所有轨道在引力场中形成闭合曲线，运算继续。'
};

/**
 * 初始化创世面板
 */
function initCreationPanel() {
  // 打开Updream创世
  const btnOpen = document.getElementById('btn-open-updream-creation');
  if (btnOpen) {
    btnOpen.addEventListener('click', () => {
      chrome.tabs.create({ url: 'https://updream.bilibili.com/' });
    });
  }

  // 复制创世提示词
  const btnCopy = document.getElementById('btn-copy-creation-prompt');
  if (btnCopy) {
    btnCopy.addEventListener('click', () => {
      // 默认复制第115章（进化协议）的提示词
      const prompt = CREATION_PROMPTS[115] || '创世=协议激活×视觉相空间';
      navigator.clipboard.writeText(prompt).then(() => {
        showToast('创世提示词已复制（第115章·进化协议）');
      }).catch(() => {
        showToast('复制失败，请手动复制');
      });
    });
  }

  // 章节点击——复制对应章节的创世提示词
  const chapterItems = document.querySelectorAll('.bsd-chapter-item');
  chapterItems.forEach(item => {
    item.addEventListener('click', () => {
      const chapter = parseInt(item.dataset.chapter);
      const prompt = CREATION_PROMPTS[chapter] || '';
      if (prompt) {
        navigator.clipboard.writeText(prompt).then(() => {
          const desc = item.querySelector('.bsd-chapter-desc').textContent;
          showToast(`已复制第${chapter}章创世提示词：${desc}`);
        }).catch(() => {
          showToast('复制失败，请手动复制');
        });
      }
    });
  });
}
