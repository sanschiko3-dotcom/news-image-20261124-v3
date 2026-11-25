from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W = H = 1024
PAPER = '#F7F2E7'
INK = '#111111'
RED = '#A41E22'
NAVY = '#102A4A'
BLUE = '#DCE9E8'
LAND = '#E4D6B8'
MUTED = '#655F55'
RULE = '#B9B1A4'

SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
SANS_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def font(path, size):
    return ImageFont.truetype(path, size)

im = Image.new('RGB', (W, H), PAPER)
d = ImageDraw.Draw(im)


def text(x, y, s, f, fill=INK):
    d.text((x, y), s, font=f, fill=fill)


def wrap(s, f, width):
    out, line = [], ''
    for word in s.split():
        test = word if not line else line + ' ' + word
        if d.textlength(test, font=f) <= width:
            line = test
        else:
            if line:
                out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def paragraph(x, y, s, f, width, fill=INK, leading=3, max_lines=None):
    lines = wrap(s, f, width)
    if max_lines is not None and len(lines) > max_lines:
        raise ValueError(f'Text overflows ({len(lines)} lines, max {max_lines}): {s}')
    step = f.size + leading
    for i, line in enumerate(lines):
        text(x, y + i * step, line, f, fill)
    return y + len(lines) * step


def rule(x1, y1, x2, y2, fill=RULE, width=1):
    d.line((x1, y1, x2, y2), fill=fill, width=width)

# Masthead and date rail
text(30, 15, 'THE WORLD TODAY', font(SERIF, 38), NAVY)
text(650, 22, 'TUESDAY, 24 NOVEMBER 2026', font(SANS_B, 15), INK)
text(650, 49, 'THE DAY IN ONE PAGE', font(SANS, 13), MUTED)
rule(30, 84, 994, 84, INK, 2)

# Lead report: broad left text column plus a large, legible schematic map.
text(30, 99, 'UKRAINE  /  LIBYA  /  WAR AT SEA', font(SANS_B, 12), RED)
lead_head = 'UKRAINE SEA DRONES SINK RUSSIAN WARSHIP OFF LIBYA'
paragraph(30, 119, lead_head, font(SERIF, 26), 535, NAVY, 1, 2)
lead_deck = ('After the Sunday 23 Nov attack, Zelensky confirmed Monday that seven Ukrainian naval drones sank the corvette Merkury at Benghazi. '
             'Commissioned in 2023, it was among Russia’s newest warships; its Ka-27 helicopter was destroyed, and cargo ship MV Angara was also hit.')
paragraph(30, 187, lead_deck, font(SANS, 14), 536, INK, 4, 5)

# Mediterranean panel
mx, my, mw, mh = 588, 104, 406, 198
d.rectangle((mx, my, mx+mw, my+mh), fill=BLUE, outline=NAVY, width=2)
text(mx+13, my+9, 'MEDITERRANEAN SEA', font(SANS_B, 11), NAVY)
# North African coast and Libya, deliberately simplified as map geometry.
d.polygon([(mx+3,my+118),(mx+48,my+111),(mx+86,my+115),(mx+125,my+110),(mx+166,my+114),
           (mx+203,my+109),(mx+239,my+112),(mx+272,my+105),(mx+309,my+111),(mx+351,my+104),
           (mx+403,my+110),(mx+403,my+197),(mx+3,my+197)], fill=LAND)
# Libya/Egypt boundary and coast detail
rule(mx+272, my+106, mx+272, my+195, '#9C8D70', 1)
text(mx+190, my+148, 'LIBYA', font(SANS_B, 15), NAVY)
text(mx+307, my+146, 'EGYPT', font(SANS_B, 10), MUTED)
text(mx+18, my+143, 'NORTH AFRICA', font(SANS, 9), MUTED)
# Benghazi marker and leader
bx, by = mx+225, my+111
d.ellipse((bx-5,by-5,bx+5,by+5), fill=RED, outline=PAPER, width=1)
text(bx-53, by-24, 'BENGHAZI', font(SANS_B, 10), RED)
# Drone trajectories, dashed approach tracks
for x1,y1,x2,y2 in [(mx+82,my+29,bx-8,by-8),(mx+126,my+19,bx+4,by-9)]:
    steps = 18
    for j in range(0, steps, 2):
        a, b = j/steps, min((j+1)/steps,1)
        d.line((x1+(x2-x1)*a,y1+(y2-y1)*a,x1+(x2-x1)*b,y1+(y2-y1)*b), fill=RED, width=2)
# small drone chevrons
for px,py in [(mx+83,my+29),(mx+127,my+19)]:
    d.polygon([(px-6,py),(px+4,py-4),(px+1,py+1),(px+7,py+4)], fill=NAVY)
# Warship, blast star and helicopter annotation
sx, sy = bx+29, by+6
d.polygon([(sx-24,sy),(sx-14,sy-5),(sx+16,sy-5),(sx+25,sy),(sx+15,sy+5),(sx-18,sy+5)], fill=NAVY)
rule(sx-9, sy-5, sx-9, sy-11, NAVY, 2)
# explosion burst
pts=[]
for k in range(16):
    import math
    a=-math.pi/2+k*math.pi/8
    r=13 if k%2==0 else 6
    pts.append((sx+math.cos(a)*r,sy+math.sin(a)*r))
d.polygon(pts, fill=RED)
text(sx+18, sy-24, 'MERKURY', font(SANS_B, 9), NAVY)
# Ka-27 silhouette label at upper right
hx, hy = mx+344, my+42
rule(hx-12,hy,hx+10,hy,NAVY,2); rule(hx-2,hy-5,hx-2,hy+5,NAVY,1)
d.ellipse((hx-5,hy-3,hx+3,hy+3), fill=NAVY)
text(hx-29, hy+9, 'Ka-27 lost', font(SANS, 9), NAVY)
text(mx+13, my+174, 'SCHEMATIC  •  BENGHAZI, LIBYA', font(SANS, 9), MUTED)

# Lead stat strip
stat_y = 309
d.rectangle((30,stat_y,994,stat_y+29), fill=NAVY)
text(43, stat_y+6, '7 DRONES   ·   1 CORVETTE SUNK   ·   1 Ka-27 DESTROYED   ·   1 CARGO SHIP HIT', font(SANS_B, 13), PAPER)
rule(30, 348, 994, 348, INK, 2)

# Four-column news grid. Each panel carries a kicker, schematic mark, headline and fact deck.
stories = [
 ('CLIMATE', 'COP31 COLLAPSES IN ANTALYA', 'After about 50 hours of overtime, talks broke up. More than 90 nations, including the entire EU, rejected a draft that never says “fossil fuels”—a “darkest moment” for climate diplomacy.', 'climate'),
 ('SECURITY', 'NATO COUNTS 25 AIRSPACE VIOLATIONS', 'The alliance logged 25 Russian airspace violations in 2026. Debris from a 20 Nov incident was found in Poland; Putin signalled openness to Article 5-style guarantees.', 'security'),
 ('MIDDLE EAST', 'US SANCTIONS IRAN; QATAR MEDIATES', 'Treasury imposed new Iran sanctions as Qatar mediates US–Tehran talks. Iran rules out talks until seven conditions are met and says four tankers hit Hormuz mines on 23 Nov.', 'iran'),
 ('JUSTICE', '14 STATES BACK ROHINGYA CASE AT ICJ', 'The UK, Spain, Canada, Australia and 10 others back the genocide case against Myanmar. The ICJ ruled last week that Myanmar committed genocide against the Rohingya.', 'justice'),
 ('MARKETS', 'HUANG RETURNS AS NVIDIA CEO', 'Nvidia’s board reinstated Jensen Huang on Monday, less than two weeks after pushing him out. The Nasdaq jumped 6.51% to 24,089.56 on the day.', 'markets'),
 ('DISASTER', 'NEPAL SHAKEN BY 5.6 QUAKE', 'A magnitude 5.6 earthquake struck Nepal near the Chinese border, shaking the Himalayan region on Tuesday.', 'quake'),
 ('WAR AT SEA', 'SPARTA II ABLAZE IN THE BALTIC', 'Two drones struck Russian-flagged Sparta II in the Gulf of Finland on 21 Nov. Fire smouldered on 22 Nov; towing began. All 16 crew evacuated, one slightly injured. Finland, Estonia and Russia fought the blaze; Zelensky confirmed Ukraine struck.', 'ship'),
 ('DIPLOMACY', 'NO UKRAINE DEAL AT SHENZHEN SUMMIT', 'Trump, Putin and Xi met in Shenzhen on 19 Nov for 3+ hours (90-minute trilateral). Declaration: nuclear security, energy, UN reform. No Ukraine deal or concrete progress, ceasefire or timetable; Ukraine and Europe absent.', 'summit'),
]

# Small flat glyphs, differentiated by story, not illustrative scenes.
def icon(x,y,kind):
    c=RED
    if kind=='climate':
        d.ellipse((x+5,y+2,x+18,y+18),outline=NAVY,width=2); rule(x+11,y+3,x+11,y+18,NAVY,1); rule(x+5,y+10,x+18,y+10,NAVY,1)
    elif kind=='security':
        d.polygon([(x+11,y+1),(x+20,y+5),(x+18,y+15),(x+11,y+21),(x+4,y+15),(x+2,y+5)],outline=NAVY,fill=None)
        rule(x+7,y+11,x+10,y+14,RED,2); rule(x+10,y+14,x+16,y+7,RED,2)
    elif kind=='iran':
        d.polygon([(x+2,y+7),(x+11,y+2),(x+20,y+7),(x+18,y+17),(x+11,y+21),(x+4,y+17)],fill=RED)
        rule(x+8,y+7,x+8,y+15,PAPER,1); rule(x+14,y+7,x+14,y+15,PAPER,1)
    elif kind=='justice':
        rule(x+11,y+3,x+11,y+19,NAVY,2); rule(x+4,y+7,x+18,y+7,NAVY,2); rule(x+5,y+7,x+2,y+14,RED,1); rule(x+5,y+7,x+8,y+14,RED,1); rule(x+15,y+7,x+12,y+14,RED,1); rule(x+15,y+7,x+18,y+14,RED,1); rule(x+5,y+18,x+17,y+18,NAVY,2)
    elif kind=='markets':
        d.rectangle((x+3,y+12,x+7,y+19),fill=RED); d.rectangle((x+9,y+7,x+13,y+19),fill=NAVY); d.rectangle((x+15,y+3,x+19,y+19),fill=RED)
    elif kind=='quake':
        rule(x+3,y+5,x+8,y+10,NAVY,2); rule(x+8,y+10,x+12,y+5,RED,2); rule(x+12,y+5,x+17,y+12,NAVY,2); rule(x+17,y+12,x+20,y+9,RED,2); rule(x+4,y+18,x+19,y+18,NAVY,2)
    elif kind=='ship':
        d.polygon([(x+2,y+12),(x+20,y+12),(x+16,y+18),(x+6,y+18)],fill=NAVY); rule(x+10,y+4,x+10,y+12,RED,2); rule(x+6,y+8,x+15,y+8,RED,1)
    else:
        d.ellipse((x+3,y+3,x+19,y+19),outline=NAVY,width=2); rule(x+11,y+3,x+11,y+19,RED,1); rule(x+3,y+11,x+19,y+11,RED,1)

col_w, gutter = 232, 12
row_h = 145
for idx, (kicker, head, body, kind) in enumerate(stories):
    col, row = idx % 4, idx // 4
    x = 30 + col*(col_w+gutter)
    y = 358 + row*row_h
    if col > 0:
        rule(x-7, y+3, x-7, y+row_h-7, RULE, 1)
    rule(x, y+row_h-2, x+col_w, y+row_h-2, RULE, 1)
    text(x, y+1, kicker, font(SANS_B, 10), RED)
    icon(x+col_w-23, y-1, kind)
    hlines = wrap(head, font(SERIF, 16), col_w)
    if len(hlines) > 2:
        raise ValueError(f'Grid headline too long: {head}: {hlines}')
    for j, line in enumerate(hlines):
        text(x, y+21+j*18, line, font(SERIF, 16), NAVY)
    body_y = y+21+len(hlines)*18
    paragraph(x, body_y, body, font(SANS, 12), col_w, INK, 0, 7)

# Full-width legal/technology story with the cited study figures.
full_y = 652
rule(30, full_y, 994, full_y, INK, 2)
text(30, full_y+9, 'TECHNOLOGY  /  COURTS', font(SANS_B, 11), RED)
paragraph(30, full_y+29, 'STATES SUE SPACEX OVER GROK ABUSE IMAGES', font(SERIF, 19), 405, NAVY, 1, 2)
full_body = ('Oregon and Virginia sued SpaceX Super Intelligence on Monday 23 Nov, alleging Grok generated sexual images of children—the first state suits of their kind. A CCDH study cited by the states estimated about 3 million sexualised images on X from 29 Dec 2025 to 8 Jan 2026, with about 23,000 appearing to depict children.')
paragraph(458, full_y+12, full_body, font(SANS, 12), 526, INK, 3, 5)
rule(30, full_y+89, 994, full_y+89, INK, 2)

# Also Today: eight individually numbered one-line briefs.
text(30, full_y+97, 'ALSO TODAY', font(SERIF, 18), NAVY)
text(173, full_y+102, 'EIGHT DEVELOPMENTS FROM AROUND THE WORLD', font(SANS_B, 10), RED)
briefs = [
 'Measles claims a ninth life in Pennsylvania: 1,638 cases across 46 counties; unvaccinated Centre County victim.',
 'Car bomb explodes in Villavicencio, Colombia; buildings destroyed, with no confirmed victims.',
 'Tripoli demands explanations from Kyiv after the attack on Russian ships off Libya.',
 'COP31 is called climate diplomacy’s “darkest moment” after the talks collapse in Antalya.',
 'Guterres calls for a multilateral framework on AI risk within a year.',
 'Huawei is convicted in a sprawling US criminal trial over its Iran business.',
 'WHO chief Tedros calls for the immediate lifting of the US fuel blockade on Cuba.',
 'China opens Tiangong to its first foreign astronaut, Pakistani Zeeshan Ali, on Shenzhou-24.',
]
for i, b in enumerate(briefs):
    yy = full_y+123 + i*21
    text(31, yy, f'{i+1:02d}', font(SANS_B, 10), RED)
    paragraph(61, yy-1, b, font(SANS, 12), 925, INK, 1, 1)
    if i < 7:
        rule(61, yy+17, 994, yy+17, '#D8D0C4', 1)

rule(30, 953, 994, 953, INK, 2)
text(30, 963, 'BBC  ·  AP  ·  REUTERS  ·  FRANCE 24', font(SANS_B, 11), NAVY)
text(707, 963, 'SOURCES  /  24 NOVEMBER 2026', font(SANS_B, 10), MUTED)

im.save(Path(__file__).with_name('entry.png'), format='PNG', optimize=True)
