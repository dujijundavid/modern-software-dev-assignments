# Document-Skills 插件深度指南：设计与创意

> A comprehensive guide to Claude Code's document-skills plugin for design and creative tasks
>
> **本指南专注于**：算法艺术、画布设计、前端界面设计、GIF 动画和主题系统

---

## Table of Contents

- [第一部分：Document Skills 概览](#第一部分document-skills-概览)
- [第二部分：设计创意 Skills 深度解析](#第二部分设计创意-skills-深度解析)
- [第三部分：项目实战工作流](#第三部分项目实战工作流)
- [第四部分：高级组合技巧](#第四部分高级组合技巧)
- [第五部分：最佳实践与陷阱](#第五部分最佳实践与陷阱)
- [附录：速查表与参考资源](#附录速查表与参考资源)

---

# 第一部分：Document Skills 概览

## 1.1 什么是 document-skills 插件

document-skills 是 Claude Code 的官方插件系统，扩展了 Claude 的能力，使其能够处理各种文档格式、创建设计作品、生成代码界面等。

### 插件架构

```
Claude Code (Core)
       │
       ├─→ Built-in Tools (Read, Write, Bash, etc.)
       │
       └─→ Plugin System
              │
              ├─→ document-skills Plugin
              │       │
              │       ├─→ docx (Word processing)
              │       ├─→ pptx (Presentations)
              │       ├─→ pdf (PDF manipulation)
              │       ├─→ xlsx (Spreadsheets)
              │       ├─→ algorithmic-art (p5.js art)
              │       ├─→ canvas-design (Visual design)
              │       ├─→ frontend-design (UI/UX)
              │       ├─→ slack-gif-creator (Animations)
              │       ├─→ theme-factory (Theming)
              │       └─→ ... (more skills)
```

### 安装和配置

document-skills 通常通过 Claude Code 的插件系统自动安装。检查安装状态：

```bash
# 查看已安装的 skills
/sc:help

# 直接调用特定 skill
/docx
/pptx
/algorithmic-art
```

### 与 Claude Code 的集成方式

```bash
# 方式 1: 直接调用 skill
Use /algorithmic-art to create flow field art

# 方式 2: 通过 Skill tool
Skill("algorithmic-art", "Create flow field with seed 12345")

# 方式 3: 自然语言触发
"Create a poster for my project" → 自动调用 canvas-design
```

---

## 1.2 所有可用 Skills 分类

### 办公文档类（快速概览）

| Skill | 能力 | 典型用途 |
|-------|------|----------|
| **docx** | Word 文档创建/编辑/批注 | 报告、合同、文档协作 |
| **pptx** | PowerPoint 演示文稿 | 幻灯片、演讲材料 |
| **pdf** | PDF 处理（提取、合并、表单） | 文档处理、报表生成 |
| **xlsx** | Excel 电子表格（公式、图表） | 数据分析、报表 |

> **注意**：本指南主要关注设计创意类 skills。办公文档类仅做概览。

---

### 设计与创意类（深度讲解）★

本指南核心内容，详见 [第二部分](#第二部分设计创意-skills-深度解析)：

| Skill | 技术栈 | 核心能力 |
|-------|--------|----------|
| **algorithmic-art** | p5.js + seeded random | 流场、粒子系统、生成艺术 |
| **canvas-design** | Python + design libs | 海报、静态视觉作品 |
| **frontend-design** | React + Tailwind + shadcn/ui | 生产级 UI 界面 |
| **slack-gif-creator** | GIF optimization | Slack 优化动画 |
| **theme-factory** | 主题引擎 | 10 预设主题 + 自定义 |

---

### 协作与工作流类

| Skill | 能力 | 典型用途 |
|-------|------|----------|
| **doc-coauthoring** | 结构化协作工作流 | 文档协作、迭代优化 |
| **internal-comms** | 企业通信模板 | 状态报告、更新公告 |
| **skill-creator** | 创建新 skills | 扩展 Claude 能力 |

---

### Web 与架构类

| Skill | 能力 | 典型用途 |
|-------|------|----------|
| **mcp-builder** | MCP 服务器开发指南 | 构建自定义 MCP |
| **webapp-testing** | Playwright 集成 | Web 应用测试 |
| **web-artifacts-builder** | React + Tailwind | 复杂 Web 组件 |

---

### 主题与品牌类

| Skill | 能力 | 典型用途 |
|-------|------|----------|
| **brand-guidelines** | Anthropic 官方品牌 | 官方样式、颜色 |
| **theme-factory** | 主题样式引擎 | 一致性视觉设计 |

---

## 1.3 设计创意 Skills 核心优势

### 为什么使用这些 Skills？

```
传统设计流程：
1. 学习设计工具 (Photoshop, Figma, etc.) → 数周
2. 学习设计原则 → 数月
3. 实践与迭代 → 持续
4. 代码实现 → 额外时间

使用 document-skills：
1. 描述需求 → 即时
2. AI 生成设计 → 秒级
3. 迭代优化 → 实时
4. 代码即设计 → 无缝
```

### Token 效率对比

| 方式 | Tokens | 时间 | 质量 |
|------|--------|------|------|
| 手写设计代码 | ~5000 | 30min | 取决于经验 |
| 使用 algorithmic-art | ~800 | 1min | 专业级 |
| 使用 canvas-design | ~600 | 1min | 品牌级 |

---

# 第二部分：设计创意 Skills 深度解析

## 2.1 Algorithmic Art - 算法艺术生成

### 技术栈

```
p5.js (Creative Coding Library)
    ↓
Seeded Randomness (确定性随机)
    ↓
Interactive Parameters (交互式参数)
```

### 核心能力

| 能力 | 描述 | 应用场景 |
|------|------|----------|
| **Flow Fields** (流场) | 基于噪声的向量场艺术 | 抽象背景、纹理生成 |
| **Particle Systems** (粒子系统) | 粒子运动模拟 | 动态效果、视觉特效 |
| **Generative Patterns** (生成模式) | 算法生成的图案 | 壁纸、装饰图案 |
| **Seeded Randomness** (种子随机) | 可重现的随机性 | 版本控制、批量生成 |

---

### 参数系统详解

#### 基础参数

```javascript
// 核心参数结构
{
  seed: 12345,           // 随机种子（决定整体风格）
  noiseScale: 0.01,      // 噪声缩放（影响平滑度）
  particleCount: 1000,   // 粒子数量（影响密度）
  speed: 2.0,            // 运动速度
  colorPalette: [...]    // 颜色配置
}
```

#### 高级参数

```javascript
{
  alpha: 0.5,            // 透明度（拖尾效果）
  fadeAmount: 0.95,      // 衰减量（影响轨迹长度）
  vectorScale: 100,      // 向量缩放（影响曲率）
  timeScale: 0.001       // 时间缩放（动画速度）
}
```

---

### 完整工作流示例

#### 示例 1: 创建基础流场艺术

**Prompt:**

```
Use /algorithmic-art to create flow field art with:
- Seed: 67890 (for reproducibility)
- 500 particles
- Blue-purple color palette
- Perlin noise scale: 0.005
- Output as PNG
```

**输出结果：**
- 高分辨率 PNG 图像
- 可重现的随机艺术
- 适合作为项目背景或装饰

---

#### 示例 2: 交互式参数探索

**Prompt:**

```
Use /algorithmic-art to explore flow field variations:
- Base seed: 11111
- Vary particleCount: [100, 500, 1000, 2000]
- Vary noiseScale: [0.001, 0.005, 0.01, 0.05]
- Generate 12 variations (3x4 grid)
- Compare and recommend best for dark theme
```

**工作流图：**

```
┌─────────────────────────────────────────────────────────────┐
│                    参数探索流程                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   定义参数空间                                              │
│   particleCount: [100, 500, 1000, 2000]                    │
│   noiseScale: [0.001, 0.005, 0.01, 0.05]                   │
│          │                                                  │
│          ▼                                                  │
│   批量生成 (12 变体)                                        │
│          │                                                  │
│          ▼                                                  │
│   质量筛选                                                  │
│   - 视觉平衡性                                              │
│   - 细节丰富度                                              │
│   - 主题适配性                                              │
│          │                                                  │
│          ▼                                                  │
│   推荐 Top 3                                                │
│   + 参数组合记录                                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 高级技巧

#### 性能优化

```javascript
// 渲染性能优化技巧
{
  // 1. 分辨率控制
  exportResolution: "2x",  // 预览时 1x，导出时 2x

  // 2. 粒子数量平衡
  particleCount: function(resolution) {
    return resolution === "1x" ? 500 : 2000;
  },

  // 3. 帧率控制
  targetFPS: 30,  // 动画预览 30fps，导出时 60fps

  // 4. 批量渲染
  batchRender: true  // 后台批量生成多个变体
}
```

#### 颜色理论应用

```javascript
// 配色方案系统
const colorPalettes = {
  monochromatic: (base) => [
    base,
    adjustBrightness(base, -20),
    adjustBrightness(base, +20),
    adjustBrightness(base, +40)
  ],

  complementary: (base) => [
    base,
    complementary(base),
    adjustSaturation(base, -50),
    adjustSaturation(complementary(base), -50)
  ],

  analogous: (base) => [
    base,
    rotateHue(base, -30),
    rotateHue(base, +30),
    adjustSaturation(base, -70)
  ]
};
```

---

## 2.2 Canvas Design - 画布视觉设计

### 核心能力

| 能力 | 描述 | 输出格式 |
|------|------|----------|
| **静态海报设计** | 文字排版 + 图形元素 | PNG, PDF |
| **品牌视觉** | Logo + 配色方案 | 多格式 |
| **信息图表** | 数据可视化 + 说明 | PDF |
| **原创设计** | 避免版权问题 | PNG, PDF |

---

### 设计哲学

```
核心原则：
1. 原创性 (Originality) - 避免复制现有艺术家风格
2. 功能性 (Functionality) - 设计服务于目的
3. 简洁性 (Simplicity) - 少即是多
4. 可访问性 (Accessibility) - 清晰可读
```

---

### 完整工作流示例

#### 示例: 项目架构海报

**输入数据** (来自 [CLAUDE.md](../CLAUDE.md)):

```yaml
Project: CS146S Modern Software Developer
Tech Stack:
  - FastAPI (Backend)
  - SQLAlchemy (Database)
  - Ollama (LLM)
  - pytest (Testing)

AI Team:
  - fastapi-expert
  - python-testing-expert
  - code-reviewer
  (etc.)
```

**Prompt:**

```
Use /canvas-design to create a project architecture poster:

Content:
- Title: "CS146S: Modern Software Developer"
- Subtitle: "AI Engineering Curriculum"
- Tech Stack: FastAPI, SQLAlchemy, Ollama, pytest
- AI Team: fastapi-expert, python-testing-expert, code-reviewer

Design Requirements:
- Professional academic style
- Color scheme: Blue (trust) + Orange (innovation)
- Clean hierarchy with clear sections
- Include project structure diagram
- Output: PDF (A3 size)
```

**输出结果：**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│          CS146S: MODERN SOFTWARE DEVELOPER                 │
│          AI Engineering Curriculum                         │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   FastAPI   │  │  SQLAlchemy │  │   Ollama    │         │
│  │   Backend   │  │   Database  │  │     LLM     │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                             │
│  AI Team:                                                   │
│  ├─ fastapi-expert (API endpoints)                         │
│  ├─ python-testing-expert (pytest + coverage)              │
│  └─ code-reviewer (quality assurance)                      │
│                                                             │
│  8-Week Path: Prompt → LLM Apps → MCP → Automation → ...   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 项目实战: 为 Week 2 创建视觉总结

**输入**: [learning_notes/week2/WEEK2_LEARNING_SUMMARY.md](../learning_notes/week2/WEEK2_LEARNING_SUMMARY.md) 内容

**Prompt:**

```
Use /canvas-design to create Week 2 learning summary poster:

Key Concepts to Visualize:
1. FastAPI Application Structure
   - main.py (app entry)
   - routers/ (API endpoints)
   - services/ (business logic)
   - db.py (database layer)

2. LLM Integration (Ollama)
   - extract.py (action item extraction)
   - JSON Schema validation
   - Error handling

3. Testing Strategy
   - 6 test files
   - 85% coverage
   - pytest + httpx

Design:
- Left side: Architecture diagram (boxes and arrows)
- Right side: Key learnings (bullet points)
- Bottom: Week 2 achievements (icons + stats)
- Color gradient: Purple (start) → Blue (end)
- Style: Technical documentation style
```

---

## 2.3 Frontend Design - 前端界面设计

### 技术栈

```
React (Component Framework)
    ↓
Tailwind CSS (Utility-First Styling)
    ↓
shadcn/ui (Component Library)
    ↓
Production-Grade UI
```

### 核心能力

| 能力 | 描述 | 特性 |
|------|------|------|
| **响应式布局** | 移动优先设计 | breakpoint-aware |
| **交互组件** | 按钮、表单、模态框 | 可访问性优化 |
| **数据可视化** | 图表、仪表板 | 实时更新 |
| **状态管理** | React hooks | 响应式数据流 |

---

### 避免通用的 AI 美学

```
问题示例：
❌ 通用渐变背景
❌ 过度使用阴影
❌ 标准圆角卡片
❌ 默认蓝色按钮

解决方案：
✅ 定制配色方案
✅ 独特的布局模式
✅ 有意的留白
✅ 品牌一致的交互
```

---

### 完整工作流示例

#### 示例: 学习进度仪表板

**数据模型:**

```typescript
interface LearningProgress {
  week: number;
  title: string;
  status: 'complete' | 'in-progress' | 'pending';
  progress: number; // 0-100
  topics: string[];
  timeSpent: number; // hours
  achievements: Achievement[];
}

interface Achievement {
  icon: string;
  title: string;
  description: string;
  unlocked: boolean;
}
```

**Prompt:**

```
Use /frontend-design to create learning progress dashboard:

Requirements:
1. Overview Cards
   - Total progress (circular progress bar)
   - Current week highlight
   - Time invested
   - Achievements unlocked

2. Week-by-Week Timeline
   - Horizontal scroll
   - Status indicators (complete/in-progress/pending)
   - Click to expand details

3. Learning Statistics
   - Bar chart: hours per week
   - Line chart: progress over time
   - Radar chart: skills coverage

4. Interactive Elements
   - Week detail modal
   - Achievement gallery
   - Export report button

Design:
- Dark mode by default
- Accent color: #6366f1 (Indigo)
- Card-based layout with subtle borders
- Smooth transitions (200ms)
- Responsive: mobile-first

Output:
- Complete React component
- Tailwind classes included
- shadcn/ui components used
- TypeScript types defined
```

---

### 响应式设计最佳实践

```typescript
// 断点策略
const breakpoints = {
  sm: '640px',   // Mobile landscape
  md: '768px',   // Tablet
  lg: '1024px',  // Laptop
  xl: '1280px',  // Desktop
  '2xl': '1536px' // Large desktop
};

// 布局模式
const layoutPatterns = {
  mobile: 'stack',      // Vertical stack
  tablet: 'split',      // 2-column grid
  desktop: 'grid',      // 3+ column grid
  wide: 'dashboard'     // Sidebar + main + aside
};
```

---

## 2.4 Slack GIF Creator - 动画 GIF 创建

### 核心能力

| 能力 | 描述 | 约束 |
|------|------|------|
| **动画优化** | 高质量 GIF 压缩 | <10MB (Slack limit) |
| **尺寸适配** | 多种输出尺寸 | 正方形/横版/竖版 |
| **帧率控制** | 平滑动画平衡 | 15-30fps |
| **颜色优化** | 256 色限制 | 智能调色板 |

---

### Slack 约束条件

```javascript
// Slack GIF 最佳实践
const constraints = {
  fileSize: {
    max: 10 * 1024 * 1024,  // 10MB
    recommended: 2 * 1024 * 1024  // 2MB (快速加载)
  },

  dimensions: {
    square: [512, 512],
    landscape: [800, 450],
    portrait: [450, 800]
  },

  animation: {
    minFrames: 6,      // 最低帧数
    maxFrames: 60,     // 最高帧数
    optimalFPS: 15,    // 最佳帧率
    loop: true         // 循环播放
  },

  colors: {
    maxColors: 256,    // GIF 限制
    recommended: 64    // 平衡质量和大小
  }
};
```

---

### 完整工作流示例

#### 示例: 周进度动画

**数据源:** 项目周进度数据

**Prompt:**

```
Use /slack-gif-creator to create weekly progress animation:

Scene Description:
Frame 1-6 (Buildup):
- Empty progress bar
- "Week 2 Progress" title appears
- Calendar flips to Week 2

Frame 7-18 (Progress):
- Progress bar fills smoothly
- Checkmarks pop in for each task:
  ✅ FastAPI setup
  ✅ LLM integration
  ✅ Testing framework
  ✅ Documentation

Frame 19-24 (Celebration):
- "85% Coverage" text appears
- Confetti animation
- Final frame: "Ready for review!"

Technical Specs:
- Size: 800x450 (landscape)
- Duration: ~2 seconds (24 frames @ 12fps)
- Colors: Team colors (blue + green)
- File size: <2MB
- Loop: Yes

Export:
- Optimized for Slack dark/light themes
- Test on both backgrounds
```

---

### 动画类型速查

| 类型 | 帧数 | 用途 | 复杂度 |
|------|------|------|--------|
| **Pulse** | 6-8 | 强调更新 | 低 |
| **Slide** | 8-12 | 过渡效果 | 中 |
| **Build** | 12-20 | 逐步展示 | 中 |
| **Celebration** | 18-30 | 成就解锁 | 高 |

---

## 2.5 Theme Factory - 主题样式工厂

### 核心能力

| 能力 | 描述 | 预设数量 |
|------|------|----------|
| **预设主题** | 即用型配色方案 | 10 |
| **动态生成** | 基于品牌色生成主题 | 无限 |
| **样式应用** | 一致性设计系统 | 全组件 |
| **导出格式** | CSS/Tailwind/JS Object | 多格式 |

---

### 10 种预设主题

```css
/* 1. Midnight (深色专业) */
--bg-primary: #0f172a;
--text-primary: #f8fafc;
--accent: #6366f1;

/* 2. Sunset (温暖渐变) */
--bg-primary: #fff7ed;
--text-primary: #1c1917;
--accent: #f97316;

/* 3. Forest (自然绿色) */
--bg-primary: #f0fdf4;
--text-primary: #14532d;
--accent: #22c55e;

/* 4. Ocean (海洋蓝色) */
--bg-primary: #f0f9ff;
--text-primary: #0c4a6e;
--accent: #0ea5e9;

/* 5. Berry (深红紫色) */
--bg-primary: #faf5ff;
--text-primary: #581c87;
--accent: #a855f7;

/* 6. Minimal (极简灰白) */
--bg-primary: #ffffff;
--text-primary: #18181b;
--accent: #71717a;

/* 7. High Contrast (高对比度) */
--bg-primary: #000000;
--text-primary: #ffffff;
--accent: #ffff00;

/* 8. Pastel (柔和色调) */
--bg-primary: #fef3c7;
--text-primary: #78350f;
--accent: #fbbf24;

/* 9. Cyber (赛博朋克) */
--bg-primary: #1a1a2e;
--text-primary: #00fff5;
--accent: #ff006e;

/* 10. Autumn (秋季色彩) */
--bg-primary: #fffbeb;
--text-primary: #451a03;
--accent: #ea580c;
```

---

### 主题组合模式

```
主题应用流程：

┌─────────────────────────────────────────────────────────────┐
│  1. 选择基础主题                                            │
│     └─→ 从 10 预设中选择 或 生成自定义                     │
├─────────────────────────────────────────────────────────────┤
│  2. 应用到组件                                              │
│     ├─→ algorithmic-art (配色方案)                         │
│     ├─→ canvas-design (品牌色彩)                           │
│     └─→ frontend-design (CSS 变量)                         │
├─────────────────────────────────────────────────────────────┤
│  3. 微调参数                                                │
│     ├─→ 亮度调整                                            │
│     ├─→ 饱和度调整                                          │
│     └─→ 对比度调整                                          │
├─────────────────────────────────────────────────────────────┤
│  4. 导出配置                                                │
│     ├─→ CSS Custom Properties                              │
│     ├─→ Tailwind Config                                    │
│     └─→ JavaScript Object                                  │
└─────────────────────────────────────────────────────────────┘
```

---

### 完整工作流示例

#### 示例: 项目品牌主题系统

**Prompt:**

```
Use /theme-factory to create project theme system:

Brand Colors (from project):
- Primary: #3b82f6 (Blue)
- Secondary: #10b981 (Green)
- Accent: #f59e0b (Orange)

Requirements:
1. Generate complete theme palette
   - Light mode variant
   - Dark mode variant
   - High contrast variant

2. Export formats
   - CSS Custom Properties
   - Tailwind config (tailwind.config.js)
   - JavaScript constants

3. Apply to all components
   - algorithmic-art color schemes
   - canvas-design brand colors
   - frontend-design theme

4. Documentation
   - Color usage guidelines
   - Accessibility compliance (WCAG AA)
   - Component examples
```

**输出示例:**

```javascript
// theme-system.js
export const projectTheme = {
  light: {
    primary: '#3b82f6',
    secondary: '#10b981',
    accent: '#f59e0b',
    background: '#ffffff',
    text: '#0f172a',
    border: '#e2e8f0'
  },

  dark: {
    primary: '#60a5fa',
    secondary: '#34d399',
    accent: '#fbbf24',
    background: '#0f172a',
    text: '#f8fafc',
    border: '#334155'
  },

  highContrast: {
    primary: '#0000ff',
    secondary: '#008000',
    accent: '#ff8c00',
    background: '#000000',
    text: '#ffffff',
    border: '#ffffff'
  }
};
```

---

# 第三部分：项目实战工作流

## 实战 1: 为项目创建视觉标识系统

### 目标

使用 canvas-design 为 CS146S 项目创建完整的品牌视觉系统

### 工作流程

```
阶段 1: 品牌分析
├─→ 分析项目定位（AI Engineering 教育）
├─→ 确定关键词（创新、专业、前沿）
└─→ 竞品参考（课程/教育平台）

阶段 2: 设计执行
├─→ 使用 canvas-design 创建 Logo
├─→ 设计配色方案
└─→ 创建视觉规范文档

阶段 3: 输出导出
├─→ 多格式 Logo (PNG, SVG, PDF)
├─→ 色彩代码 (HEX, RGB, HSL)
└─→ 使用指南

阶段 4: 应用验证
├─→ 应用到文档
├─→ 应用到演示文稿
└─→ 一致性检查
```

### 详细 Prompt

```
Use /canvas-design to create complete visual identity system:

Phase 1: Logo Design
- Logo type: Wordmark + Icon
- Text: "CS146S" (prominent) + "Modern Software Developer" (subtitle)
- Icon concept: Abstract representation of AI + Code collaboration
- Style: Modern tech, clean lines, professional
- Color: Blue primary (#3b82f6) with green accent (#10b981)

Phase 2: Color System
- Primary: Deep blue (trust, knowledge)
- Secondary: Green (growth, success)
- Accent: Orange (innovation, energy)
- Neutral: Gray scale for text/background
- Output: HEX, RGB, HSL values

Phase 3: Typography
- Headings: Inter/Montserrat (sans-serif, bold)
- Body: Source Sans Pro (readable, modern)
- Code: Fira Code (monospace, clear)

Phase 4: Visual Guidelines
- Logo usage rules (size, spacing, clear space)
- Color combinations (primary/secondary/accent pairs)
- Do's and don'ts
- Example applications

Output:
1. Logo variations (full color, monochrome, reversed)
2. Color palette reference
3. Typography scale
4. Usage guidelines PDF
```

### 验收标准

- [ ] Logo 在浅色和深色背景都清晰
- [ ] 色彩符合 WCAG AA 对比度标准
- [ ] 所有格式可缩放不失真
- [ ] 使用指南清晰易懂

---

## 实战 2: 生成项目文档艺术插图

### 目标

使用 algorithmic-art 为项目文档创建系列艺术插图

### 工作流程

```
主题确定
├─→ Week 1: Prompt Engineering (流动/探索)
├─→ Week 2: LLM Integration (连接/融合)
├─→ Week 3: MCP Server (扩展/工具)
├─→ Week 4: Automation (流程/效率)
└─→ Week 5+: Advanced (复杂/协作)

风格统一
├─→ 共同色彩方案
├─→ 一致粒子密度
└─→ 平衡复杂度
```

### 详细 Prompt

```
Use /algorithmic-art to create documentation illustration series:

Theme: "AI Engineering Journey" - 8 visual metaphors

Illustration 1: Week 1 - "Foundations"
- Concept: Flow field representing knowledge exploration
- Visual: Particles following invisible paths
- Colors: Blue to purple gradient
- Seed: 10001
- Style: Clean, minimal, inviting

Illustration 2: Week 2 - "Integration"
- Concept: Two systems merging
- Visual: Particle convergence pattern
- Colors: Blue + Green blend
- Seed: 10002
- Style: Harmonious, balanced

Illustration 3: Week 3 - "Extension"
- Concept: Expanding capabilities
- Visual: Radial burst pattern
- Colors: Green + Orange accent
- Seed: 10003
- Style: Dynamic, outward

Illustration 4: Week 4 - "Automation"
- Concept: Efficient processes
- Visual: Organized flow lines
- Colors: All three colors in harmony
- Seed: 10004
- Style: Structured, rhythmic

Illustration 5-8: Advanced weeks
- Concept: Complexity and collaboration
- Visual: Multi-layer patterns
- Colors: Full palette
- Seeds: 10005-10008
- Style: Rich, sophisticated

Common Parameters:
- Resolution: 1920x1080 (16:9)
- Particle count: 1500 (consistent density)
- Alpha: 0.6 (soft overlap)
- Fade: 0.96 (medium trail length)

Output:
- 8 PNG files (week1.png through week8.png)
- PDF reference document with all 8
- Parameter log for reproducibility
```

### 参数对比表

| 参数 | Week 1-2 | Week 3-4 | Week 5-8 |
|------|----------|----------|----------|
| particleCount | 1000 | 1500 | 2000 |
| alpha | 0.5 | 0.6 | 0.7 |
| fadeAmount | 0.95 | 0.96 | 0.97 |
| colorVariety | 2 | 3 | 4 |

---

## 实战 3: 创建项目进度可视化页面

### 目标

使用 frontend-design 创建交互式学习进度追踪界面

### 数据结构

```typescript
// 数据模型
interface WeeklyData {
  week: number;
  title: string;
  status: 'locked' | 'current' | 'complete';
  progress: number;
  topics: {
    category: string;
    items: string[];
  }[];
  timeSpent: {
    learning: number;
    practice: number;
    review: number;
  };
  achievements: Achievement[];
}

interface Achievement {
  id: string;
  icon: string;
  title: string;
  unlockedAt?: Date;
}
```

### 详细 Prompt

```
Use /frontend-design to create interactive learning progress dashboard:

Page Structure:
┌─────────────────────────────────────────────────────────────┐
│ Header: CS146S Progress Tracker                             │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│  Week Navigation │  Week Detail View                        │
│  (Left Sidebar)  │  (Main Content)                         │
│                  │                                          │
│  ┌────────────┐ │  ┌─────────────────────────────────────┐│
│  │ Week 1     │ │  │ Week 2: LLM-Powered Applications    ││
│  │ ✓ Complete │ │  │                                     ││
│  ├────────────┤ │  │ Progress: ████████░░ 80%           ││
│  │ Week 2     │ │  │                                     ││
│  │ → Current  │ │  │ Topics:                             ││
│  ├────────────┤ │  │ ├─ FastAPI Fundamentals             ││
│  │ Week 3     │ │  │ ├─ LLM Integration with Ollama      ││
│  │   Locked   │ │  │ └─ Testing with pytest              ││
│  └────────────┘ │  │                                     ││
│                  │  │ Time Invested:                      ││
│                  │  │ ├─ Learning: 8h                     ││
│                  │  │ ├─ Practice: 12h                    ││
│  Achievements   │  │ └─ Review: 2h                       ││
│  (Bottom Panel) │  │                                     ││
│                  │  │ Achievements:                      ││
│  ┌─┐ ┌─┐ ┌─┐   │  │ 🏆 First FastAPI Endpoint           ││
│  │ │ │ │ │ │   │  │ 🧪 Test Coverage Champion           ││
│  └─┘ └─┘ └─┘   │  │ 📝 Documentation Pro                ││
│                  │  │                                     ││
│                  │  │ [Mark Complete] [Export Report]    ││
│                  │  └─────────────────────────────────────┘│
└──────────────────┴──────────────────────────────────────────┘

Features:
1. Week Navigation (Sidebar)
   - Vertical scroll
   - Status icons (✓ complete, → current, 🔒 locked)
   - Click to navigate
   - Progress indicator per week

2. Week Detail View (Main)
   - Overview header with title
   - Progress bar (animated)
   - Topic list with checkboxes
   - Time breakdown (donut chart)
   - Achievement badges
   - Action buttons

3. Achievements Panel (Bottom)
   - Horizontal scroll
   - Locked/unlocked states
   - Tooltip on hover
   - Click for details

4. Interactive Elements
   - Week completion toggle
   - Topic checkbox (updates progress)
   - Time log input
   - Export to PDF
   - Filter by status

Design Requirements:
- Dark mode default
- Primary: #3b82f6 (blue)
- Success: #10b981 (green)
- Warning: #f59e0b (orange)
- Card background: #1e293b
- Text: #f8fafc (primary), #94a3b8 (secondary)

Technical:
- React with TypeScript
- Tailwind CSS for styling
- shadcn/ui components
- Responsive (mobile-friendly)
- State management with React hooks
- Local storage for persistence
```

### 组件结构

```typescript
// 文件结构
src/
├── components/
│   ├── WeekSidebar.tsx          // 周导航
│   ├── WeekDetailView.tsx       // 周详情
│   ├── ProgressBar.tsx          // 进度条
│   ├── TopicList.tsx            // 主题列表
│   ├── TimeChart.tsx            // 时间图表
│   └── AchievementPanel.tsx     // 成就面板
├── hooks/
│   ├── useProgress.ts           // 进度状态
│   └── useLocalStorage.ts       // 本地存储
├── types/
│   └── index.ts                 // TypeScript 类型
└── data/
    └── weekData.ts              // 静态数据
```

---

## 实战 4: 生成周报动画 GIF

### 目标

使用 slack-gif-creator 为团队创建周进度动画

### 数据转换

```typescript
// 输入数据
interface WeekReport {
  week: number;
  title: string;
  completed: number;
  total: number;
  highlights: string[];
  nextUp: string;
}

// 动画场景规划
interface AnimationScene {
  frameStart: number;
  frameEnd: number;
  action: string;
  content: string;
}
```

### 详细 Prompt

```
Use /slack-gif-creator to create weekly report animation:

Input Data:
- Week: 2
- Title: "LLM-Powered Applications"
- Completed: 4/5 tasks (80%)
- Highlights:
  * Built first FastAPI endpoint
  * Integrated Ollama for local LLM
  * Wrote 6 test files with 85% coverage
  * Created comprehensive documentation
- Next: "MCP Server Development"

Animation Script (24 frames @ 12fps):

Frames 1-4: Title Reveal
├─→ Frame 1: "Week 2" fades in
├─→ Frame 2: Subtitle appears
├─→ Frame 3: Icon (FastAPI logo) slides in
└─→ Frame 4: Background gradient stabilizes

Frames 5-12: Progress Buildup
├─→ Frame 5-8: Empty progress bar appears
├─→ Frame 9-12: Bar fills smoothly (0% → 80%)

Frames 13-18: Highlights
├─→ Frame 13: "✓ FastAPI" checkmark pops
├─→ Frame 15: "✓ Ollama" checkmark pops
├─→ Frame 17: "✓ Testing" checkmark pops
└─→ Frame 18: "✓ Docs" checkmark pops

Frames 19-22: Stats
├─→ Frame 19: "85% Coverage" counter animates
├─→ Frame 21: "6 Tests" appears
└─→ Frame 22: Trophy icon unlocks

Frames 23-24: Next Week
├─→ Frame 23: "Up Next: MCP Server" slides up
└─→ Frame 24: Final pose (pause for loop)

Visual Design:
- Size: 800x450
- Colors:
  * Background: #0f172a (dark blue)
  * Progress: #10b981 (green)
  * Text: #f8fafc (white)
  * Accent: #3b82f6 (blue)
- Font: Inter/Roboto
- Style: Clean, modern, tech-focused

Technical Specs:
- Duration: 2 seconds
- FPS: 12
- Loop: Yes
- File size target: <1.5MB
- Dithering: Adaptive
- Colors: Optimized palette

Optimization:
- Use color reduction (64 colors max)
- Crop to content bounds
- Remove redundant frames
- Test on both Slack dark/light themes

Output:
1. Optimized GIF file
2. Preview on both backgrounds
3. File size report
4. Frame-by-frame breakdown
```

### 动画模板

```
┌─────────────────────────────────────────────────────────────┐
│                   动画帧模板系统                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   通用模板 A: 线性进度                                      │
│   ├─ 适用于: 任务完成、进度更新                            │
│   └─ 结构: 标题 → 进度条 → 统计 → 循环                     │
│                                                             │
│   通用模板 B: 列表展开                                      │
│   ├─ 适用于: 功能列表、成就展示                            │
│   └─ 结构: 标题 → 逐项显示 → 全览 → 循环                   │
│                                                             │
│   通用模板 C: 对比展示                                      │
│   ├─ 适用于: Before/After、对比分析                        │
│   └─ 结构: 状态A → 转换 → 状态B → 循环                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

# 第四部分：高级组合技巧

## 4.1 多 Skill 协作模式

### 模式 1: Theme + Algorithmic Art

**场景**: 生成主题一致的系列艺术作品

```
Workflow:

/theme-factory
├─→ Generate project color palette
├─→ Export as JavaScript object
└─→ Output: theme.js

/algorithmic-art
├─→ Import colors from theme.js
├─→ Apply to multiple seed values
└─→ Output: Themed art series

Result: Consistent visual language across all generative art
```

### 模式 2: Frontend Design + Canvas Design

**场景**: 创建完整的网站设计系统

```
Workflow:

/canvas-design
├─→ Create brand assets (logo, icons, patterns)
├─→ Export as SVG/PNG
└─→ Output: assets/

/frontend-design
├─→ Import brand assets
├─→ Create component library
├─→ Apply brand colors
└─→ Output: Complete UI system

Result: Cohesive design system with custom assets
```

### 模式 3: Algorithmic Art + Slack GIF

**场景**: 从静态艺术到动态展示

```
Workflow:

/algorithmic-art
├─→ Create base artwork
├─→ Export frame sequence
└─→ Output: frame-001.png through frame-060.png

/slack-gif-creator
├─→ Import frame sequence
├─→ Optimize for Slack
├─→ Add overlays/text
└─→ Output: Optimized GIF

Result: Animated showcase of generative art process
```

---

## 4.2 自动化工作流设计

### 批量生成策略

```python
# 批量生成工作流伪代码
def batch_generate_art(theme, variations):
    results = []

    # 1. 生成基础主题
    base_colors = theme_factory.generate(theme)

    # 2. 为每个变体创建艺术
    for i, params in enumerate(variations):
        art = algorithmic_art.create(
            seed=base_colors.seed + i,
            colors=base_colors.palette,
            **params
        )
        results.append(art)

    # 3. 质量筛选
    filtered = quality_filter(results)

    # 4. 批量导出
    export_batch(filtered, format='png')

    return filtered
```

### 质量控制流程

```
┌─────────────────────────────────────────────────────────────┐
│                    质量控制流水线                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   生成                                                      │
│   ├─→ 批量创建候选作品                                      │
│   └─→ 保存原始数据                                          │
│          │                                                  │
│          ▼                                                  │
│   自动筛选                                                  │
│   ├─→ 文件大小检查 (<10MB)                                  │
│   ├─→ 分辨率验证 (>=1920x1080)                              │
│   ├─→ 颜色一致性 (符合主题)                                  │
│   └─→ 复杂度评分 (避免过度简单/复杂)                         │
│          │                                                  │
│          ▼                                                  │
│   人工审查                                                  │
│   ├─→ 视觉吸引力                                            │
│   ├─→ 品牌一致性                                            │
│   └─→ 用途适配性                                            │
│          │                                                  │
│          ▼                                                  │
│   最终输出                                                  │
│   ├─→ 选中作品                                              │
│   ├─→ 参数记录                                              │
│   └─→ 使用建议                                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4.3 性能与优化

### 渲染性能优化

| 技巧 | 效果 | 适用场景 |
|------|------|----------|
| **分辨率分级** | 预览 1x，导出 2x | 交互式设计 |
| **帧率控制** | 降低预览帧率 | 动画预览 |
| **颜色限制** | 减少调色板大小 | GIF 优化 |
| **增量渲染** | 只渲染变化部分 | 复杂场景 |

### 内存管理

```javascript
// 内存优化策略
const memoryStrategy = {
  // 1. 分块处理
  chunkSize: 10,  // 每次处理 10 个项目

  // 2. 及时释放
  cleanupAfter: 1000,  // 1秒后清理

  // 3. 流式导出
  streaming: true  // 边生成边导出
};
```

### 输出质量平衡

```
质量 vs 大小权衡：

高保真 (适用于打印/展示)
├─→ 分辨率: 4K (3840x2160)
├─→ 颜色: 完整色彩空间
├─→ 文件大小: 5-10MB
└─→ 处理时间: 长

标准 (适用于 Web)
├─→ 分辨率: 2K (1920x1080)
├─→ 颜色: sRGB
├─→ 文件大小: 1-3MB
└─→ 处理时间: 中

优化 (适用于快速预览)
├─→ 分辨率: 1080p
├─→ 颜色: 优化调色板
├─→ 文件大小: <500KB
└─→ 处理时间: 短
```

---

# 第五部分：最佳实践与陷阱

## 5.1 设计原则

### 版权与原创性

```
❌ 避免：
- 复制知名艺术家风格
- 使用受版权保护的图像
- 模仿现有品牌设计

✅ 推荐：
- 使用算法生成独特图案
- 基于项目需求原创设计
- 记录生成参数供复现
```

### 可访问性

```css
/* WCAG AA 标准 */
:root {
  /* 正常文本 */
  --contrast-ratio: 4.5:1;  /* 最小值 */

  /* 大文本 (18pt+) */
  --contrast-ratio-large: 3:1;  /* 最小值 */

  /* 交互元素 */
  --focus-indicator: 2px solid currentColor;
  --active-indicator: invert;
}
```

### 响应式设计

```
断点策略：
Mobile (320px+)    → 堆叠布局，大触摸目标
Tablet (768px+)    → 两列布局，适中目标
Desktop (1024px+)  → 多列布局，完整导航
Wide (1440px+)     → 最大宽度限制，居中内容
```

---

## 5.2 技术债务避免

### 代码复用策略

```typescript
// ✅ 好: 可复用组件
const DesignCard = ({ title, image, description }) => (
  <Card className="design-card">
    <CardHeader>
      <img src={image} alt={title} />
      <Title>{title}</Title>
    </CardHeader>
    <CardBody>
      <Text>{description}</Text>
    </CardBody>
  </Card>
);

// ❌ 不好: 重复代码
const Card1 = () => (
  <div className="card">
    <div className="header">
      <img src="..." />
      <h3>Title 1</h3>
    </div>
    <div className="body">
      <p>Description 1</p>
    </div>
  </div>
);
```

### 模块化设计

```
设计系统层次：

原子 (Atoms)
├─→ 按钮、输入框、图标
└─→ 最小可复用单元

分子 (Molecules)
├─→ 搜索框、导航项
└─→ 原子组合

生物 (Organisms)
├─→ 导航栏、卡片网格
└─→ 分子组合

模板 (Templates)
├─→ 页面布局
└─→ 生物组合

页面 (Pages)
├─→ 完整页面
└─→ 模板实例化
```

---

## 5.3 故障排查

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| **GIF 文件过大** | 帧数过多/颜色过多 | 减少帧数/优化调色板 |
| **颜色不一致** | 颜色空间不匹配 | 统一使用 sRGB |
| **渲染缓慢** | 分辨率过高 | 降低预览分辨率 |
| **动画卡顿** | 帧率不匹配 | 统一帧率设置 |
| **导出失败** | 磁盘空间不足 | 清理临时文件 |

### 调试技巧

```javascript
// 调试日志
const debugLog = {
  // 1. 参数记录
  params: { seed, particleCount, colors },

  // 2. 性能指标
  performance: {
    renderTime: Date.now() - start,
    memory: process.memoryUsage(),
    fps: frameCount / duration
  },

  // 3. 输出验证
  output: {
    dimensions: [width, height],
    fileSize: stats.size,
    format: mimeType
  }
};

console.table(debugLog);
```

---

# 附录：速查表与参考资源

## A. 参数速查表

### Algorithmic Art

```javascript
// 流场艺术参数
{
  seed: 12345,              // 随机种子
  particleCount: 1000,      // 粒子数: 100-5000
  noiseScale: 0.01,         // 噪声: 0.001-0.1
  alpha: 0.6,               // 透明度: 0.1-1.0
  fadeAmount: 0.96,         // 衰减: 0.9-0.99
  speed: 2.0,               // 速度: 0.5-10
  colors: [...]             // 颜色数组
}
```

### Canvas Design

```javascript
// 输出规格
{
  format: 'png',            // png, pdf, svg
  width: 1920,              // 像素宽度
  height: 1080,             // 像素高度
  dpi: 300,                 // 打印分辨率
  backgroundColor: '#ffffff',
  fontFamily: 'Inter'
}
```

### Slack GIF Creator

```javascript
// GIF 优化参数
{
  width: 800,               // 最大宽度
  height: 450,              // 最大高度
  fps: 12,                  // 帧率: 10-30
  colors: 64,               // 颜色数: 16-256
  dither: true,             // 抖动
  loop: 0,                  // 循环 (0=无限)
  quality: 80               // 质量: 1-100
}
```

---

## B. 颜色理论快速参考

### 色彩关系

```
色轮 (Color Wheel)

        Red (0°)
          │
          │
Purple (300°) ───┼─── Orange (30°)
          │
          │
       Blue (240°)
          │
          │
Green (120°) ─────┼──── Yellow (60°)
          │
          │
```

### 配色方案

| 方案 | 描述 | 示例 |
|------|------|------|
| **单色** | 同色相，不同明度 | 深蓝 → 蓝 → 浅蓝 |
| **类比** | 相邻色相 | 蓝 → 蓝绿 → 绿 |
| **互补** | 对立色相 | 蓝 → 橙 |
| **三色** | 等距三色 | 红 → 黄 → 蓝 |
| **分裂互补** | 互补 + 邻近 | 蓝 → 橙红 → 橙黄 |

---

## C. 性能基准数据

### 渲染时间参考

| 分辨率 | 粒子数 | 渲染时间 | 内存使用 |
|--------|--------|----------|----------|
| 1080p | 500 | ~2s | ~50MB |
| 1080p | 1000 | ~4s | ~80MB |
| 1080p | 2000 | ~8s | ~150MB |
| 4K | 500 | ~8s | ~100MB |
| 4K | 1000 | ~15s | ~200MB |
| 4K | 2000 | ~30s | ~400MB |

### GIF 优化参考

| 帧数 | 颜色 | 文件大小 | 质量 |
|------|------|----------|------|
| 12 | 32 | ~200KB | 低 |
| 24 | 64 | ~500KB | 中 |
| 48 | 128 | ~1.5MB | 高 |
| 60 | 256 | ~3MB | 极高 |

---

## D. 社区资源链接

### 官方资源

- [Claude Code 文档](https://docs.anthropic.com/claude-code)
- [Anthropic Brand Guidelines](https://anthropic.com/brand)
- [MCP Protocol](https://modelcontextprotocol.io)

### 设计资源

- [p5.js 官网](https://p5js.org)
- [Color Hunt](https://colorhunt.co) - 配色灵感
- [Coolors](https://coolors.co) - 配色生成器
- [Tailwind CSS](https://tailwindcss.com)

### 学习资源

- [Generative Design](https://generative-design.ch) - 生成艺术
- [The Nature of Code](https://natureofcode.com) - 自然模拟
- [Creative Coding](https://creative-coding.de) - 创意编程

---

## 结语

本指南专注于 document-skills 插件的设计创意能力。通过掌握这些工具，你可以：

1. **快速创建** 专业级视觉内容
2. **保持一致** 的品牌视觉语言
3. **自动化** 设计工作流程
4. **避免版权** 问题（原创生成）

### 下一步

- [ ] 选择一个实战项目开始实践
- [ ] 创建你的第一个主题系统
- [ ] 为项目生成系列艺术作品
- [ ] 构建完整的 UI 设计系统

---

**版本**: 1.0
**更新日期**: 2025-12-28
**项目**: CS146S Modern Software Developer
