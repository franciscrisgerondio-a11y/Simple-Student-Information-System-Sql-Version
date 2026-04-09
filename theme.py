BG_BASE     = "#020B14"
BG_DEEP     = "#041525"
BG_SIDEBAR  = "#071828"
BG_CARD_BG  = "#0A1F30"

CYAN_400    = "#22D3EE"
CYAN_500    = "#06B6D4"
TEAL_600    = "#0D9488"
TEAL_700    = "#1D9E75"

TEXT_BRIGHT = "#F0FDFA"
TEXT_PRIMARY= "#E2F8FC"
TEXT_BODY   = "#CBD5E1"
TEXT_MUTED  = "#4B6175"
TEXT_DIM    = "#2E4A5C"
TEXT_MONO   = "#22D3EE"

DANGER      = "#EF4444"
WARNING     = "#F59E0B"
SUCCESS     = "#10B981"
PINK        = "#EC4899"
BLUE        = "#60A5FA"
SLATE       = "#94A3B8"


def qss(dark: bool = True) -> str:
    return _DARK if dark else _LIGHT


_DARK = f"""
* {{
    font-family: "Segoe UI", "SF Pro Text", "Helvetica Neue", Arial, sans-serif;
    font-size: 13px;
    color: {TEXT_BODY};
    outline: none;
    border: none;
    box-sizing: border-box;
}}
QMainWindow, QWidget {{ background-color: transparent; }}
QDialog {{ background-color: {BG_DEEP}; }}

#sidebar {{
    background-color: transparent;
    min-width: 220px; max-width: 220px;
}}
#sidebarBrand {{
    background-color: rgba(6,182,212,0.04);
    border-bottom: 1px solid rgba(34,211,238,0.15);
    min-height: 74px; max-height: 74px;
}}
#brandTitle {{
    color: {TEXT_BRIGHT};
    font-family: "Fira Code","Consolas","Courier New",monospace;
    font-size: 15px; font-weight: 700; letter-spacing: -0.5px;
    background: transparent;
}}
#brandSub {{
    color: {TEXT_MUTED};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 9px; font-weight: 500; letter-spacing: 2px;
    background: transparent;
}}
#navSection {{
    color: {TEXT_MUTED};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 9px; font-weight: 600; letter-spacing: 2.5px;
    padding: 16px 20px 6px 20px; background: transparent;
}}
#navBtn {{
    background-color: transparent;
    color: #64748B; border: none; border-radius: 8px;
    padding: 10px 14px; font-size: 13px; font-weight: 400;
    text-align: left; margin: 1px 8px;
}}
#navBtn:hover {{
    background-color: rgba(6,182,212,0.06); color: {TEXT_BODY};
}}
#navBtn[active="true"] {{
    background-color: rgba(255,255,255,0.06);
    color: {CYAN_400}; font-weight: 600;
    border: 1px solid rgba(34,211,238,0.30);
}}
#sidebarFooter {{
    background-color: transparent;
    border-top: 1px solid rgba(34,211,238,0.10);
    min-height: 56px; max-height: 56px; padding: 0 12px;
}}
#themeToggle {{
    background-color: rgba(30,58,74,0.8);
    color: #64748B; border: 1px solid rgba(34,211,238,0.20);
    border-radius: 8px; padding: 7px 12px;
    font-size: 12px; font-weight: 400; min-width: 150px;
}}
#themeToggle:hover {{
    background-color: rgba(34,211,238,0.08); color: {TEXT_BODY};
    border-color: rgba(34,211,238,0.35);
}}

#topBar {{
    background-color: transparent;
    border-bottom: 1px solid rgba(34,211,238,0.08);
    min-height: 72px; max-height: 72px; padding: 0 28px;
}}
#pageTitle {{
    color: {TEXT_BRIGHT};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 27px; font-weight: 700; letter-spacing: -0.5px;
    background: transparent;
}}
#pageSubtitle {{
    color: {TEXT_MUTED}; font-size: 13px; background: transparent;
}}

#statsStrip {{
    background-color: transparent;
    border-bottom: 1px solid rgba(34,211,238,0.08);
    min-height: 124px; max-height: 124px; padding: 0 28px;
}}
#statValue {{
    color: {TEXT_BRIGHT};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 28px; font-weight: 700; background: transparent;
}}
#statValueWarn {{
    color: {WARNING};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 28px; font-weight: 700; background: transparent;
}}
#statLabel {{
    color: {TEXT_MUTED}; font-size: 11px; font-weight: 500;
    letter-spacing: 0.5px; background: transparent;
}}
#statIconBox {{
    background-color: rgba(34,211,238,0.12);
    border: 1px solid rgba(34,211,238,0.25);
    border-radius: 7px;
}}
#statIconBoxWarn {{
    background-color: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.30);
    border-radius: 7px;
}}
#statIcon {{ color: {CYAN_400}; font-size: 15px; background: transparent; }}
#statIconWarn {{ color: {WARNING}; font-size: 15px; background: transparent; }}

#toolbar {{
    background-color: transparent;
    border-bottom: 1px solid rgba(34,211,238,0.08);
    min-height: 64px; max-height: 64px; padding: 0 28px;
}}
#searchBox {{
    background-color: rgba(255,255,255,0.06);
    border: 1px solid rgba(34,211,238,0.20);
    border-radius: 10px; padding: 10px 16px;
    font-size: 13px; color: {TEXT_BODY};
    min-width: 340px;
}}
#searchBox:focus {{
    border-color: rgba(34,211,238,0.50);
    background-color: rgba(255,255,255,0.08);
}}
#filterCombo {{
    background-color: rgba(255,255,255,0.06);
    border: 1px solid rgba(34,211,238,0.20);
    border-radius: 10px; padding: 10px 14px;
    font-size: 13px; color: #94A3B8; min-width: 120px;
}}
#filterCombo:focus {{ border-color: rgba(34,211,238,0.45); }}
#filterCombo::drop-down {{ border: none; width: 24px; }}
#filterCombo QAbstractItemView {{
    background-color: {BG_CARD_BG};
    border: 1px solid rgba(34,211,238,0.20); border-radius: 8px;
    selection-background-color: rgba(34,211,238,0.15);
    selection-color: {CYAN_400}; padding: 4px; outline: none;
}}

QPushButton {{
    border: none; border-radius: 8px; padding: 8px 18px;
    font-weight: 600; font-size: 13px;
    background-color: rgba(34,211,238,0.12);
    color: {CYAN_400};
}}
QPushButton:hover {{ background-color: rgba(34,211,238,0.20); }}
QPushButton:disabled {{ color: {TEXT_DIM}; background-color: transparent; }}

#btnAdd {{
    background-color: {CYAN_500}; color: white;
    border-radius: 10px; padding: 10px 22px;
    font-size: 13px; font-weight: 600; min-height: 42px;
}}
#btnAdd:hover {{ background-color: {CYAN_400}; }}

#btnEdit {{
    background-color: rgba(34,211,238,0.12);
    color: {CYAN_400};
    border: 1px solid rgba(34,211,238,0.30);
    border-radius: 6px; font-size: 12px; font-weight: 600;
}}
#btnEdit:hover {{
    background-color: rgba(34,211,238,0.20);
    border-color: rgba(34,211,238,0.55);
}}
#btnDelete {{
    background-color: rgba(239,68,68,0.10);
    color: {DANGER};
    border: 1px solid rgba(239,68,68,0.30);
    border-radius: 6px; font-size: 12px; font-weight: 600;
}}
#btnDelete:hover {{
    background-color: rgba(239,68,68,0.22);
    border-color: rgba(239,68,68,0.55);
}}
#btnNav {{
    background-color: rgba(255,255,255,0.04);
    color: {TEXT_MUTED};
    border: 1px solid rgba(34,211,238,0.20);
    border-radius: 7px; padding: 5px 10px;
    font-family: "Fira Code","Consolas",monospace;
    font-size: 12px; font-weight: 600;
    min-width: 32px; min-height: 32px;
}}
#btnNav:hover {{
    background-color: rgba(34,211,238,0.08); color: {CYAN_400};
    border-color: rgba(34,211,238,0.35);
}}
#btnNav:disabled {{
    color: {TEXT_DIM}; border-color: rgba(34,211,238,0.08);
    background-color: transparent;
}}
#btnNavActive {{
    background-color: rgba(34,211,238,0.15); color: {CYAN_400};
    border: 1px solid rgba(34,211,238,0.45);
    border-radius: 7px; font-family: "Fira Code","Consolas",monospace;
    font-size: 12px; font-weight: 700;
    min-width: 32px; min-height: 32px;
}}
#btnSave {{
    background-color: {CYAN_500}; color: white;
    border-radius: 10px; padding: 10px 28px;
    font-weight: 700; font-size: 13px; min-width: 110px;
}}
#btnSave:hover {{ background-color: {CYAN_400}; }}
#btnCancel {{
    background-color: transparent; color: {TEXT_MUTED};
    border: 1px solid rgba(34,211,238,0.20);
    border-radius: 10px; padding: 10px 24px;
    font-weight: 500; font-size: 13px; min-width: 90px;
}}
#btnCancel:hover {{
    background-color: rgba(34,211,238,0.06); color: {TEXT_BODY};
    border-color: rgba(34,211,238,0.35);
}}

QTableWidget {{
    background-color: transparent;
    alternate-background-color: rgba(6,182,212,0.025);
    gridline-color: rgba(34,211,238,0.07);
    border: none; selection-background-color: rgba(34,211,238,0.08);
    selection-color: {TEXT_BRIGHT}; outline: none;
}}
QTableWidget::item {{
    padding: 0px 14px; border: none;
    border-bottom: 1px solid rgba(34,211,238,0.07);
    color: {TEXT_BODY}; background-color: transparent;
}}
QTableWidget::item:selected {{
    background-color: rgba(34,211,238,0.08); color: {TEXT_BRIGHT};
}}
QTableWidget::item:hover {{
    background-color: rgba(34,211,238,0.04);
}}
QHeaderView {{ background-color: transparent; }}
QHeaderView::section {{
    background-color: rgba(6,182,212,0.05);
    color: {TEXT_MUTED};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 10px; font-weight: 600; letter-spacing: 1.5px;
    border: none; border-bottom: 1px solid rgba(34,211,238,0.12);
    border-right: 1px solid rgba(34,211,238,0.06);
    padding: 0px 14px; min-height: 44px;
}}
QHeaderView::section:hover {{
    background-color: rgba(34,211,238,0.07); color: {CYAN_400};
}}
QHeaderView::section:last-child {{ border-right: none; }}

#pillCourse {{
    background-color: rgba(34,211,238,0.12);
    color: {CYAN_400};
    border: 1px solid rgba(34,211,238,0.30);
    border-radius: 11px;
    font-family: "Fira Code","Consolas",monospace;
    font-size: 11px; font-weight: 600;
    padding: 1px 8px; min-height: 22px;
}}
#pillYear1 {{
    background-color: rgba(245,158,11,0.12); color: {WARNING};
    border: 1px solid rgba(245,158,11,0.30); border-radius: 11px;
    font-size: 11px; font-weight: 600; padding: 1px 8px; min-height: 22px;
}}
#pillYear2 {{
    background-color: rgba(16,185,129,0.12); color: {SUCCESS};
    border: 1px solid rgba(16,185,129,0.30); border-radius: 11px;
    font-size: 11px; font-weight: 600; padding: 1px 8px; min-height: 22px;
}}
#pillYear3 {{
    background-color: rgba(16,185,129,0.12); color: {SUCCESS};
    border: 1px solid rgba(16,185,129,0.30); border-radius: 11px;
    font-size: 11px; font-weight: 600; padding: 1px 8px; min-height: 22px;
}}
#pillYear4 {{
    background-color: rgba(16,185,129,0.12); color: {SUCCESS};
    border: 1px solid rgba(16,185,129,0.30); border-radius: 11px;
    font-size: 11px; font-weight: 600; padding: 1px 8px; min-height: 22px;
}}
#pillMale {{
    background-color: rgba(96,165,250,0.12); color: {BLUE};
    border: 1px solid rgba(96,165,250,0.30); border-radius: 11px;
    font-size: 11px; padding: 1px 8px; min-height: 22px;
}}
#pillFemale {{
    background-color: rgba(236,72,153,0.12); color: {PINK};
    border: 1px solid rgba(236,72,153,0.30); border-radius: 11px;
    font-size: 11px; padding: 1px 8px; min-height: 22px;
}}
#pillOther {{
    background-color: rgba(71,85,105,0.30); color: {SLATE};
    border: 1px solid rgba(71,85,105,0.40); border-radius: 11px;
    font-size: 11px; padding: 1px 8px; min-height: 22px;
}}
#pillNull {{
    background-color: rgba(239,68,68,0.12); color: {DANGER};
    border: 1px solid rgba(239,68,68,0.30); border-radius: 11px;
    font-family: "Fira Code","Consolas",monospace;
    font-size: 11px; font-weight: 700; padding: 1px 8px; min-height: 22px;
}}

QScrollBar:vertical {{
    background: transparent; width: 5px; margin: 4px;
}}
QScrollBar::handle:vertical {{
    background: rgba(34,211,238,0.20); border-radius: 3px; min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{ background: rgba(34,211,238,0.40); }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ height: 0; }}

#paginationBar {{
    background-color: transparent;
    border-top: 1px solid rgba(34,211,238,0.08);
    min-height: 54px; max-height: 54px; padding: 0 28px;
}}
#pageInfo {{
    color: {TEXT_MUTED};
    font-family: "Fira Code","Consolas",monospace;
    font-size: 12px; background: transparent;
}}
#recordInfo {{
    color: {TEXT_MUTED}; font-size: 12px; font-weight: 400;
    background: transparent;
}}

#emptyIcon  {{ font-size: 56px; background: transparent; }}
#emptyTitle {{ font-size: 18px; font-weight: 700; color: {TEXT_BRIGHT}; background: transparent; }}
#emptySub   {{ font-size: 13px; color: {TEXT_MUTED}; background: transparent; }}

QDialog {{ background-color: {BG_DEEP}; }}
#dialogHeader {{
    background-color: rgba(6,182,212,0.06);
    border-bottom: 1px solid rgba(34,211,238,0.18);
    min-height: 64px; max-height: 64px; padding: 0 24px;
}}
#dialogTitle {{
    font-family: "Fira Code","Consolas",monospace;
    font-size: 17px; font-weight: 700; color: {TEXT_BRIGHT};
    background: transparent; letter-spacing: -0.3px;
}}
#dialogSubtitle {{
    font-size: 11px; color: {TEXT_MUTED}; background: transparent;
}}
#formLabel {{
    font-size: 12px; font-weight: 600; color: {TEXT_MUTED};
    background: transparent; letter-spacing: 0.3px;
}}
QLineEdit, QComboBox {{
    background-color: rgba(255,255,255,0.04);
    border: 1px solid rgba(34,211,238,0.20);
    border-radius: 10px; padding: 10px 14px;
    font-size: 13px; color: {TEXT_BODY}; min-height: 22px;
    selection-background-color: rgba(34,211,238,0.20);
    selection-color: {CYAN_400};
}}
QLineEdit:focus, QComboBox:focus {{
    border-color: rgba(34,211,238,0.55);
    background-color: rgba(255,255,255,0.06);
}}
QLineEdit:disabled {{
    background-color: rgba(255,255,255,0.02);
    color: {TEXT_MUTED}; border-color: rgba(34,211,238,0.10);
}}
QComboBox::drop-down {{ border: none; width: 28px; }}
QComboBox QAbstractItemView {{
    background-color: {BG_CARD_BG};
    border: 1px solid rgba(34,211,238,0.20); border-radius: 8px;
    selection-background-color: rgba(34,211,238,0.15);
    selection-color: {CYAN_400}; padding: 4px; outline: none;
}}

QMessageBox {{ background-color: {BG_DEEP}; }}
QMessageBox QLabel {{ color: {TEXT_BODY}; font-size: 13px; min-width: 320px; }}
QMessageBox QPushButton {{ min-width: 86px; padding: 8px 20px; border-radius: 8px; }}

#divider  {{ background-color: rgba(34,211,238,0.08); max-height:1px; min-height:1px; border:none; }}
#dividerV {{ background-color: rgba(34,211,238,0.10); max-width:1px; min-width:1px; border:none; }}
"""

_LIGHT = """
* {
    font-family: "Inter","Segoe UI","Helvetica Neue",Arial,sans-serif;
    font-size: 13px;
    color: #334155;
    outline: none;
    border: none;
    box-sizing: border-box;
}

QMainWindow, QWidget { background-color: #EDF9FC; }
QDialog { background-color: #ffffff; }

#sidebar {
    background-color: transparent;
    min-width: 220px; max-width: 220px;
}
#sidebarBrand {
    background-color: rgba(6,182,212,0.05);
    border-bottom: 1px solid rgba(6,182,212,0.15);
    min-height: 74px; max-height: 74px;
}
#brandTitle {
    color: #0F172A;
    font-size: 15px; font-weight: 700; letter-spacing: -0.4px;
    background: transparent;
}
#brandSub {
    color: #94A3B8;
    font-size: 9px; font-weight: 600; letter-spacing: 2.2px;
    background: transparent;
}
#navSection {
    color: #94A3B8;
    font-size: 9px; font-weight: 700; letter-spacing: 2.5px;
    padding: 16px 20px 6px 20px;
    background: transparent;
}
#sidebarFooter {
    background-color: transparent;
    border-top: 1px solid rgba(6,182,212,0.12);
    min-height: 56px; max-height: 56px;
    padding: 0 12px;
}
#themeToggle {
    background-color: rgba(255,255,255,0.75);
    color: #475569;
    border: 1px solid rgba(14,165,233,0.20);
    border-radius: 10px;
    padding: 7px 12px;
    font-size: 13px;
    font-weight: 500;
    min-width: 150px;
}
#themeToggle:hover {
    background-color: rgba(224,242,254,0.90);
    color: #0369A1;
    border-color: rgba(14,165,233,0.40);
}

#topBar {
    background-color: transparent;
    border-bottom: 1px solid rgba(14,165,233,0.12);
    min-height: 72px; max-height: 72px;
    padding: 0 28px;
}
#pageTitle {
    color: #0F172A;
    font-size: 27px; font-weight: 700; letter-spacing: -0.5px;
    background: transparent;
}
#pageSubtitle {
    color: #64748B; font-size: 13px;
    background: transparent;
}

#statsStrip {
    background-color: transparent;
    border-bottom: 1px solid rgba(14,165,233,0.10);
    min-height: 124px; max-height: 124px;
    padding: 0 28px;
}
#statValue {
    color: #0F172A;
    font-size: 28px; font-weight: 700; letter-spacing: -1px;
    background: transparent;
}
#statValueWarn {
    color: #92400E;
    font-size: 28px; font-weight: 700; letter-spacing: -1px;
    background: transparent;
}
#statLabel {
    color: #94A3B8;
    font-size: 11px; font-weight: 600; letter-spacing: 0.8px;
    background: transparent;
}
#statIconBox {
    background-color: rgba(14,165,233,0.10);
    border: 1px solid rgba(14,165,233,0.25);
    border-radius: 8px;
}
#statIconBoxWarn {
    background-color: rgba(245,158,11,0.12);
    border: 1px solid rgba(245,158,11,0.35);
    border-radius: 8px;
}

#toolbar {
    background-color: transparent;
    border-bottom: 1px solid rgba(14,165,233,0.10);
    min-height: 64px; max-height: 64px;
    padding: 0 28px;
}
#searchBox {
    background-color: rgba(255,255,255,0.72);
    border: 1px solid rgba(14,165,233,0.22);
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 13.5px;
    color: #334155;
    min-width: 340px;
}
#searchBox:focus {
    border-color: rgba(14,165,233,0.55);
    background-color: rgba(255,255,255,0.92);
}
#searchBox::placeholder { color: #94A3B8; }

#filterCombo {
    background-color: rgba(255,255,255,0.72);
    border: 1px solid rgba(14,165,233,0.22);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 13.5px;
    color: #64748B;
    min-width: 120px;
}
#filterCombo:focus { border-color: rgba(14,165,233,0.50); }
#filterCombo::drop-down { border: none; width: 24px; }
#filterCombo QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid rgba(14,165,233,0.25);
    border-radius: 8px;
    selection-background-color: #E0F2FE;
    selection-color: #0369A1;
    padding: 4px;
    outline: none;
}

QPushButton {
    border: none; border-radius: 8px; padding: 8px 18px;
    font-weight: 600; font-size: 13px;
    background-color: #0EA5E9; color: white;
}
QPushButton:hover { background-color: #0284C7; }
QPushButton:disabled { background-color: #E2E8F0; color: #94A3B8; }

#btnAdd {
    background-color: #0EA5E9;
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    font-size: 14px; font-weight: 600;
    min-height: 44px;
}
#btnAdd:hover { background-color: #0284C7; }

#btnEdit {
    background-color: #E0F2FE;
    color: #0369A1;
    border: 1px solid #7DD3FC;
    border-radius: 7px;
    font-size: 12px; font-weight: 600;
}
#btnEdit:hover {
    background-color: #BAE6FD;
    border-color: #38BDF8;
    color: #1D4ED8;
}
#btnDelete {
    background-color: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
    border-radius: 7px;
    font-size: 12px; font-weight: 600;
}
#btnDelete:hover {
    background-color: #FEE2E2;
    border-color: #FCA5A5;
    color: #B91C1C;
}
#btnNav {
    background-color: rgba(255,255,255,0.72);
    color: #64748B;
    border: 1px solid rgba(14,165,233,0.20);
    border-radius: 8px;
    padding: 5px 10px;
    font-size: 12px; font-weight: 600;
    min-width: 32px; min-height: 34px;
}
#btnNav:hover {
    background-color: #E0F2FE;
    color: #0369A1;
    border-color: #7DD3FC;
}
#btnNav:disabled {
    color: #CBD5E1;
    border-color: rgba(14,165,233,0.10);
    background-color: transparent;
}
#btnNavActive {
    background-color: #0EA5E9;
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 12px; font-weight: 700;
    min-width: 32px; min-height: 34px;
}

#btnSave {
    background-color: #0EA5E9; color: white;
    border-radius: 10px; padding: 10px 28px;
    font-weight: 700; font-size: 13px; min-width: 110px;
}
#btnSave:hover { background-color: #0284C7; }
#btnCancel {
    background-color: transparent; color: #64748B;
    border: 1px solid #CBD5E1;
    border-radius: 10px; padding: 10px 24px;
    font-weight: 500; font-size: 13px; min-width: 90px;
}
#btnCancel:hover {
    background-color: #F0F9FF;
    color: #0369A1;
    border-color: #7DD3FC;
}

QTableWidget {
    background-color: rgba(255,255,255,0.78);
    alternate-background-color: rgba(14,165,233,0.025);
    gridline-color: rgba(14,165,233,0.07);
    border: none;
    selection-background-color: rgba(14,165,233,0.08);
    selection-color: #0F172A;
    outline: none;
}
QTableWidget::item {
    padding: 0px 14px;
    border: none;
    border-bottom: 1px solid rgba(14,165,233,0.07);
    color: #334155;
    background-color: transparent;
}
QTableWidget::item:selected {
    background-color: rgba(14,165,233,0.08);
    color: #0F172A;
}
QTableWidget::item:hover {
    background-color: rgba(14,165,233,0.06);
}
QHeaderView { background-color: transparent; }
QHeaderView::section {
    background-color: rgba(14,165,233,0.05);
    color: #94A3B8;
    font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
    border: none;
    border-bottom: 2px solid rgba(14,165,233,0.18);
    border-right: 1px solid rgba(14,165,233,0.08);
    padding: 0px 14px;
    min-height: 46px;
}
QHeaderView::section:hover {
    background-color: rgba(14,165,233,0.08);
    color: #0369A1;
}
QHeaderView::section:last-child { border-right: none; }

#pillCourse {
    background-color: #E0F2FE;
    color: #0369A1;
    border: 1px solid #BAE6FD;
    border-radius: 11px;
    font-size: 11px; font-weight: 600;
    padding: 1px 8px; min-height: 22px;
}
#pillYear1 {
    background-color: #FFFBEB;
    color: #92400E;
    border: 1px solid #FDE68A;
    border-radius: 11px;
    font-size: 11px; font-weight: 600;
    padding: 1px 8px; min-height: 22px;
}
#pillYear2 {
    background-color: #ECFDF5;
    color: #065F46;
    border: 1px solid #6EE7B7;
    border-radius: 11px;
    font-size: 11px; font-weight: 600;
    padding: 1px 8px; min-height: 22px;
}
#pillYear3 {
    background-color: #ECFDF5;
    color: #065F46;
    border: 1px solid #6EE7B7;
    border-radius: 11px;
    font-size: 11px; font-weight: 600;
    padding: 1px 8px; min-height: 22px;
}
#pillYear4 {
    background-color: #D1FAE5;
    color: #065F46;
    border: 1px solid #6EE7B7;
    border-radius: 11px;
    font-size: 11px; font-weight: 600;
    padding: 1px 8px; min-height: 22px;
}
#pillMale {
    background-color: #EFF6FF;
    color: #1D4ED8;
    border: 1px solid #BFDBFE;
    border-radius: 11px;
    font-size: 11px;
    padding: 1px 8px; min-height: 22px;
}
#pillFemale {
    background-color: #FDF2F8;
    color: #9D174D;
    border: 1px solid #F9A8D4;
    border-radius: 11px;
    font-size: 11px;
    padding: 1px 8px; min-height: 22px;
}
#pillOther {
    background-color: #F1F5F9;
    color: #475569;
    border: 1px solid #CBD5E1;
    border-radius: 11px;
    font-size: 11px;
    padding: 1px 8px; min-height: 22px;
}
#pillNull {
    background-color: #FEF2F2;
    color: #DC2626;
    border: 1px solid #FECACA;
    border-radius: 11px;
    font-size: 11px; font-weight: 700;
    padding: 1px 8px; min-height: 22px;
}

QScrollBar:vertical { background: transparent; width: 5px; margin: 4px; }
QScrollBar::handle:vertical { background: #CBD5E1; border-radius: 3px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #94A3B8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal { height: 0; }

#paginationBar {
    background-color: rgba(255,255,255,0.55);
    border-top: 1px solid rgba(14,165,233,0.10);
    min-height: 54px; max-height: 54px;
    padding: 0 28px;
}
#pageInfo { color: #64748B; font-size: 12px; background: transparent; }
#recordInfo { color: #64748B; font-size: 12px; background: transparent; }

#emptyIcon { font-size: 56px; background: transparent; }
#emptyTitle { font-size: 18px; font-weight: 700; color: #0F172A; background: transparent; }
#emptySub { font-size: 13px; color: #64748B; background: transparent; }

QDialog { background-color: #ffffff; }
#dialogHeader {
    background-color: #0EA5E9;
    border-bottom: 1px solid #0284C7;
    min-height: 56px; max-height: 56px;
    padding: 0 24px;
}
#dialogTitle {
    font-size: 17px; font-weight: 700; color: #ffffff;
    background: transparent; letter-spacing: -0.3px;
}
#dialogSubtitle {
    font-size: 11px; color: rgba(255,255,255,0.65);
    background: transparent;
}
#dialogBody { background-color: #ffffff; }
#formLabel {
    font-size: 12px; font-weight: 600; color: #475569;
    background: transparent;
}
QLineEdit, QComboBox {
    background-color: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-radius: 10px; padding: 10px 14px;
    font-size: 13px; color: #0F172A; min-height: 22px;
}
QLineEdit:focus, QComboBox:focus {
    border-color: #38BDF8;
    background-color: #ffffff;
}
QLineEdit:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
    border-color: #E2E8F0;
}
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #CBD5E1; border-radius: 8px;
    selection-background-color: #E0F2FE;
    selection-color: #0369A1; padding: 4px;
}

QMessageBox { background-color: #ffffff; }
QMessageBox QLabel { color: #1E293B; font-size: 13px; min-width: 320px; }
QMessageBox QPushButton { min-width: 86px; padding: 8px 20px; border-radius: 8px; }

#divider { background-color: rgba(14,165,233,0.10); max-height:1px; min-height:1px; border:none; }
#dividerV { background-color: rgba(14,165,233,0.10); max-width:1px; min-width:1px; border:none; }
"""
#Finally Done