# -*- coding: utf-8 -*-
"""Reconstruct Georgy Marinenko's CV in English (faithful translation of the
current Russian version), matching the original layout. Uses only '-' (hyphen),
no en/em dashes."""
import os
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
story.append(P("GEORGY MARINENKO", "name"))
story.append(P("Senior Product Owner / Product Lead - FinTech, Digital Operations &amp; B2B Platforms", "subtitle"))
story.append(P("Tbilisi, Georgia · Open to remote roles and relocation", "meta"))
story.append(P("georgy.marinenko@gmail.com · +7 917 564 2590 · +995 591 129 308 · Telegram: @gggggeorgii · Instagram: @gggggeorgii", "meta"))
story.append(Rule(1.1, RULE_NAVY, 6, 3))

# ===== PROFESSIONAL SUMMARY =====
story += section("PROFESSIONAL SUMMARY")
summary = [
 "I am a product manager with six years of experience building and scaling digital products across fintech, logistics, B2B SaaS, electronic document management and regulated industries.",
 "Today I am growing the service and delivery vertical at a major bank. I own the product side of processes used by thousands of users every month: 40,000+ deliveries nationwide, work with 7,000+ field-service employees and three development teams. I operate at the intersection of strategy, customer experience, operations and product economics: I frame and test hypotheses, analyse funnels and user behaviour with metrics I built into my own products, model unit economics, improve SLAs and look for points of efficiency growth.",
 "I favour a hands-on, entrepreneurial approach to product. Alongside my employed roles I launched and ran my own businesses: I owned P&amp;L, pricing, sales, marketing, customer service and operations - through to a successful exit from one of the projects. This experience helps me see a product not only through metrics and a roadmap, but also through the real value it delivers to the customer, the team and the business.",
 "My engineering background was shaped in part by working on real-time distributed systems in the aerospace industry. Because of it I collaborate confidently with engineering, understand technical constraints and can translate business goals into clear, implementable solutions.",
 "I am especially drawn to products at the intersection of everyday scenarios, service and loyalty.",
]
for i, para in enumerate(summary):
    st = ParagraphStyle("sm", parent=S["summary"], spaceBefore=(4 if i else 6))
    story.append(Paragraph(para, st))

# ===== CORE SKILLS =====
story += section("CORE SKILLS")
story.append(P(lab("Product Leadership:") + " Product Strategy · Product Discovery · Roadmapping · Backlog Management · Requirements &amp; User Stories · End-to-End Delivery · Agile/Scrum · Cross-functional Leadership · Stakeholder Management · Product Operations", "skill"))
story.append(P(lab("Analytics &amp; Growth:") + " Product Analytics · SQL · KPI Design · Funnel &amp; Conversion Analysis · Customer Journey Mapping · User Research · Market &amp; Competitor Research · Unit Economics · A/B Testing · Voice of Customer", "skill"))
story.append(P(lab("Domains:") + " FinTech · Digital Logistics &amp; Delivery · Digital Operations · B2B SaaS · Electronic Document Management · Workflow Automation · Regulated Products · Customer Experience", "skill"))
story.append(P(lab("Tools &amp; Technical Fluency:") + " Jira / Confluence · Notion · Figma · SQL · Python · C/C++ · Docker · Git · AI assistants &amp; workflow automation", "skill"))

# ===== PROFESSIONAL EXPERIENCE =====
story += section("PROFESSIONAL EXPERIENCE")

story += job("alfa",
  "Alfa-Bank - Director of Product, Service and Delivery Platforms",
  "Russia (remote) | April 2026 - Present",
  "Runs the product vertical for the bank's service and delivery ecosystem across three domains: product issuance in bank branches, inventory accounting and logistics for physical assets, and courier delivery of banking products to customers. Scale: " + hlbi("40,000+ deliveries per month") + " nationwide, " + hlbi("7,000+ field-service employees") + ".",
  [
   "Improved conversion to successful handover to " + hlb("98.3%") + " in the courier delivery channel and to " + hlb("92%") + " in bank branches.",
   "Leads " + hlb("three product teams") + " across these domains, aligning roadmaps, backlogs, priorities and resource allocation between them.",
   "Owns the outcome metrics - conversion, successful-delivery rate, SLA, NPS/CSAT, handover time - and runs continuous improvement cycles grounded in field data and unit economics.",
   "Automated a manual cross-selling process in the delivery channel, cutting " + hlb("~6 minutes") + " of handling time per sale and removing workload equivalent to " + hlb("10 FTE") + "; the approach was adopted by other product teams.",
   "Launched sales of banking products in branches for non-resident customers, opening a previously unserved segment.",
  ])

story += job("alfa",
  "Alfa-Bank - Head of Digital Products, Delivery",
  "Russia | July 2025 - April 2026",
  "Owned digital products for logistics operations and courier delivery of banking products to retail customers, including SIM-card delivery and activation flows for the bank's MVNO offering.",
  [
   "Reduced SIM-card handover time by " + hlb("3x") + " by identifying process bottlenecks and redesigning field operation scenarios.",
   "Improved successful-delivery conversion by " + hlb("9%") + " through a customer journey overhaul and logistics optimisation.",
   "Increased subscriber activation by " + hlb("8%") + " by introducing a new notification mechanism for field-service employees.",
   "Increased SIM-card handovers by " + hlb("6%") + " by launching an issuance flow for customers who were not yet bank clients; also launched SIM issuance with mobile-number portability.",
   "Developed and defended the 2026 product strategy for the delivery domain, managing teams across two product areas and grounding the conversion roadmap in analytics, UX research and unit-economics work.",
  ])

story += job("sber",
  "Sber - Product Owner, B2B Electronic Document Management Platform",
  "Russia | June 2024 - July 2025",
  "B2B platform for legally binding electronic document management (EDM) and business-process automation - replacing paper contracts, invoices and regulatory reporting with digital equivalents. " + hlbi("RUB 2.5B annual revenue") + "; " + hlbi("7,000-8,000 monthly active business customers") + ", from SMEs to the largest enterprises.",
  [
   "Owned the backlog of a cross-functional team of " + hlb("20+ specialists") + " (engineering, analytics, design, QA, architecture) and led the Double Diamond process from problem discovery to delivery.",
   "Ran user, market and competitor research; developed and defended a three-year product strategy for expansion into the external market.",
   "Initiated and led development of a prototype AI assistant for first-line customer support: ran a 1% traffic pilot to prove the concept, after which the assistant handled " + hlb("10% of ~12,000 monthly requests") + " at first touch, reducing agent workload.",
   "Identified a new market opportunity in everyday document-signing for individuals - healthcare, rental, and similar - assessed its potential and led the market entry process.",
   "Built the product's unit economics, identified underperforming acquisition channels and cut servicing costs; redesigned onboarding after finding that customer drop-off clustered around specific journey steps.",
   "Led the full development cycle of a new product from first principles to launch readiness; the initiative was recognised by a Sber Vice President as a potential game changer.",
  ])

story += job("znak",
  "ZNAK Corporation - Product Owner, B2B SaaS and Track &amp; Trace",
  "Russia | December 2022 - June 2024",
  "B2B SaaS and integrated solutions for Russia's state-mandated product labelling programme (CRPT, 'Chestny ZNAK'), which requires every unit of regulated goods to carry a unique traceable digital code. The products let manufacturers and retailers apply, scan and track those codes and stay compliant as the regulation changes.",
  [
   "Defined the product strategy for the B2B SaaS portfolio and grew average deal value by " + hlb("19.4% YoY") + " through a subscription model and portfolio rationalisation.",
   "Launched " + hlb("ZNAKCODE") + ", a new SaaS product that added a standalone revenue stream to the company.",
   "Cut time-to-market by introducing CI/CD practices - particularly valuable when regulatory deadlines tightened.",
   "Led the transition to microservices architecture, improving scalability across the product line.",
   "Built a structured Voice of Customer process and a unified L1-L3 support model; automated the project handoff workflow from initial sale through to ongoing customer support.",
   "Represented company solutions at CRPT product-labelling conferences and appeared as an industry expert in RBC news coverage.",
  ])

story += job("ural",
  "Ural Civil Aviation Plant - Software Engineer (Qt/C++)",
  "Russia | September 2020 - December 2022",
  None,
  [
   "Developed real-time embedded software for ground-station and antenna-positioning systems, including a distributed client-server architecture over TCP/IP and SNMP for remote monitoring and control.",
   "Delivered software to " + hlb("99.9% reliability") + " requirements in asynchronous, time-critical environments (C/C++, Python, Qt/QML, SQL, Docker, Git) - a background that makes technical conversations with architects and engineers genuinely productive.",
  ])

# ===== FOUNDER & OPERATOR EXPERIENCE =====
story += section("FOUNDER &amp; OPERATOR EXPERIENCE")

story += job("found",
  "CCO - Private Residential Development",
  "Russia | December 2021 - May 2024 (alongside full-time roles)",
  None,
  [
   "Owned the commercial side of a residential development project: " + hlb("16 houses") + " sold across two projects (average area ~240 m², average sale price ~RUB 40M each).",
   "Sold " + hlb("six houses within the first three months") + " of sales, generating " + hlb("~RUB 230M") + " in revenue - validating demand well ahead of the original schedule.",
   "Built the financial model and a per-unit pricing calculator, which made it possible to adjust each house's margin on the fly and actively manage pricing.",
   "Ran all commercial activity personally - marketing, sales, procurement and financial planning.",
  ])

story += job("found",
  "Founder / Franchisee - Massage Studio Business",
  "Russia | November 2024 - July 2026 (alongside full-time roles)",
  None,
  [
   "Launched and operated a massage studio that served " + hlb("7,000+ unique clients") + " in its first year and reached " + hlb("top-2 by revenue") + " in a national franchise network of 70 studios.",
   "Generated " + hlb("~RUB 22M") + " in first-year revenue, grew average customer spend by " + hlb("20%") + " and sustained " + hlb("~60% customer retention") + "; monthly revenue stayed within ~±15% through 2025-2026.",
   "Managed a " + hlb("team of 16") + ", owning customer experience, local marketing, CRM, scheduling and operations end to end.",
   "Exited the business, selling the studio in approximately 1.5 months.",
   "Packaged the operating model into a repeatable playbook: launched a second studio as a turnkey service for a partner, getting it open within a month and profitable within a quarter and a half.",
  ])

# ===== EDUCATION & PROFESSIONAL DEVELOPMENT =====
story += section("EDUCATION &amp; PROFESSIONAL DEVELOPMENT")
edu = [
 "MBA, Product Management - Moscow Business Academy, 2024",
 "BSc, Computer Science and Engineering - Moscow Aviation Institute (National Research University), 2022",
 "Customer Experience in Product Management - Sber, 2024",
 "Project Management - HSE University (Higher School of Economics), 2023",
 "School 21 (software engineering programme) - Sber, 2021",
]
for e in edu:
    story.append(P(BUL + e, "bullet"))

# ===== LANGUAGES =====
story.append(P('<font name="Carlito-Bold" size="10" color="' + NAVY + '">LANGUAGES:</font>&nbsp;&nbsp;Russian - Native · English - Intermediate (B1), actively improving; practical written English and presentations.', "lang"))

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Georgy_Marinenko_CV_EN.pdf")
doc = SimpleDocTemplate(OUT, pagesize=letter,
                        leftMargin=40, rightMargin=40, topMargin=28, bottomMargin=34,
                        title="Georgy Marinenko - CV", author="Georgy Marinenko")
doc.build(story)
print("WROTE", OUT)
