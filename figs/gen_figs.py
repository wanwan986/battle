# -*- coding: utf-8 -*-
"""生成论文插图。所有文字严格取自论文正文，不引入正文没有的内容。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

FP = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
fm.fontManager.addfont(FP)
FONT = fm.FontProperties(fname=FP).get_name()
plt.rcParams['font.family'] = FONT
plt.rcParams['axes.unicode_minus'] = False

INK   = '#1a1a1a'
LINE  = '#555555'
FILL1 = '#eef2f7'
FILL2 = '#e6ede6'
FILL3 = '#f5eee6'
FILL4 = '#ffffff'
HL    = '#fdf6e3'
ACC   = '#2c4a6e'


def box(ax, x, y, w, h, text='', fc=FILL4, ec=LINE, fs=10, lw=1.0,
        weight='normal', tc=INK, ls='-'):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle="round,pad=0,rounding_size=0.6",
                 facecolor=fc, edgecolor=ec, linewidth=lw, linestyle=ls, zorder=2))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha='center', va='center',
                fontsize=fs, color=tc, weight=weight, zorder=3, linespacing=1.6)


def arrow(ax, p1, p2, lw=1.2, color=LINE, ms=9):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle='-|>', mutation_scale=ms,
                 linewidth=lw, color=color, zorder=4, shrinkA=0, shrinkB=0))


def canvas(w, h, xlim=(0, 100), ylim=(0, 100), equal=False):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if equal:
        ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, name):
    fig.savefig(f'/home/user/battle/figs/{name}', dpi=200,
                bbox_inches='tight', facecolor='white', pad_inches=0.14)
    plt.close(fig)
    print('saved', name)


# ═════════ 图1 研究框架与逻辑主线 ═════════
fig, ax = canvas(9.6, 6.6)

box(ax, 16, 88, 68, 9.5,
    '概念辨析：能力同源、运用异构\n'
    '（能力在战场与非战场同根同源；运用目的、手段限度、法律依据各异）',
    fc=FILL1, ec=ACC, fs=10.5, lw=1.4, weight='bold')
arrow(ax, (50, 88), (50, 83))

ax.text(50, 80.5, '四条战法制约条件', ha='center', va='center',
        fontsize=10.5, weight='bold', color=ACC)
for i, t in enumerate(['法治先行\n依据是法律授权\n而非交战规则',
                       '非致命优先\n处置手段\n梯次受限',
                       '军地协同\n多元主体\n而非单一力量',
                       '舆情敏感\n容错空间\n趋零']):
    box(ax, 6 + i * 23.5, 65, 21, 12, t, fc=FILL1, fs=9)
for i in range(4):
    arrow(ax, (16.5 + i * 23.5, 65), (16.5 + i * 23.5, 60.5))
ax.plot([16.5, 87], [60.5, 60.5], color=LINE, lw=1.0, zorder=1)
arrow(ax, (26, 60.5), (26, 56)); arrow(ax, (74, 60.5), (74, 56))

box(ax, 4, 30, 44, 26, fc=FILL3, ec=ACC, lw=1.3)
ax.text(26, 52.6, '对抗性场景　大型活动“低慢小”防控',
        ha='center', va='center', fontsize=10, weight='bold', color=ACC)
for i, t in enumerate(['侦控一体：三源复合侦测＋圈层分区管控',
                       '梯次处置：法律授权前置的分级响应',
                       '闭环追责：处置—取证—追责同步']):
    box(ax, 7, 44.4 - i * 6.3, 38, 5.3, t, fs=8.8)

box(ax, 52, 30, 44, 26, fc=FILL2, ec=ACC, lw=1.3)
ax.text(74, 52.6, '非对抗性场景　抢险救灾应急运用',
        ha='center', va='center', fontsize=10, weight='bold', color=ACC)
for i, t in enumerate(['先侦后救：短时形成“灾情一张图”',
                       '断点续传：空中基站重建应急通信',
                       '分级投送与有人—无人—民间协同编组']):
    box(ax, 55, 44.4 - i * 6.3, 38, 5.3, t, fs=8.8)

arrow(ax, (26, 30), (26, 25.5)); arrow(ax, (74, 30), (74, 25.5))
ax.plot([26, 74], [25.5, 25.5], color=LINE, lw=1.0, zorder=1)
arrow(ax, (50, 25.5), (50, 21))

ax.text(50, 18.5, '双场景比较：四条共性规律', ha='center', va='center',
        fontsize=10.5, weight='bold', color=ACC)
for i, (a, b) in enumerate([('人机功能分配', '谁来干'), ('数据同源复用', '靠什么干'),
                            ('制度倍增效应', '凭什么能干'), ('能力平战迁移', '练了有什么用')]):
    box(ax, 6 + i * 23.5, 3.5, 21, 11, f'{a}\n\n（{b}）', fc=FILL1, fs=9)

save(fig, 'fig1_framework.png')


# ═════════ 图2 “图—谱—链”三源复合侦测融合 ═════════
fig, ax = canvas(10.2, 4.8)

srcs = [('“图”　雷达探测', '微多普勒调制特征，\n区分真目标与飞鸟、气球', '解决“有没有目标”'),
        ('“谱”　频谱侦测', '到达时间差（TDOA）网格化组网，\n对无人机与操控者双重定位', '解决“在哪、谁在操控”'),
        ('“链”　运行识别', '广播式＋网络式报送身份位置，\n形成“电子身份证”', '解决“是友是异”')]
for i, (h, d, k) in enumerate(srcs):
    y = 66 - i * 31
    box(ax, 1, y, 33, 27, fc=FILL1, ec=LINE)
    ax.text(17.5, y + 21, h, ha='center', va='center', fontsize=10, weight='bold', color=ACC)
    ax.text(17.5, y + 12.5, d, ha='center', va='center', fontsize=8.3, color=INK, linespacing=1.6)
    ax.text(17.5, y + 4.5, k, ha='center', va='center', fontsize=8.6, color=ACC, style='italic')
    arrow(ax, (34, y + 13.5), (40, y + 13.5))

box(ax, 40, 4, 10, 89, '特\n征\n级\n与\n决\n策\n级\n融\n合',
    fc=ACC, ec=ACC, fs=9.6, tc='white')
arrow(ax, (50, 48.5), (56, 48.5))

box(ax, 56, 55, 43, 30, fc=FILL4, ec=ACC, lw=1.5)
ax.text(77.5, 76, '统一低空态势图', ha='center', va='center',
        fontsize=11.5, weight='bold', color=ACC)
ax.text(77.5, 64, '三源配准后，方能把一个回波点升级为\n含身份、轨迹、操控者位置的完整目标信息',
        ha='center', va='center', fontsize=8.4, color=INK, linespacing=1.7)

box(ax, 56, 12, 43, 32, fc=HL, ec=ACC, lw=1.3)
ax.text(77.5, 37, '战法级变化', ha='center', va='center',
        fontsize=10.5, weight='bold', color=ACC)
ax.text(77.5, 24, '由“筛查一切未知目标”\n转为“锁定未登记目标”，\n探测识别从大海捞针变为按图索骥',
        ha='center', va='center', fontsize=8.8, color=INK, linespacing=1.8)

save(fig, 'fig2_three_sources.png')


# ═════════ 图3 “圈层—网格—白名单”分区管控 ═════════
fig, ax = canvas(9.6, 5.2, xlim=(-54, 96), ylim=(-56, 50), equal=True)

outer = Circle((0, 0), 40, facecolor='#f4f7fa', edgecolor=ACC, lw=1.3, zorder=2)
ax.add_patch(outer)
for g in range(-3, 4):
    l1, = ax.plot([g * 13, g * 13], [-40, 40], color='#9bb0c4', lw=0.5, zorder=3, alpha=.8)
    l2, = ax.plot([-40, 40], [g * 13, g * 13], color='#9bb0c4', lw=0.5, zorder=3, alpha=.8)
    l1.set_clip_path(outer); l2.set_clip_path(outer)
ax.add_patch(Circle((0, 0), 26, facecolor='#e0eaf4', edgecolor=ACC, lw=1.2, zorder=4))
ax.add_patch(Circle((0, 0), 12, facecolor='#b9cfe4', edgecolor=ACC, lw=1.3, zorder=5))

ax.text(0, 0, '核心\n禁飞区', ha='center', va='center', fontsize=9,
        weight='bold', color=ACC, zorder=6, linespacing=1.5)
ax.text(0, 19, '缓冲限飞区', ha='center', va='center', fontsize=9, color=ACC, zorder=6)
ax.text(0, 33, '外围警戒区', ha='center', va='center', fontsize=9, color=ACC, zorder=6)

# 径向箭头：由外向内，与文字表述方向一致
arrow(ax, (31.5, 31.5), (9.5, 9.5), lw=1.7, color='#a63a2f', ms=13)
ax.text(35, 37, '由外向内', ha='left', va='center', fontsize=9.2,
        weight='bold', color='#a63a2f')
ax.text(46, 12, '探测密度加密\n响应时限压缩\n处置权限上收',
        ha='left', va='center', fontsize=9.2, color=ACC, linespacing=2.0)

ax.annotate('网格化责任区\n明确首问责任与响应时限',
            xy=(-27, 26), xytext=(-53, 43), fontsize=8.8, color=INK,
            linespacing=1.6, ha='left', va='center',
            arrowprops=dict(arrowstyle='-', color=LINE, lw=0.9))

box(ax, -53, -55, 148, 11,
    '白名单动态授权：安保、勤务、转播用机以电子标识纳入统一态势图，实现“放得开、管得住”',
    fc=HL, ec=ACC, fs=9.4, lw=1.2)

save(fig, 'fig3_zoning.png')


# ═════════ 图4 法律授权前置的分级响应模型 ═════════
fig, ax = canvas(11.2, 6.0)

ax.text(31, 96, '处置烈度由低到高逐级递进', ha='center', fontsize=10.5,
        weight='bold', color=ACC)

levels = [('第一级　持续监视与告警', '喊话、灯光警示，引导目标自行离开'),
          ('第二级　软性干预', '对图传与遥控链路实施定向干预'),
          ('第三级　受控迫降', '借导航信号手段引导至预设安全区降落'),
          ('第四级　末端物理拦截', '抛网、动能撞击及定向能手段')]
shades = ['#eef4fa', '#dce8f3', '#c6d9ea', '#aec8de']
for i, ((h, d), sh) in enumerate(zip(levels, shades)):
    y = 70 - i * 16
    box(ax, 5 + i * 2.6, y, 52 - i * 2.6, 14, fc=sh, ec=ACC, lw=1.1)
    ax.text(8 + i * 2.6, y + 9, h, ha='left', va='center',
            fontsize=9.8, weight='bold', color=ACC)
    ax.text(8 + i * 2.6, y + 4, d, ha='left', va='center', fontsize=8.4, color=INK)

arrow(ax, (2.5, 24), (2.5, 84), lw=1.5, color=ACC, ms=11)
ax.text(0.6, 54, '烈\n度\n递\n增', ha='center', va='center', fontsize=9,
        color=ACC, linespacing=1.6)

# 阶梯与四要素的关联
ax.plot([58, 62], [77, 77], color=ACC, lw=1.0, ls=':')
ax.plot([58, 62], [26, 26], color=ACC, lw=1.0, ls=':')
ax.plot([62, 62], [26, 77], color=ACC, lw=1.0, ls=':')
arrow(ax, (62, 51.5), (66, 51.5), lw=1.3, color=ACC, ms=10)
ax.text(63.5, 59, '每一级\n均须明确', ha='center', va='center',
        fontsize=8.4, color=ACC, linespacing=1.5)

box(ax, 66, 24, 33, 68, fc=FILL1, ec=ACC, lw=1.4)
ax.text(82.5, 86, '手段的“四要素”', ha='center', va='center',
        fontsize=10.5, weight='bold', color=ACC)
elems = [('手　段', '拟采用的技术措施'),
         ('主　体', '谁依法有权使用'),
         ('授　权', '经何种程序批准'),
         ('约　束', '受何法律限制、担何后果')]
for i, (a, b) in enumerate(elems):
    y = 70 - i * 13
    box(ax, 69, y, 27, 9.5, fc=FILL4, ec=LINE)
    ax.text(72, y + 6.4, a, ha='left', va='center', fontsize=9.4,
            weight='bold', color=ACC)
    ax.text(72, y + 2.7, b, ha='left', va='center', fontsize=7.8, color=INK)
    if i < 3:
        arrow(ax, (82.5, y), (82.5, y - 3.3), ms=8, color=ACC)

box(ax, 2.5, 12.5, 96.5, 7.5,
    '手段的可用性首先取决于法律授权，其次才是技术有效性',
    fc=ACC, ec=ACC, fs=11, tc='white', weight='bold', lw=1.2)

box(ax, 2.5, 1, 96.5, 9,
    '级间跃迁由法律要件触发，而非距离、高度、驻留时间等技术阈值；\n'
    '智能化可加速探测识别到处置建议的链条，但最终授权必须由人保留——机器可以“建议”，不可“自主决定”',
    fc=HL, ec=ACC, fs=9, lw=1.2)

save(fig, 'fig4_legal_response.png')


# ═════════ 图5 “侦救一体”四步应急战法 ═════════
fig, ax = canvas(11.6, 4.4)

box(ax, 5, 87, 90, 10,
    '“侦救一体”：同一无人平台（群）在一次出动中连续完成灾情搜索定位与物资投送或人员转运，避免两次出动之间的时间断档',
    fc=FILL2, ec=ACC, fs=9.2, lw=1.3)

steps = [('第一步\n先侦后救',
          '正射影像、三维建模\n与SAR穿云侦察，\n短时形成“灾情一张图”',
          '2024·华容洞庭湖决口\n2025·西藏定日地震'),
         ('第二步\n断点续传',
          '系留、中继与大型固定翼\n无人机空中基站组网，\n重建“三断”条件下的通信',
          '2025·台风“桦加沙”\n4小时恢复1960名用户'),
         ('第三步\n分级投送',
          '轻型平台“精准滴灌”，\n重型平台吊运、加固堤坝\n乃至人员转移',
          '2026·广西横州特大洪灾\n“破例”吊运转移被困人员'),
         ('第四步\n协同编组',
          '专业力量、军队与民间飞手\n明确任务分工、统一空域调度、\n规范准入与指挥',
          '“军地协同”约束的直接体现\n当前最需规范化的环节')]
w = 21.5
for i, (h, d, c) in enumerate(steps):
    x = 3 + i * 24
    box(ax, x, 18, w, 60, fc=FILL4, ec=ACC, lw=1.2)
    box(ax, x, 63, w, 15, h, fc=FILL2, ec=ACC, fs=9.6, weight='bold', tc=ACC)
    ax.text(x + w / 2, 48, d, ha='center', va='center', fontsize=8.1,
            color=INK, linespacing=1.8)
    ax.plot([x + 2, x + w - 2], [32, 32], color='#bbbbbb', lw=0.8)
    ax.text(x + w / 2, 25, c, ha='center', va='center', fontsize=7.8,
            color=ACC, linespacing=1.7, style='italic')
    if i < 3:
        arrow(ax, (x + w, 48), (x + 24, 48), lw=1.4, color=ACC, ms=10)

ax.text(50, 9, '案例来源：应急管理部、新华社等公开报道', ha='center',
        fontsize=8, color='#666666')

save(fig, 'fig5_rescue_four_steps.png')


# ═════════ 图6 双场景比较与四条共性规律 ═════════
fig, ax = canvas(9.8, 6.2)

box(ax, 3, 74, 44, 22, fc=FILL3, ec=ACC, lw=1.3)
ax.text(25, 91.5, '对抗性　大型活动“低慢小”防控', ha='center', va='center',
        fontsize=10, weight='bold', color=ACC)
ax.text(25, 82, '在受控空域中\n把“闯入者”识别出来加以处置\n（“对手”是威胁主体）',
        ha='center', va='center', fontsize=8.8, color=INK, linespacing=1.8)

box(ax, 53, 74, 44, 22, fc=FILL2, ec=ACC, lw=1.3)
ax.text(75, 91.5, '非对抗性　抢险救灾应急运用', ha='center', va='center',
        fontsize=10, weight='bold', color=ACC)
ax.text(75, 82, '在混乱空域中\n把“自己人”组织起来协同作业\n（“对手”是灾害）',
        ha='center', va='center', fontsize=8.8, color=INK, linespacing=1.8)

arrow(ax, (25, 74), (25, 68.5), lw=1.3, color=ACC)
arrow(ax, (75, 74), (75, 68.5), lw=1.3, color=ACC)
ax.plot([25, 75], [68.5, 68.5], color=ACC, lw=1.3)
arrow(ax, (50, 68.5), (50, 63), lw=1.4, color=ACC)

box(ax, 14, 51.5, 72, 11,
    '同一技术底座：低空空域的实时态势感知与统一调度',
    fc=ACC, ec=ACC, fs=11, tc='white', weight='bold', lw=1.2)
arrow(ax, (50, 51.5), (50, 45.5), lw=1.4, color=ACC)
ax.text(50, 42.5, '由此提炼四条共性规律', ha='center', va='center',
        fontsize=10.5, weight='bold', color=ACC)

laws = [('其一　人机功能分配', '探测识别、持续值守、危险抵近交给机器；\n研判决策、授权处置、价值判断留给人', '谁来干'),
        ('其二　数据同源复用', '“运行识别白名单”与“灾情一张图”共享\n同一数据底座，应一体化建设、多任务复用', '靠什么干'),
        ('其三　制度是效能倍增器', '运行识别国标未增一台探测设备，\n却重构了探测识别的问题结构', '凭什么能干'),
        ('其四　能力平战迁移', '沿数据、平台、人员三条路径迁移，\n安保与救灾能力可相互转换', '练了有什么用')]
for i, (h, d, q) in enumerate(laws):
    x = 2 + (i % 2) * 49
    y = 20 - (i // 2) * 19
    box(ax, x, y, 47, 17, fc=FILL1, ec=LINE)
    ax.text(x + 2.5, y + 12.8, h, ha='left', va='center',
            fontsize=9.4, weight='bold', color=ACC)
    ax.text(x + 2.5, y + 5.6, d, ha='left', va='center',
            fontsize=7.9, color=INK, linespacing=1.7)
    ax.text(x + 44.5, y + 12.8, f'［{q}］', ha='right', va='center',
            fontsize=8, color=ACC)

save(fig, 'fig6_comparison_laws.png')

print('ALL DONE')
