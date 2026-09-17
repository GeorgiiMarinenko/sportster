# -*- coding: utf-8 -*-
"""Reconstruct Georgy Marinenko's CV in Russian, matching the original layout."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Flowable,
                                KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT

FDIR = "/usr/share/fonts/truetype/crosextra/"
pdfmetrics.registerFont(TTFont("Carlito", FDIR + "Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Bold", FDIR + "Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-Italic", FDIR + "Carlito-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Carlito-BoldItalic", FDIR + "Carlito-BoldItalic.ttf"))
registerFontFamily("Carlito", normal="Carlito", bold="Carlito-Bold",
                   italic="Carlito-Italic", boldItalic="Carlito-BoldItalic")
pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))

# ---- colours ----
NAVY = "#1f3a5f"
BLUE = "#2b6cb0"
GRAY = "#5a6372"
BODY = "#1a1a1a"
RULE_LIGHT = HexColor("#c2c8d0")
RULE_NAVY = HexColor(NAVY)
MK = {"alfa": "#ef3124", "sber": "#21a038", "znak": "#2b5ca8",
      "ural": "#a32639", "found": "#c0873f"}

RUB = '<font name="DejaVu">₽</font>'  # ruble sign (Carlito lacks it)

def hlb(t):   # bold navy highlight (body)
    return f'<font name="Carlito-Bold" color="{NAVY}">{t}</font>'
def hlbi(t):  # bold-italic navy highlight (description)
    return f'<font name="Carlito-BoldItalic" color="{NAVY}">{t}</font>'
def lab(t):   # bold navy inline label
    return f'<font name="Carlito-Bold" color="{NAVY}">{t}</font>'

# ---- styles ----
S = {}
S["name"]    = ParagraphStyle("name", fontName="Carlito-Bold", fontSize=17,
                              textColor=HexColor(NAVY), leading=19, spaceAfter=0)
S["subtitle"]= ParagraphStyle("subtitle", fontName="Carlito-Bold", fontSize=10,
                              textColor=HexColor(BLUE), leading=13, spaceBefore=6)
S["meta"]    = ParagraphStyle("meta", fontName="Carlito", fontSize=8.5,
                              textColor=HexColor(GRAY), leading=11.5, spaceBefore=4)
S["section"] = ParagraphStyle("section", fontName="Carlito-Bold", fontSize=10,
                              textColor=HexColor(NAVY), leading=12, spaceBefore=9)
S["body"]    = ParagraphStyle("body", fontName="Carlito", fontSize=9,
                              textColor=HexColor(BODY), leading=12.6, spaceBefore=0)
S["skill"]   = ParagraphStyle("skill", fontName="Carlito", fontSize=9,
                              textColor=HexColor(BODY), leading=12.7, spaceBefore=3)
S["summary"] = ParagraphStyle("summary", fontName="Carlito", fontSize=9,
                              textColor=HexColor(BODY), leading=12.9, spaceBefore=6)
S["jobtitle"]= ParagraphStyle("jobtitle", fontName="Carlito-Bold", fontSize=9.5,
                              textColor=HexColor(NAVY), leading=12.5, spaceBefore=7)
S["jobmeta"] = ParagraphStyle("jobmeta", fontName="Carlito-Italic", fontSize=8.5,
                              textColor=HexColor(GRAY), leading=11.5, spaceBefore=2)
S["jobdesc"] = ParagraphStyle("jobdesc", fontName="Carlito-Italic", fontSize=8.5,
                              textColor=HexColor(GRAY), leading=11.9, spaceBefore=2,
                              leftIndent=15.8)
S["bullet"]  = ParagraphStyle("bullet", fontName="Carlito", fontSize=9,
                              textColor=HexColor(BODY), leading=12.6, spaceBefore=2,
                              leftIndent=15.8, firstLineIndent=-9.3)
S["lang"]    = ParagraphStyle("lang", fontName="Carlito", fontSize=9,
                              textColor=HexColor(BODY), leading=12.6, spaceBefore=9)

BUL = f'<font name="Carlito" size="8" color="{BLUE}">▪</font>&nbsp;&nbsp;'

class Rule(Flowable):
    def __init__(self, thickness=0.5, color=RULE_LIGHT, sb=1, sa=4, width=None):
        super().__init__()
        self.t = thickness; self.c = color; self.sb = sb; self.sa = sa; self.w = width
    def wrap(self, aw, ah):
        self.aw = self.w or aw
        return (self.aw, self.t + self.sb + self.sa)
    def draw(self):
        self.canv.setStrokeColor(self.c); self.canv.setLineWidth(self.t)
        y = self.sa + self.t / 2.0
        self.canv.line(0, y, self.aw, y)

def P(text, style):
    return Paragraph(text, S[style])

def section(title):
    return [P(title, "section"), Rule(0.5, RULE_LIGHT, 1, 4)]

def job(marker, title, meta, desc, bullets):
    """A job entry; keep the header+meta+first line together."""
    flow = []
    mk = MK[marker]
    sq = f'<font name="DejaVu" size="10" color="{mk}">■</font>&nbsp;&nbsp;'
    head = [P(sq + title, "jobtitle"), P(meta, "jobmeta")]
    if desc:
        head.append(P(desc, "jobdesc"))
    flow.append(KeepTogether(head))
    for b in bullets:
        flow.append(P(BUL + b, "bullet"))
    return flow

story = []

# ===== HEADER =====
story.append(P("ГЕОРГИЙ МАРИНЕНКО", "name"))
story.append(P("Senior Product Owner / Product Lead — финтех, цифровые операции и B2B-платформы", "subtitle"))
story.append(P("Тбилиси, Грузия · Открыт к удалённой работе и релокации", "meta"))
story.append(P("georgy.marinenko@gmail.com · +7 917 564 2590 · +995 591 129 308 · Telegram: @gggggeorgii · Instagram: @gggggeorgii", "meta"))
story.append(Rule(1.1, RULE_NAVY, 6, 3))

# ===== О СЕБЕ =====
story += section("О СЕБЕ")
summary = [
 "Я продуктовый менеджер с шестилетним опытом создания и развития цифровых продуктов в финтехе, логистике, B2B SaaS, электронном документообороте и регулируемых отраслях.",
 "Сейчас я развиваю направление сервисных услуг и доставки в крупном банке. В зоне моей ответственности — продуктовая часть процессов, которыми ежемесячно пользуются тысячи пользователей: более 40 000 доставок по всей стране, работа с 7 000+ выездными сотрудниками и три команды разработки. Я работаю на стыке стратегии, клиентского опыта, операционных процессов и экономики продукта: формулирую и проверяю гипотезы, анализирую воронки и поведение пользователей с помощью метрик, которые сам и построил в своих продуктах, считаю юнит-экономику, улучшаю SLA и ищу точки роста эффективности.",
 "Мне близок практический, предпринимательский подход к продукту. Параллельно с работой в найме я запускал и управлял собственными бизнесами: отвечал за P&L, ценообразование, продажи, маркетинг, клиентский сервис и операционные процессы — вплоть до успешного выхода из одного из проектов. Этот опыт помогает мне смотреть на продукт не только через метрики и roadmap, но и через реальную ценность для клиента, команды и бизнеса.",
 "Мой инженерный бэкграунд сформировался в том числе в работе над распределёнными системами реального времени в аэрокосмической отрасли. Благодаря этому я уверенно взаимодействую с разработкой, понимаю технические ограничения и умею переводить бизнес-задачи в понятные, реализуемые решения.",
 "Мне особенно интересны продукты на пересечении повседневных сценариев, сервиса, лояльности и удобного клиентского опыта.",
]
for i, para in enumerate(summary):
    st = ParagraphStyle("sm", parent=S["summary"], spaceBefore=(4 if i else 6))
    story.append(Paragraph(para, st))

# ===== КЛЮЧЕВЫЕ НАВЫКИ =====
story += section("КЛЮЧЕВЫЕ НАВЫКИ")
story.append(P(lab("Продуктовое лидерство:") + " Продуктовая стратегия · Product Discovery · Построение роадмапов · Управление бэклогом · Требования и user stories · Сквозная поставка (end-to-end) · Agile/Scrum · Кросс-функциональное лидерство · Управление стейкхолдерами · Продуктовые операции", "skill"))
story.append(P(lab("Аналитика и рост:") + " Продуктовая аналитика · SQL · Дизайн KPI · Анализ воронок и конверсии · Customer Journey Mapping · Пользовательские исследования · Анализ рынка и конкурентов · Юнит-экономика · A/B-тестирование · Voice of Customer", "skill"))
story.append(P(lab("Домены:") + " Финтех · Цифровая логистика и доставка · Цифровые операции · B2B SaaS · Электронный документооборот · Автоматизация процессов · Регулируемые продукты · Клиентский опыт", "skill"))
story.append(P(lab("Инструменты и технологии:") + " Jira / Confluence · Notion · Figma · SQL · Python · C/C++ · Docker · Git · AI-ассистенты и автоматизация процессов", "skill"))

# ===== ОПЫТ РАБОТЫ =====
story += section("ОПЫТ РАБОТЫ")

story += job("alfa",
  "Альфа-Банк — директор по продукту, платформы сервиса и доставки",
  "Россия (удалённо) | апрель 2026 — настоящее время",
  "Отвечаю за продуктовую вертикаль экосистемы сервиса и доставки банка в трёх доменах: выдача продуктов в отделениях, складской учёт и логистика физических активов, курьерская доставка банковских продуктов клиентам. Масштаб: " + hlbi("40 000+ доставок в месяц") + " по всей стране, " + hlbi("7 000+ выездных сотрудников") + ".",
  [
   "Повысил конверсию в успешную выдачу до " + hlb("98,3%") + " в канале курьерской доставки и до " + hlb("92%") + " в отделениях банка.",
   "Руковожу " + hlb("тремя продуктовыми командами") + " в этих доменах: синхронизирую роадмапы, бэклоги, приоритеты и распределение ресурсов между ними.",
   "Отвечаю за продуктовые метрики — конверсия, доля успешных доставок, SLA, NPS/CSAT, время выдачи — и веду циклы непрерывных улучшений на основе полевых данных и юнит-экономики.",
   "Автоматизировал ручной процесс кросс-продаж в канале доставки: сократил время обработки на " + hlb("~6 минут") + " на сделку и снял нагрузку, эквивалентную " + hlb("10 FTE") + "; подход переняли другие продуктовые команды.",
   "Запустил продажи банковских продуктов в отделениях для клиентов-нерезидентов, открыв ранее неохваченный сегмент.",
  ])

story += job("alfa",
  "Альфа-Банк — руководитель цифровых продуктов, доставка",
  "Россия | июль 2025 — апрель 2026",
  "Отвечал за цифровые продукты логистических операций и курьерской доставки банковских продуктов розничным клиентам, включая доставку и активацию SIM-карт для MVNO-направления банка.",
  [
   "Сократил время выдачи SIM-карт в " + hlb("3 раза") + ", выявив узкие места процесса и переработав сценарии полевых операций.",
   "Повысил конверсию в успешную доставку на " + hlb("9%") + " за счёт переработки клиентского пути и оптимизации логистики.",
   "Увеличил активацию абонентов на " + hlb("8%") + ", внедрив новый механизм уведомлений для выездных сотрудников.",
   "Увеличил число выдач SIM-карт на " + hlb("6%") + ", запустив сценарий выдачи для клиентов, ещё не являвшихся клиентами банка; также запустил выдачу SIM с переносом номера (MNP).",
   "Разработал и защитил продуктовую стратегию домена доставки на 2026 год, управляя командами в двух продуктовых направлениях и обосновав роадмап по конверсии аналитикой, UX-исследованиями и юнит-экономикой.",
  ])

story += job("sber",
  "Сбер — Product Owner, B2B-платформа электронного документооборота",
  "Россия | июнь 2024 — июль 2025",
  "B2B-платформа юридически значимого электронного документооборота (ЭДО) и автоматизации бизнес-процессов — замена бумажных договоров, счетов и регуляторной отчётности цифровыми аналогами. " + hlbi("Выручка 2,5 млрд " + RUB + " в год") + "; " + hlbi("7 000–8 000 активных бизнес-клиентов в месяц") + " — от МСБ до крупнейших предприятий.",
  [
   "Вёл бэклог кросс-функциональной команды из " + hlb("20+ специалистов") + " (разработка, аналитика, дизайн, QA, архитектура) и руководил процессом Double Diamond от исследования проблемы до поставки.",
   "Проводил пользовательские, рыночные и конкурентные исследования; разработал и защитил трёхлетнюю продуктовую стратегию выхода на внешний рынок.",
   "Инициировал и возглавил разработку прототипа AI-ассистента для первой линии поддержки: провёл пилот на 1% трафика для проверки концепции, после чего ассистент обрабатывал " + hlb("10% из ~12 000 обращений в месяц") + " на первом контакте, снижая нагрузку на операторов.",
   "Обнаружил новую рыночную возможность в повседневном подписании документов для физлиц — медицина, аренда и подобное — оценил её потенциал и возглавил процесс выхода на рынок.",
   "Построил юнит-экономику продукта, выявил неэффективные каналы привлечения и сократил затраты на обслуживание; переработал онбординг, обнаружив, что отток пользователей концентрируется на определённых шагах пути.",
   "Провёл полный цикл разработки нового продукта — от первых принципов до готовности к запуску; инициативу вице-президент Сбера отметил как потенциально прорывную.",
  ])

story += job("znak",
  "Корпорация ЗНАК — Product Owner, B2B SaaS и маркировка (Track & Trace)",
  "Россия | декабрь 2022 — июнь 2024",
  "B2B SaaS и интеграционные решения для государственной системы маркировки товаров (ЦРПТ, «Честный ЗНАК»), которая требует наносить на каждую единицу регулируемого товара уникальный отслеживаемый цифровой код. Продукты позволяют производителям и ритейлерам наносить, сканировать и отслеживать коды и соответствовать меняющимся требованиям регулятора.",
  [
   "Определил продуктовую стратегию портфеля B2B SaaS и увеличил средний чек сделки на " + hlb("19,4% год к году") + " за счёт подписной модели и оптимизации портфеля.",
   "Запустил " + hlb("ZNAKCODE") + " — новый SaaS-продукт, создавший отдельный поток выручки для компании.",
   "Сократил time-to-market, внедрив практики CI/CD — особенно ценно при ужесточении регуляторных сроков.",
   "Возглавил переход на микросервисную архитектуру, повысив масштабируемость всей продуктовой линейки.",
   "Выстроил структурированный процесс Voice of Customer и единую модель поддержки L1–L3; автоматизировал передачу проекта от первичной продажи до дальнейшего клиентского сопровождения.",
   "Представлял решения компании на отраслевых конференциях по маркировке (ЦРПТ) и выступал отраслевым экспертом в материалах РБК.",
  ])

story += job("ural",
  "Уральский завод гражданской авиации — инженер-программист (Qt/C++)",
  "Россия | сентябрь 2020 — декабрь 2022",
  None,
  [
   "Разрабатывал встраиваемое ПО реального времени для наземных станций и систем наведения антенн, включая распределённую клиент-серверную архитектуру поверх TCP/IP и SNMP для удалённого мониторинга и управления.",
   "Обеспечивал соответствие ПО требованиям надёжности " + hlb("99,9%") + " в асинхронных, критичных ко времени средах (C/C++, Python, Qt/QML, SQL, Docker, Git) — этот бэкграунд делает технические обсуждения с архитекторами и инженерами по-настоящему продуктивными.",
  ])

# ===== ПРЕДПРИНИМАТЕЛЬСКИЙ ОПЫТ =====
story += section("ПРЕДПРИНИМАТЕЛЬСКИЙ ОПЫТ")

story += job("found",
  "Основатель — частное загородное строительство",
  "Россия | декабрь 2021 — май 2024 (параллельно с основной работой)",
  None,
  [
   "Создал бизнес по загородному строительству и сдал " + hlb("16 домов") + " в двух проектах (средняя площадь ~240 м², средняя цена продажи ~40 млн " + RUB + " за дом).",
   "Продал " + hlb("шесть домов за первые три месяца") + " продаж, получив " + hlb("~230 млн " + RUB) + " выручки, — подтвердив спрос значительно раньше плана.",
   "С нуля построил финансовую модель, калькулятор ценообразования и P&L на каждый объект и опирался на них в каждом коммерческом решении.",
   "Вёл всю коммерческую деятельность лично — маркетинг, продажи, закупки и финансовое планирование — и координировал график строительства и сдачи от начала до конца.",
  ])

story += job("found",
  "Основатель / франчайзи — сеть массажных студий",
  "Россия | ноябрь 2024 — июль 2026 (параллельно с основной работой)",
  None,
  [
   "Запустил и вёл массажную студию, которая за первый год обслужила " + hlb("7 000+ уникальных клиентов") + " и вышла в " + hlb("топ-2 по выручке") + " в федеральной франшизной сети из 70 студий.",
   "Сгенерировал " + hlb("~22 млн " + RUB) + " выручки за первый год, увеличил средний чек на " + hlb("20%") + " и удержал " + hlb("~60% возвращаемость клиентов") + "; месячная выручка держалась в пределах ~±15% в 2025–2026.",
   "Управлял " + hlb("командой из 16 человек") + ", отвечая за клиентский опыт, локальный маркетинг, CRM, расписание и операционные процессы целиком.",
   "Вышел из бизнеса, продав студию примерно за 1,5 месяца.",
   "Упаковал операционную модель в тиражируемый плейбук: запустил вторую студию «под ключ» для партнёра, открыв её за месяц и выведя в прибыль за полтора квартала.",
  ])

# ===== ОБРАЗОВАНИЕ =====
story += section("ОБРАЗОВАНИЕ И ПРОФЕССИОНАЛЬНОЕ РАЗВИТИЕ")
edu = [
 "MBA, продуктовый менеджмент — Moscow Business Academy, 2024",
 "Бакалавр, информатика и вычислительная техника — Московский авиационный институт (МАИ), 2022",
 "Клиентский опыт в продуктовом менеджменте — Сбер, 2024",
 "Управление проектами — НИУ ВШЭ (Высшая школа экономики), 2023",
 "Школа 21 (программа по разработке ПО) — Сбер, 2021",
]
for e in edu:
    story.append(P(BUL + e, "bullet"))

# ===== ЯЗЫКИ =====
story.append(P('<font name="Carlito-Bold" size="10" color="' + NAVY + '">ЯЗЫКИ:</font>&nbsp;&nbsp;Русский — родной · Английский — средний (B1), активно развиваю; уверенная деловая переписка и презентации.', "lang"))

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Georgy_Marinenko_CV_RU.pdf")
doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=40, rightMargin=40, topMargin=28, bottomMargin=34,
                        title="Георгий Мариненко — резюме",
                        author="Георгий Мариненко")
doc.build(story)
print("WROTE", OUT)
