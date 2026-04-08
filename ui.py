import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTableWidget, QTableWidgetItem,
    QHeaderView, QAbstractItemView, QFrame, QMessageBox,
    QSizePolicy, QStackedWidget, QComboBox,
    QStyledItemDelegate, QStyleOptionViewItem,
)
from PyQt6.QtCore import Qt, QSize, QRectF, QRect, QPointF
from PyQt6.QtGui import (
    QColor, QFont, QPainter, QLinearGradient, QRadialGradient,
    QPainterPath, QPen, QBrush, QPixmap, QIcon,
)

import db
import theme as th
from dialogs import CollegeDialog, ProgramDialog, StudentDialog


ACTIONS_W = 182
PILL_W    = 100


def _stroke(p: QPainter, col: QColor, w: float = 1.5):
    p.setPen(QPen(col, w, Qt.PenStyle.SolidLine,
                  Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
    p.setBrush(Qt.BrushStyle.NoBrush)


def _fill(p: QPainter, col: QColor):
    p.setPen(Qt.PenStyle.NoPen)
    p.setBrush(QBrush(col))


def draw_icon_students(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _stroke(p, col, 1.4)
    p.drawEllipse(QRectF(s*0.46, s*0.08, s*0.22, s*0.22))
    path = QPainterPath()
    path.moveTo(s*0.33, s*0.88)
    path.cubicTo(s*0.33, s*0.62, s*0.36, s*0.52, s*0.57, s*0.52)
    path.cubicTo(s*0.78, s*0.52, s*0.81, s*0.62, s*0.81, s*0.88)
    p.drawPath(path)
    col2 = QColor(col); col2.setAlphaF(col.alphaF() * 0.55)
    _stroke(p, col2, 1.2)
    p.drawEllipse(QRectF(s*0.18, s*0.14, s*0.18, s*0.18))
    path2 = QPainterPath()
    path2.moveTo(s*0.06, s*0.86)
    path2.cubicTo(s*0.06, s*0.64, s*0.09, s*0.54, s*0.27, s*0.54)
    path2.cubicTo(s*0.42, s*0.54, s*0.48, s*0.62, s*0.48, s*0.80)
    p.drawPath(path2)
    p.restore()


def draw_icon_programs(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _stroke(p, col, 1.4)
    board = QPainterPath()
    board.moveTo(s*0.50, s*0.12)
    board.lineTo(s*0.88, s*0.32)
    board.lineTo(s*0.50, s*0.50)
    board.lineTo(s*0.12, s*0.32)
    board.closeSubpath()
    p.drawPath(board)
    path = QPainterPath()
    path.moveTo(s*0.28, s*0.40)
    path.lineTo(s*0.28, s*0.60)
    path.cubicTo(s*0.28, s*0.76, s*0.72, s*0.76, s*0.72, s*0.60)
    path.lineTo(s*0.72, s*0.40)
    p.drawPath(path)
    p.drawLine(QPointF(s*0.88, s*0.32), QPointF(s*0.88, s*0.58))
    _fill(p, col)
    p.drawEllipse(QRectF(s*0.83, s*0.56, s*0.10, s*0.10))
    p.restore()


def draw_icon_colleges(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _stroke(p, col, 1.4)
    roof = QPainterPath()
    roof.moveTo(s*0.10, s*0.38)
    roof.lineTo(s*0.50, s*0.10)
    roof.lineTo(s*0.90, s*0.38)
    roof.closeSubpath()
    p.drawPath(roof)
    p.drawRect(QRectF(s*0.08, s*0.82, s*0.84, s*0.08))
    p.drawRect(QRectF(s*0.06, s*0.88, s*0.88, s*0.06))
    for cx in (0.22, 0.50, 0.78):
        p.drawLine(QPointF(s*cx, s*0.38), QPointF(s*cx, s*0.82))
    p.drawRect(QRectF(s*0.10, s*0.36, s*0.80, s*0.06))
    p.restore()


def draw_icon_warning(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _stroke(p, col, 1.5)
    tri = QPainterPath()
    tri.moveTo(s*0.50, s*0.10)
    tri.lineTo(s*0.92, s*0.84)
    tri.lineTo(s*0.08, s*0.84)
    tri.closeSubpath()
    p.drawPath(tri)
    p.drawLine(QPointF(s*0.50, s*0.36), QPointF(s*0.50, s*0.62))
    _fill(p, col)
    p.drawEllipse(QRectF(s*0.44, s*0.68, s*0.12, s*0.12))
    p.restore()


def draw_icon_sun(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _stroke(p, col, 1.3)
    cx, cy, r = s*0.50, s*0.50, s*0.18
    p.drawEllipse(QRectF(cx-r, cy-r, r*2, r*2))
    for i in range(8):
        angle = math.radians(i * 45)
        inner = s * 0.28
        outer = s * 0.44
        p.drawLine(
            QPointF(cx + inner * math.cos(angle), cy + inner * math.sin(angle)),
            QPointF(cx + outer * math.cos(angle), cy + outer * math.sin(angle)),
        )
    p.restore()


def draw_icon_moon(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _fill(p, col)
    outer = QPainterPath()
    outer.addEllipse(QRectF(s*0.14, s*0.10, s*0.72, s*0.72))
    inner = QPainterPath()
    inner.addEllipse(QRectF(s*0.30, s*0.06, s*0.68, s*0.68))
    crescent = outer.subtracted(inner)
    p.drawPath(crescent)
    p.restore()


def draw_icon_logo(p: QPainter, x: float, y: float, s: float):
    p.save()
    p.translate(x, y)
    for i, (yoff, alpha) in enumerate(((0.60, 0.4), (0.42, 0.7), (0.24, 1.0))):
        c = QColor("#22D3EE" if i < 2 else "#22D3EE")
        c.setAlphaF(alpha)
        _stroke(p, c, 1.5)
        _fill(p, QColor(34, 211, 238, int(alpha * 80)))
        path = QPainterPath()
        path.moveTo(s*0.12, s*(yoff + 0.14))
        path.lineTo(s*0.50, s*yoff)
        path.lineTo(s*0.88, s*(yoff + 0.14))
        path.lineTo(s*0.88, s*(yoff + 0.28))
        path.lineTo(s*0.50, s*(yoff + 0.14))
        path.lineTo(s*0.12, s*(yoff + 0.28))
        path.closeSubpath()
        p.drawPath(path)
    p.restore()


def draw_icon_search(p: QPainter, x: float, y: float, s: float, col: QColor):
    p.save()
    p.translate(x, y)
    _stroke(p, col, 1.6)
    r = s * 0.28
    cx, cy = s*0.40, s*0.40
    p.drawEllipse(QRectF(cx-r, cy-r, r*2, r*2))
    p.drawLine(QPointF(cx + r*0.72, cy + r*0.72),
               QPointF(s*0.86, s*0.86))
    p.restore()


class IconWidget(QWidget):
    def __init__(self, icon_fn, size: int = 20, col: QColor = None, parent=None):
        super().__init__(parent)
        self._icon_fn = icon_fn
        self._size    = size
        self._col     = col or QColor("#22D3EE")
        self.setFixedSize(QSize(size, size))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_color(self, col: QColor):
        self._col = col; self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        self._icon_fn(p, 0, 0, self._size, self._col)


class LogoIconWidget(QWidget):
    def __init__(self, size: int = 20, parent=None):
        super().__init__(parent)
        self.setFixedSize(QSize(size, size))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        draw_icon_logo(p, 0, 0, self.width())


class GlowBackground(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def set_dark(self, d: bool):
        self._is_dark = d
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        if self._is_dark:
            bg = QLinearGradient(0, 0, w, h)
            bg.setColorAt(0, QColor("#020B14"))
            bg.setColorAt(1, QColor("#041525"))
            p.fillRect(0, 0, w, h, bg)

            for cx, cy, r, col, op in (
                (0.20, 0.18, 0.40, "#06B6D4", 0.18),
                (0.85, 0.75, 0.35, "#0D9488", 0.14),
                (0.55, 0.95, 0.30, "#22D3EE", 0.10),
                (0.20, 0.60, 0.40, "#06B6D4", 0.15),
                (0.80, 0.30, 0.35, "#0D9488", 0.12),
            ):
                g = QRadialGradient(w * cx, h * cy, w * r)
                c0 = QColor(col); c0.setAlphaF(op)
                c1 = QColor(col); c1.setAlphaF(0.0)
                g.setColorAt(0, c0); g.setColorAt(1, c1)
                p.fillRect(0, 0, w, h, g)
        else:
            bg = QLinearGradient(0, 0, w, h)
            bg.setColorAt(0.00, QColor("#E8F8FC"))
            bg.setColorAt(0.55, QColor("#F0FAF6"))
            bg.setColorAt(1.00, QColor("#EAF5F9"))
            p.fillRect(0, 0, w, h, bg)

            for cx, cy, r, col, op in (
                (0.15, 0.18, 0.38, "#BAE6FD", 0.55),
                (0.88, 0.72, 0.32, "#99F6E4", 0.45),
                (0.55, 0.95, 0.28, "#7DD3FC", 0.30),
                (0.12, 0.65, 0.36, "#A5F3FC", 0.40),
                (0.82, 0.28, 0.30, "#6EE7B7", 0.35),
            ):
                g = QRadialGradient(w * cx, h * cy, w * r)
                c0 = QColor(col); c0.setAlphaF(op)
                c1 = QColor(col); c1.setAlphaF(0.0)
                g.setColorAt(0, c0); g.setColorAt(1, c1)
                p.fillRect(0, 0, w, h, g)


class LightGlassCard(QWidget):
    def __init__(self, warn=False, radius=16, parent=None):
        super().__init__(parent)
        self._warn   = warn
        self._radius = radius
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r    = QRectF(0.5, 0.5, w - 1, h - 1)
        rad  = self._radius

        fill = QLinearGradient(0, 0, w, h)
        if self._warn:
            fill.setColorAt(0, QColor(255, 255, 255, 184))
            fill.setColorAt(1, QColor(255, 251, 235, 153))
        else:
            fill.setColorAt(0, QColor(255, 255, 255, 184))
            fill.setColorAt(1, QColor(224, 247, 250, 148))
        p.setBrush(QBrush(fill)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(r, rad, rad)

        shimmer = QLinearGradient(0, 0, w, h)
        if self._warn:
            shimmer.setColorAt(0, QColor(253, 230, 138, 46))
            shimmer.setColorAt(1, QColor(252, 211, 77,  20))
        else:
            shimmer.setColorAt(0, QColor(103, 232, 249, 25))
            shimmer.setColorAt(0.45, QColor(255, 255, 255, 46))
            shimmer.setColorAt(1, QColor(110, 231, 183, 20))
        p.setBrush(QBrush(shimmer))
        p.drawRoundedRect(r, rad, rad)

        top = QLinearGradient(0, 0, w, 0)
        if self._warn:
            top.setColorAt(0,    QColor(255, 255, 255, 0))
            top.setColorAt(0.35, QColor(255, 255, 255, 140))
            top.setColorAt(0.65, QColor(245, 158, 11,  64))
            top.setColorAt(1,    QColor(255, 255, 255, 0))
        else:
            top.setColorAt(0,    QColor(255, 255, 255, 0))
            top.setColorAt(0.35, QColor(255, 255, 255, 166))
            top.setColorAt(0.65, QColor(6,  182, 212,  51))
            top.setColorAt(1,    QColor(255, 255, 255, 0))
        p.setBrush(QBrush(top))
        p.drawRect(QRectF(0.5, 0.5, w - 1, 2))

        sheen = QLinearGradient(0, 0, w * 0.55, h * 0.55)
        sheen.setColorAt(0, QColor(255, 255, 255, 115))
        sheen.setColorAt(1, QColor(255, 255, 255, 0))
        p.setBrush(QBrush(sheen))
        p.drawRoundedRect(QRectF(0.5, 0.5, w * 0.5, h * 0.5), rad, rad)

        border_col = QColor(245, 158, 11, 72) if self._warn else QColor(14, 165, 233, 51)
        p.setPen(QPen(border_col, 0.9)); p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, rad, rad)


class GlassCard(QWidget):
    def __init__(self, warn=False, radius=14, parent=None):
        super().__init__(parent)
        self._warn   = warn
        self._radius = radius
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r   = QRectF(0.5, 0.5, self.width() - 1, self.height() - 1)
        rad = self._radius

        fill = QLinearGradient(0, 0, self.width(), self.height())
        fill.setColorAt(0, QColor(255, 255, 255, 15))
        fill.setColorAt(1, QColor(6, 182, 212, 8))
        p.setBrush(QBrush(fill)); p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(r, rad, rad)

        sh = QLinearGradient(0, 0, self.width(), self.height())
        if self._warn:
            sh.setColorAt(0, QColor(252, 211, 77, 25))
            sh.setColorAt(1, QColor(245, 158, 11, 13))
        else:
            sh.setColorAt(0, QColor(103, 232, 249, 30))
            sh.setColorAt(0.4, QColor(255, 255, 255, 10))
            sh.setColorAt(1, QColor(13, 148, 136, 20))
        p.setBrush(QBrush(sh))
        p.drawRoundedRect(r, rad, rad)

        al = QLinearGradient(0, 0, self.width(), 0)
        if self._warn:
            al.setColorAt(0, QColor(245, 158, 11, 0))
            al.setColorAt(0.5, QColor(245, 158, 11, 153))
            al.setColorAt(1, QColor(245, 158, 11, 0))
        else:
            al.setColorAt(0, QColor(34, 211, 238, 0))
            al.setColorAt(0.5, QColor(34, 211, 238, 153))
            al.setColorAt(1, QColor(34, 211, 238, 0))
        p.setBrush(QBrush(al))
        p.drawRect(QRectF(0.5, 0.5, self.width() - 1, 1))

        bc = QColor(245, 158, 11, 64) if self._warn else QColor(34, 211, 238, 46)
        p.setPen(QPen(bc, 0.8)); p.setBrush(Qt.BrushStyle.NoBrush)
        p.drawRoundedRect(r, rad, rad)


class RowDelegate(QStyledItemDelegate):
    def __init__(self, table, is_dark=True):
        super().__init__(table)
        self._table     = table
        self._hover_row = -1
        self._is_dark   = is_dark

    def set_hover(self, row: int):
        self._hover_row = row

    def set_dark(self, d: bool):
        self._is_dark = d

    def paint(self, painter, option, index):
        row = index.row()
        if row == self._hover_row:
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
            hover_bg = QColor(34, 211, 238, 10) if self._is_dark else QColor(14, 165, 233, 15)
            accent   = QColor(34, 211, 238, 178) if self._is_dark else QColor(14, 165, 233, 255)
            painter.fillRect(option.rect, hover_bg)
            if index.column() == 0:
                bar = QRect(option.rect.left(), option.rect.top(),
                            4, option.rect.height())
                painter.fillRect(bar, accent)
            painter.restore()
        super().paint(painter, option, index)


def _hline() -> QFrame:
    f = QFrame(); f.setObjectName("divider")
    f.setFrameShape(QFrame.Shape.HLine); f.setFixedHeight(1)
    f.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    return f


def _vline() -> QFrame:
    f = QFrame(); f.setObjectName("dividerV")
    f.setFrameShape(QFrame.Shape.VLine); f.setFixedWidth(1)
    f.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    return f


def _pill(text: str, obj: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName(obj)
    lbl.setFixedWidth(PILL_W)
    lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lbl.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    lbl.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    return lbl


def _year_pill(year: int) -> QLabel:
    names = {1: "pillYear1", 2: "pillYear2", 3: "pillYear3", 4: "pillYear4"}
    return _pill(f"Year {year}", names.get(year, "pillYear1"))


def _gender_pill(gender: str) -> QLabel:
    return _pill(gender, {"Male": "pillMale", "Female": "pillFemale"}.get(gender, "pillOther"))


class _RO(QTableWidgetItem):
    def __init__(self, text: str,
                 align=Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft):
        super().__init__(str(text))
        self.setFlags(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled)
        self.setTextAlignment(align)
        self.setBackground(QColor(0, 0, 0, 0))


class EmptyState(QWidget):
    def __init__(self, icon_fn, title, sub, btn_label, on_add):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter); lay.setSpacing(12)

        ico = IconWidget(icon_fn, size=56, col=QColor(34, 211, 238, 60))
        lay.addWidget(ico, alignment=Qt.AlignmentFlag.AlignCenter)

        t = QLabel(title); t.setObjectName("emptyTitle")
        t.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(t)

        s = QLabel(sub); s.setObjectName("emptySub")
        s.setAlignment(Qt.AlignmentFlag.AlignCenter); s.setWordWrap(True)
        lay.addWidget(s)

        lay.addSpacing(14)
        btn = QPushButton(f"Add {btn_label}"); btn.setObjectName("btnAdd")
        btn.setFixedWidth(200); btn.setFixedHeight(44)
        btn.clicked.connect(on_add)
        lay.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)


class TableView(QWidget):
    COLS:   list[str] = []
    ENTITY: str = ""
    ICON_FN = staticmethod(draw_icon_students)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._page     = 1
        self._per_page = 10
        self._total    = 0
        self._sort_col = self.COLS[0] if self.COLS else ""
        self._sort_asc = True
        self._search   = ""
        self._is_dark  = True
        self._filter_course = ""
        self._filter_year   = ""
        self._filter_gender = ""
        self._build()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)
        root.addWidget(self._mk_toolbar()); root.addWidget(_hline())

        self._view_stack = QStackedWidget()
        self._view_stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._tbl   = self._mk_table()
        self._empty = EmptyState(
            icon_fn   = self.ICON_FN,
            title     = f"No {self.ENTITY}s yet",
            sub       = f"Add your first {self.ENTITY.lower()} to get started.",
            btn_label = self.ENTITY,
            on_add    = self._on_add,
        )
        self._view_stack.addWidget(self._tbl)
        self._view_stack.addWidget(self._empty)
        root.addWidget(self._view_stack, 1)
        root.addWidget(_hline()); root.addWidget(self._mk_pagination())

    def _mk_toolbar(self) -> QWidget:
        bar = QWidget(); bar.setObjectName("toolbar")
        bar.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(28, 0, 28, 0); lay.setSpacing(10)

        self._search_box = QLineEdit()
        self._search_box.setObjectName("searchBox")
        self._search_box.setPlaceholderText(
            f"Search {self.ENTITY.lower()}s by name, ID, or course…")
        self._search_box.setFixedHeight(44)
        self._search_box.textChanged.connect(self._on_search)

        self._btn_add = QPushButton(f"  Add {self.ENTITY}")
        self._btn_add.setObjectName("btnAdd")
        self._btn_add.setFixedHeight(44)
        self._btn_add.clicked.connect(self._on_add)

        lay.addWidget(self._search_box)
        self._add_filters(lay)
        lay.addWidget(self._btn_add)
        return bar

    def _add_filters(self, lay: QHBoxLayout):
        pass

    def _mk_table(self) -> QTableWidget:
        n = len(self.COLS) + 1
        t = QTableWidget()
        t.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        t.setColumnCount(n)
        t.setHorizontalHeaderLabels(self.COLS + ["ACTIONS"])
        t.setAlternatingRowColors(False)
        t.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        t.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        t.verticalHeader().setVisible(False)
        t.horizontalHeader().setHighlightSections(False)
        t.setShowGrid(True)
        t.setSortingEnabled(False)
        t.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        t.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._delegate = RowDelegate(t, is_dark=self._is_dark)
        t.setItemDelegate(self._delegate)
        t.viewport().setMouseTracking(True)
        t.viewport().installEventFilter(self)

        hdr = t.horizontalHeader()
        hdr.setStretchLastSection(False)
        hdr.sectionClicked.connect(self._on_col_click)
        self._configure_cols(t, hdr)
        return t

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if not hasattr(self, "_tbl"): return False
        vp = self._tbl.viewport()
        if obj is vp and event.type() == QEvent.Type.MouseMove:
            idx = self._tbl.indexAt(event.pos())
            self._delegate.set_hover(idx.row() if idx.isValid() else -1)
            vp.update()
        elif obj is vp and event.type() == QEvent.Type.Leave:
            self._delegate.set_hover(-1); vp.update()
        return False

    def _configure_cols(self, t, hdr):
        for i in range(len(self.COLS)):
            hdr.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(len(self.COLS), QHeaderView.ResizeMode.Fixed)
        t.setColumnWidth(len(self.COLS), ACTIONS_W)

    def _mk_pagination(self) -> QWidget:
        bar = QWidget(); bar.setObjectName("paginationBar")
        bar.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay = QHBoxLayout(bar)
        lay.setContentsMargins(28, 0, 28, 0); lay.setSpacing(6)

        self._rec_lbl  = QLabel(); self._rec_lbl.setObjectName("recordInfo")
        self._page_lbl = QLabel(); self._page_lbl.setObjectName("pageInfo")
        self._page_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        def _nb(t, w=36):
            b = QPushButton(t); b.setObjectName("btnNav")
            b.setFixedSize(QSize(w, 34)); return b

        self._b1 = _nb("«"); self._bp = _nb("‹  Prev", 80)
        self._bn = _nb("Next  ›", 80); self._bz = _nb("»")

        self._b1.clicked.connect(lambda: self._go(1))
        self._bp.clicked.connect(lambda: self._go(self._page - 1))
        self._bn.clicked.connect(lambda: self._go(self._page + 1))
        self._bz.clicked.connect(lambda: self._go(self._total_pages()))

        lay.addWidget(self._rec_lbl); lay.addStretch()
        lay.addWidget(self._b1); lay.addWidget(self._bp)
        lay.addSpacing(8); lay.addWidget(self._page_lbl)
        lay.addSpacing(8); lay.addWidget(self._bn); lay.addWidget(self._bz)
        return bar

    def refresh(self):
        rows, self._total = self._fetch()
        self._tbl.setRowCount(0)
        self._view_stack.setCurrentIndex(
            1 if (self._total == 0 and not self._search) else 0)
        for i, rec in enumerate(rows):
            self._tbl.insertRow(i)
            self._tbl.setRowHeight(i, 52)
            self._fill_row(i, rec)
            self._inject_actions(i, rec)
        self._apply_highlight()
        self._sync_pagination()

    def _inject_actions(self, row: int, rec: dict):
        key  = self._pk(rec)
        cell = QWidget(); cell.setFixedWidth(ACTIONS_W); cell.setFixedHeight(52)
        cell.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay  = QHBoxLayout(cell)
        lay.setContentsMargins(12, 12, 12, 12); lay.setSpacing(8)

        edit = QPushButton("Edit"); edit.setObjectName("btnEdit")
        edit.setFixedWidth(62); edit.setFixedHeight(28)
        edit.setCursor(Qt.CursorShape.PointingHandCursor)
        edit.clicked.connect(lambda _, k=key: self._on_edit(k))

        delete = QPushButton("Delete"); delete.setObjectName("btnDelete")
        delete.setFixedWidth(74); delete.setFixedHeight(28)
        delete.setCursor(Qt.CursorShape.PointingHandCursor)
        delete.clicked.connect(lambda _, k=key: self._on_delete(k))

        lay.addWidget(edit); lay.addWidget(delete)
        self._tbl.setCellWidget(row, len(self.COLS), cell)

    def _set_pill(self, row: int, col: int, pill: QLabel):
        cell = QWidget()
        cell.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay  = QHBoxLayout(cell)
        lay.setContentsMargins(4, 8, 4, 8)
        lay.addStretch(); lay.addWidget(pill); lay.addStretch()
        self._tbl.setCellWidget(row, col, cell)

    def _on_search(self, text: str):
        self._search = text; self._page = 1; self.refresh()

    def _apply_highlight(self):
        kw = self._search.strip().lower()
        if not kw: return
        hl_bg = QColor(34, 211, 238, 60) if self._is_dark else QColor(254, 240, 138, 200)
        hl_fg = QColor(th.TEXT_BRIGHT    if self._is_dark else "#5a3a00")
        for r in range(self._tbl.rowCount()):
            for c in range(len(self.COLS)):
                item = self._tbl.item(r, c)
                if item and kw in item.text().lower():
                    item.setBackground(hl_bg); item.setForeground(hl_fg)

    def _on_col_click(self, idx: int):
        if idx >= len(self.COLS): return
        col = self.COLS[idx]
        self._sort_asc = not self._sort_asc if self._sort_col == col else True
        self._sort_col = col; self._page = 1
        self._redraw_headers(); self.refresh()

    def _redraw_headers(self):
        for i, col in enumerate(self.COLS):
            arrow = ("  ▲" if self._sort_asc else "  ▼") if col == self._sort_col else ""
            self._tbl.horizontalHeaderItem(i).setText(col + arrow)
        self._tbl.horizontalHeaderItem(len(self.COLS)).setText("ACTIONS")

    def _total_pages(self):
        return max(1, (self._total + self._per_page - 1) // self._per_page)

    def _go(self, p: int):
        self._page = max(1, min(p, self._total_pages())); self.refresh()

    def _sync_pagination(self):
        tp = self._total_pages()
        s  = (self._page - 1) * self._per_page + 1
        e  = min(self._page * self._per_page, self._total)
        self._page_lbl.setText(f"Page {self._page} / {tp}")
        self._rec_lbl.setText(
            f"Showing {s:,}–{e:,} of {self._total:,} records"
            if self._total else "No records found")
        self._b1.setEnabled(self._page > 1); self._bp.setEnabled(self._page > 1)
        self._bn.setEnabled(self._page < tp); self._bz.setEnabled(self._page < tp)

    def set_dark(self, d: bool):
        self._is_dark = d
        if hasattr(self, "_delegate"):
            self._delegate.set_dark(d)

    def _fetch(self): raise NotImplementedError
    def _fill_row(self, i, rec): raise NotImplementedError
    def _pk(self, rec): raise NotImplementedError
    def _on_add(self): raise NotImplementedError
    def _on_edit(self, key): raise NotImplementedError
    def _on_delete(self, key): raise NotImplementedError


class CollegeView(TableView):
    COLS     = ["CODE", "NAME"]
    ENTITY   = "College"
    ICON_FN  = staticmethod(draw_icon_colleges)

    def _configure_cols(self, t, hdr):
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        t.setColumnWidth(2, ACTIONS_W)

    def _fetch(self):
        return db.get_colleges(search=self._search, sort_col=self._sort_col,
                               sort_asc=self._sort_asc, page=self._page,
                               per_page=self._per_page)

    def _pk(self, rec): return rec["code"]

    def _fill_row(self, i, rec):
        ctr  = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        col_str = QColor(th.CYAN_400) if self._is_dark else QColor("#0EA5E9")
        code = _RO(rec["code"], ctr)
        code.setFont(QFont("Fira Code, Consolas, Courier New", 12))
        code.setForeground(col_str)
        self._tbl.setItem(i, 0, code)
        name_item = _RO(rec["name"])
        name_item.setForeground(QColor("#0F172A") if not self._is_dark else QColor(th.TEXT_PRIMARY))
        self._tbl.setItem(i, 1, name_item)

    def _on_add(self):
        if CollegeDialog(self.window()).exec():
            self.refresh(); self.window().refresh_stats()

    def _on_edit(self, code):
        rows, _ = db.get_colleges(search=code, page=1, per_page=5)
        r = next((x for x in rows if x["code"] == code), None)
        if not r: return
        if CollegeDialog(self.window(), edit_code=r["code"], edit_name=r["name"]).exec():
            self.refresh()

    def _on_delete(self, code):
        n   = len(db.get_programs_for_college(code))
        msg = (f"Delete college '{code}'?\n\nThis will also delete {n} program(s) "
               f"and set affected students' course to NULL.\n\nThis cannot be undone."
               ) if n else f"Delete college '{code}'?\n\nThis cannot be undone."
        if QMessageBox.question(self.window(), "Delete College", msg,
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            db.delete_college(code); self.refresh(); self.window().refresh_stats()


class ProgramView(TableView):
    COLS    = ["CODE", "NAME", "COLLEGE"]
    ENTITY  = "Program"
    ICON_FN = staticmethod(draw_icon_programs)

    def _configure_cols(self, t, hdr):
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        t.setColumnWidth(3, ACTIONS_W)

    def _fetch(self):
        return db.get_programs(search=self._search, sort_col=self._sort_col,
                               sort_asc=self._sort_asc, page=self._page,
                               per_page=self._per_page)

    def _pk(self, rec): return rec["code"]

    def _fill_row(self, i, rec):
        ctr    = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        col_str = QColor(th.CYAN_400) if self._is_dark else QColor("#0EA5E9")
        muted   = QColor(th.TEXT_MUTED) if self._is_dark else QColor("#64748B")
        code = _RO(rec["code"], ctr)
        code.setFont(QFont("Fira Code, Consolas, Courier New", 12))
        code.setForeground(col_str)
        self._tbl.setItem(i, 0, code)
        name_item = _RO(rec["name"])
        name_item.setForeground(QColor("#0F172A") if not self._is_dark else QColor(th.TEXT_PRIMARY))
        self._tbl.setItem(i, 1, name_item)
        col_i = _RO(rec.get("college") or "—", ctr)
        col_i.setForeground(muted)
        self._tbl.setItem(i, 2, col_i)

    def _on_add(self):
        if not db.get_all_colleges():
            QMessageBox.information(self.window(), "No Colleges",
                "Add at least one college before adding a program.")
            return
        if ProgramDialog(self.window()).exec():
            self.refresh(); self.window().refresh_stats()

    def _on_edit(self, code):
        rows, _ = db.get_programs(search=code, page=1, per_page=10)
        r = next((x for x in rows if x["code"] == code), None)
        if not r: return
        if ProgramDialog(self.window(), edit_code=r["code"],
                         edit_name=r["name"], edit_college=r["college"]).exec():
            self.refresh()

    def _on_delete(self, code):
        if QMessageBox.question(self.window(), "Delete Program",
                f"Delete program '{code}'?\nAffected students' course will be set to NULL.\n\nThis cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            db.delete_program(code); self.refresh(); self.window().refresh_stats()


class StudentView(TableView):
    COLS    = ["STUDENT ID", "FIRST NAME", "LAST NAME", "COURSE", "YEAR", "GENDER"]
    ENTITY  = "Student"
    ICON_FN = staticmethod(draw_icon_students)

    def _configure_cols(self, t, hdr):
        hdr.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        hdr.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hdr.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        for col in (3, 4, 5):
            hdr.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            t.setColumnWidth(col, PILL_W + 20)
        hdr.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        t.setColumnWidth(6, ACTIONS_W)

    def _add_filters(self, lay: QHBoxLayout):
        def _combo(ph, items, cb):
            c = QComboBox(); c.setObjectName("filterCombo")
            c.setFixedHeight(44); c.addItem(ph)
            for it in items: c.addItem(it)
            c.currentTextChanged.connect(cb); return c

        self._cmb_course = _combo("All Courses",
            [p["code"] for p in db.get_all_programs()],
            lambda t: self._set_filter("course", t))
        self._cmb_year   = _combo("All Years",
            ["Year 1", "Year 2", "Year 3", "Year 4"],
            lambda t: self._set_filter("year", t))
        self._cmb_gender = _combo("All Genders",
            ["Male", "Female", "Other"],
            lambda t: self._set_filter("gender", t))
        lay.addWidget(self._cmb_course)
        lay.addWidget(self._cmb_year)
        lay.addWidget(self._cmb_gender)

    def _set_filter(self, key, val):
        if key == "course":   self._filter_course = "" if val.startswith("All") else val
        elif key == "year":   self._filter_year   = "" if val.startswith("All") else val[-1]
        elif key == "gender": self._filter_gender = "" if val.startswith("All") else val
        self._page = 1; self.refresh()

    def _fetch(self):
        return db.get_students(
            search=self._search,
            sort_col=self._sort_col.replace("STUDENT ", ""),
            sort_asc=self._sort_asc, page=self._page, per_page=self._per_page,
            course_filter=self._filter_course, year_filter=self._filter_year,
            gender_filter=self._filter_gender,
        )

    def _pk(self, rec): return rec["id"]

    def _fill_row(self, i, rec):
        ctr     = Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignCenter
        id_col  = QColor(th.CYAN_400) if self._is_dark else QColor("#0EA5E9")
        txt_col = QColor(th.TEXT_PRIMARY) if self._is_dark else QColor("#1E293B")
        sub_col = QColor(th.TEXT_BODY)    if self._is_dark else QColor("#334155")

        id_item = _RO(rec["id"], ctr)
        id_item.setFont(QFont("Fira Code, Consolas, Courier New", 12))
        id_item.setForeground(id_col)
        self._tbl.setItem(i, 0, id_item)

        fn = _RO(rec["firstname"]); fn.setForeground(txt_col)
        self._tbl.setItem(i, 1, fn)
        ln = _RO(rec["lastname"]); ln.setForeground(sub_col)
        self._tbl.setItem(i, 2, ln)

        course = rec.get("course") or "NULL"
        self._set_pill(i, 3,
            _pill("NULL", "pillNull") if course == "NULL"
            else _pill(course, "pillCourse"))
        self._set_pill(i, 4, _year_pill(rec["year"]))
        self._set_pill(i, 5, _gender_pill(rec["gender"]))

    def _on_add(self):
        if StudentDialog(self.window()).exec():
            self.refresh(); self.window().refresh_stats()

    def _on_edit(self, sid):
        rows, _ = db.get_students(search=sid, page=1, per_page=10)
        r = next((x for x in rows if x["id"] == sid), None)
        if not r: return
        if StudentDialog(self.window(), edit_id=r["id"], edit_first=r["firstname"],
                         edit_last=r["lastname"], edit_course=r["course"],
                         edit_year=r["year"], edit_gender=r["gender"]).exec():
            self.refresh()

    def _on_delete(self, sid):
        if QMessageBox.question(self.window(), "Delete Student",
                f"Permanently delete student '{sid}'?\n\nThis cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            db.delete_student(sid); self.refresh(); self.window().refresh_stats()


class StatCard(QWidget):
    def __init__(self, icon_fn, label: str, warn=False, is_dark=True):
        super().__init__()
        self._warn    = warn
        self._is_dark = is_dark
        self._icon_fn = icon_fn
        self._label   = label
        self.setFixedHeight(104); self.setMinimumWidth(220)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._build_layout()

    def _build_layout(self):
        lay = QHBoxLayout(self); lay.setContentsMargins(20, 0, 20, 0); lay.setSpacing(16)

        ib = QWidget()
        ib.setObjectName("statIconBoxWarn" if self._warn else "statIconBox")
        ib.setFixedSize(QSize(34, 34))
        ib.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if self._is_dark:
            icon_col = QColor(th.WARNING if self._warn else th.CYAN_400)
        else:
            icon_col = QColor("#D97706" if self._warn else "#0EA5E9")

        self._ico = IconWidget(self._icon_fn, size=18, col=icon_col, parent=ib)
        ib_lay = QHBoxLayout(ib); ib_lay.setContentsMargins(8, 8, 8, 8)
        ib_lay.addWidget(self._ico)
        lay.addWidget(ib)

        tc = QVBoxLayout(); tc.setSpacing(2)
        self._val = QLabel("0")
        self._val.setObjectName("statValueWarn" if self._warn else "statValue")
        self._val.setFont(QFont("Fira Code, Consolas, Courier New", 26, QFont.Weight.Bold))
        lbl = QLabel(self._label); lbl.setObjectName("statLabel")
        tc.addWidget(self._val); tc.addWidget(lbl)
        lay.addLayout(tc); lay.addStretch()

    def set_value(self, v):
        self._val.setText(f"{v:,}")

    def set_dark(self, d: bool):
        self._is_dark = d
        icon_col = QColor(th.WARNING if self._warn else th.CYAN_400) if d \
                   else QColor("#D97706" if self._warn else "#0EA5E9")
        self._ico.set_color(icon_col)

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        r    = QRectF(0.5, 0.5, w - 1, h - 1)
        rad  = 16

        if self._is_dark:
            fill = QLinearGradient(0, 0, w, h)
            fill.setColorAt(0, QColor(255, 255, 255, 15))
            fill.setColorAt(1, QColor(6, 182, 212, 8))
            p.setBrush(QBrush(fill)); p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(r, rad, rad)

            sh = QLinearGradient(0, 0, w, h)
            if self._warn:
                sh.setColorAt(0, QColor(252, 211, 77, 25))
                sh.setColorAt(1, QColor(245, 158, 11, 13))
            else:
                sh.setColorAt(0, QColor(103, 232, 249, 30))
                sh.setColorAt(0.4, QColor(255, 255, 255, 10))
                sh.setColorAt(1, QColor(13, 148, 136, 20))
            p.setBrush(QBrush(sh)); p.drawRoundedRect(r, rad, rad)

            al = QLinearGradient(0, 0, w, 0)
            if self._warn:
                al.setColorAt(0, QColor(245, 158, 11, 0))
                al.setColorAt(0.5, QColor(245, 158, 11, 153))
                al.setColorAt(1, QColor(245, 158, 11, 0))
            else:
                al.setColorAt(0, QColor(34, 211, 238, 0))
                al.setColorAt(0.5, QColor(34, 211, 238, 153))
                al.setColorAt(1, QColor(34, 211, 238, 0))
            p.setBrush(QBrush(al))
            p.drawRect(QRectF(0.5, 0.5, w - 1, 1))

            bc = QColor(245, 158, 11, 64) if self._warn else QColor(34, 211, 238, 46)
            p.setPen(QPen(bc, 0.8)); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(r, rad, rad)
        else:
            fill = QLinearGradient(0, 0, w, h)
            if self._warn:
                fill.setColorAt(0, QColor(255, 255, 255, 184))
                fill.setColorAt(1, QColor(255, 251, 235, 148))
            else:
                fill.setColorAt(0, QColor(255, 255, 255, 184))
                fill.setColorAt(1, QColor(224, 247, 250, 148))
            p.setBrush(QBrush(fill)); p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(r, rad, rad)

            shimmer = QLinearGradient(0, 0, w, h)
            if self._warn:
                shimmer.setColorAt(0, QColor(253, 230, 138, 46))
                shimmer.setColorAt(1, QColor(252, 211, 77, 20))
            else:
                shimmer.setColorAt(0, QColor(103, 232, 249, 25))
                shimmer.setColorAt(0.45, QColor(255, 255, 255, 46))
                shimmer.setColorAt(1, QColor(110, 231, 183, 20))
            p.setBrush(QBrush(shimmer)); p.drawRoundedRect(r, rad, rad)

            top = QLinearGradient(0, 0, w, 0)
            if self._warn:
                top.setColorAt(0, QColor(255, 255, 255, 0))
                top.setColorAt(0.35, QColor(255, 255, 255, 140))
                top.setColorAt(0.65, QColor(245, 158, 11, 64))
                top.setColorAt(1, QColor(255, 255, 255, 0))
            else:
                top.setColorAt(0, QColor(255, 255, 255, 0))
                top.setColorAt(0.35, QColor(255, 255, 255, 166))
                top.setColorAt(0.65, QColor(6, 182, 212, 51))
                top.setColorAt(1, QColor(255, 255, 255, 0))
            p.setBrush(QBrush(top))
            p.drawRect(QRectF(0.5, 0.5, w - 1, 2))

            sheen = QLinearGradient(0, 0, w * 0.55, h * 0.55)
            sheen.setColorAt(0, QColor(255, 255, 255, 115))
            sheen.setColorAt(1, QColor(255, 255, 255, 0))
            p.setBrush(QBrush(sheen))
            p.drawRoundedRect(QRectF(0.5, 0.5, w * 0.5, h * 0.5), rad, rad)

            bc = QColor(245, 158, 11, 72) if self._warn else QColor(14, 165, 233, 51)
            p.setPen(QPen(bc, 0.9)); p.setBrush(Qt.BrushStyle.NoBrush)
            p.drawRoundedRect(r, rad, rad)


class Sidebar(QWidget):
    def __init__(self, is_dark=True, parent=None):
        super().__init__(parent)
        self._is_dark = is_dark

    def set_dark(self, d: bool):
        self._is_dark = d
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        if self._is_dark:
            fill = QLinearGradient(0, 0, w, 0)
            fill.setColorAt(0, QColor(7, 24, 40, 235))
            fill.setColorAt(1, QColor(10, 31, 48, 224))
            p.fillRect(0, 0, w, h, fill)
            hl = QLinearGradient(0, 0, w * 0.6, h * 0.6)
            hl.setColorAt(0, QColor(255, 255, 255, 33))
            hl.setColorAt(1, QColor(255, 255, 255, 0))
            p.fillRect(0, 0, w, h, hl)
            p.setPen(QPen(QColor(34, 211, 238, 31), 1))
            p.drawLine(w - 1, 0, w - 1, h)
        else:
            fill = QLinearGradient(0, 0, w, 0)
            fill.setColorAt(0, QColor(255, 255, 255, 209))
            fill.setColorAt(1, QColor(240, 250, 251, 194))
            p.fillRect(0, 0, w, h, fill)

            shimmer = QLinearGradient(0, 0, w, h)
            shimmer.setColorAt(0,    QColor(103, 232, 249, 25))
            shimmer.setColorAt(0.45, QColor(255, 255, 255, 46))
            shimmer.setColorAt(1,    QColor(110, 231, 183, 20))
            p.fillRect(0, 0, w, h, shimmer)

            sheen = QLinearGradient(0, 0, w * 0.55, h * 0.28)
            sheen.setColorAt(0, QColor(255, 255, 255, 115))
            sheen.setColorAt(1, QColor(255, 255, 255, 0))
            p.fillRect(0, 0, w, h, sheen)

            p.setPen(QPen(QColor(6, 182, 212, 46), 1))
            p.drawLine(w - 1, 0, w - 1, h)


class NavButton(QWidget):
    clicked = None

    def __init__(self, icon_fn, label: str, is_dark=True, parent=None):
        super().__init__(parent)
        self._active   = False
        self._hovered  = False
        self._icon_fn  = icon_fn
        self._label    = label
        self._is_dark  = is_dark
        self.setFixedHeight(42)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMouseTracking(True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        lay = QHBoxLayout(self)
        lay.setContentsMargins(14, 0, 14, 0); lay.setSpacing(12)

        self._ico = IconWidget(icon_fn, size=17, col=QColor(th.CYAN_400))
        self._ico.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self._lbl = QLabel(label)
        self._lbl.setObjectName("navBtnLabel")
        self._lbl.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        lay.addSpacing(4)
        lay.addWidget(self._ico)
        lay.addWidget(self._lbl)
        lay.addStretch()

        self._update_style()

    def set_dark(self, d: bool):
        self._is_dark = d
        self._update_style()
        self.update()

    def set_active(self, active: bool):
        self._active = active
        self._update_style()
        self.update()

    def _update_style(self):
        if self._active:
            active_col = QColor(th.CYAN_400) if self._is_dark else QColor("#0EA5E9")
            self._ico.set_color(active_col)
            active_hex = th.CYAN_400 if self._is_dark else "#0EA5E9"
            self._lbl.setStyleSheet(
                f"color: {active_hex}; font-weight: 700; font-size: 14px; background: transparent;")
        else:
            dim = QColor(100, 116, 139)
            self._ico.set_color(dim)
            self._lbl.setStyleSheet(
                "color: #64748B; font-weight: 400; font-size: 14px; background: transparent;")

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = QRectF(0, 0, self.width(), self.height())

        if self._active:
            if self._is_dark:
                fill = QLinearGradient(0, 0, self.width(), self.height())
                fill.setColorAt(0, QColor(255, 255, 255, 15))
                fill.setColorAt(1, QColor(6, 182, 212, 8))
                p.setBrush(QBrush(fill)); p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(r.adjusted(8, 1, -8, -1), 8, 8)
                p.setBrush(QBrush(QColor(34, 211, 238, 200)))
                p.drawRoundedRect(QRectF(4, 10, 3.5, 24), 2, 2)
                p.setPen(QPen(QColor(34, 211, 238, 76), 0.8))
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawRoundedRect(r.adjusted(8, 1, -8, -1), 8, 8)
            else:
                fill = QLinearGradient(0, 0, self.width(), self.height())
                fill.setColorAt(0, QColor(14, 165, 233, 30))
                fill.setColorAt(1, QColor(13, 148, 136, 20))
                p.setBrush(QBrush(fill)); p.setPen(Qt.PenStyle.NoPen)
                p.drawRoundedRect(r.adjusted(8, 1, -8, -1), 10, 10)

                shimmer = QLinearGradient(0, 0, self.width(), self.height())
                shimmer.setColorAt(0, QColor(103, 232, 249, 25))
                shimmer.setColorAt(1, QColor(110, 231, 183, 20))
                p.setBrush(QBrush(shimmer))
                p.drawRoundedRect(r.adjusted(8, 1, -8, -1), 10, 10)

                p.setBrush(QBrush(QColor(14, 165, 233, 255)))
                p.drawRoundedRect(QRectF(7, 9, 3.5, 24), 2, 2)

                p.setPen(QPen(QColor(14, 165, 233, 89), 0.9))
                p.setBrush(Qt.BrushStyle.NoBrush)
                p.drawRoundedRect(r.adjusted(8, 1, -8, -1), 10, 10)

        elif self._hovered:
            hover_col = QColor(6, 182, 212, 15) if self._is_dark else QColor(14, 165, 233, 18)
            p.setBrush(QBrush(hover_col))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(r.adjusted(8, 1, -8, -1), 10, 10)

    def enterEvent(self, e):
        self._hovered = True; self.update(); super().enterEvent(e)

    def leaveEvent(self, e):
        self._hovered = False; self.update(); super().leaveEvent(e)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self.clicked:
            self.clicked()
        super().mousePressEvent(e)


_PAGE_META = {
    "student": ("Students",  "Manage and browse all enrolled student records"),
    "program": ("Programs",  "Manage academic programs and their colleges"),
    "college": ("Colleges",  "Manage college units and departments"),
}

APP_NAME    = "Simple Student Information System"
APP_SUBTITLE = "SSIS"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1024, 680)

        self._dark  = True
        self._views: dict[str, TableView] = {}
        self._nav:   dict[str, NavButton] = {}
        self._stats: dict[str, StatCard]  = {}

        self._build()
        self._apply_theme()
        self._switch("student")

    def _build(self):
        self._bg = GlowBackground(is_dark=True, parent=self)
        self._bg.setGeometry(0, 0, self.width(), self.height())
        self._bg.lower()

        root = QWidget()
        root.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setCentralWidget(root)

        h = QHBoxLayout(root)
        h.setContentsMargins(0, 0, 0, 0); h.setSpacing(0)
        h.addWidget(self._build_sidebar())
        h.addWidget(self._build_content(), 1)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, "_bg"):
            self._bg.setGeometry(0, 0, self.width(), self.height())

    def _build_sidebar(self) -> QWidget:
        self._sidebar = Sidebar(is_dark=True)
        self._sidebar.setObjectName("sidebar")
        self._sidebar.setFixedWidth(224)
        v = QVBoxLayout(self._sidebar)
        v.setContentsMargins(0, 0, 0, 0); v.setSpacing(0)

        brand = QWidget(); brand.setObjectName("sidebarBrand")
        brand.setFixedHeight(74)
        bl = QHBoxLayout(brand); bl.setContentsMargins(16, 0, 16, 0); bl.setSpacing(12)

        logo_box = QWidget(); logo_box.setFixedSize(QSize(38, 38))
        logo_box.setStyleSheet(
            "background: qlineargradient(x1:0,y1:0,x2:1,y2:1,"
            "stop:0 #0EA5E9,stop:1 #0D9488); border-radius:10px;")
        logo_box.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        logo_ico = LogoIconWidget(size=22, parent=logo_box)
        lb_lay = QHBoxLayout(logo_box); lb_lay.setContentsMargins(8, 8, 8, 8)
        lb_lay.addWidget(logo_ico)

        tc = QVBoxLayout(); tc.setSpacing(1)
        t1 = QLabel("SSIS"); t1.setObjectName("brandTitle")
        t2 = QLabel("DIRECTORY"); t2.setObjectName("brandSub")
        tc.addWidget(t1); tc.addWidget(t2)

        bl.addWidget(logo_box); bl.addLayout(tc); bl.addStretch()
        v.addWidget(brand)

        sec = QLabel("NAVIGATION"); sec.setObjectName("navSection")
        v.addWidget(sec); v.addSpacing(4)

        for key, icon_fn, label in (
            ("student", draw_icon_students, "Students"),
            ("program", draw_icon_programs, "Programs"),
            ("college", draw_icon_colleges, "Colleges"),
        ):
            btn = NavButton(icon_fn, label, is_dark=True, parent=self._sidebar)
            btn.clicked = lambda k=key: self._switch(k)
            self._nav[key] = btn
            v.addWidget(btn)

        v.addStretch()

        footer = QWidget(); footer.setObjectName("sidebarFooter")
        fl = QHBoxLayout(footer); fl.setContentsMargins(14, 0, 14, 0); fl.setSpacing(10)

        self._theme_icon = IconWidget(draw_icon_sun, size=16, col=QColor(100, 116, 139))
        self._theme_lbl  = QLabel("Light Mode")
        self._theme_lbl.setObjectName("themeToggleLabel")
        self._theme_lbl.setStyleSheet(
            "color: #64748B; font-size: 13px; background: transparent;")

        theme_btn_w = QWidget(); theme_btn_w.setObjectName("themeToggle")
        theme_btn_w.setCursor(Qt.CursorShape.PointingHandCursor)
        theme_btn_w.setFixedHeight(40)
        tbl = QHBoxLayout(theme_btn_w); tbl.setContentsMargins(12, 0, 12, 0); tbl.setSpacing(8)
        tbl.addWidget(self._theme_icon); tbl.addWidget(self._theme_lbl); tbl.addStretch()

        def _toggle(_=None):
            self._toggle_theme()

        theme_btn_w.mousePressEvent = _toggle
        fl.addWidget(theme_btn_w)
        v.addWidget(footer)

        return self._sidebar

    def _build_content(self) -> QWidget:
        panel = QWidget()
        panel.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        v = QVBoxLayout(panel); v.setContentsMargins(0, 0, 0, 0); v.setSpacing(0)

        v.addWidget(self._build_topbar()); v.addWidget(_hline())
        v.addWidget(self._build_stats()); v.addWidget(_hline())

        self._stack = QStackedWidget()
        self._stack.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        for key, cls in (("student", StudentView),
                          ("program", ProgramView),
                          ("college", CollegeView)):
            view = cls(); self._views[key] = view; self._stack.addWidget(view)

        v.addWidget(self._stack, 1)
        return panel

    def _build_topbar(self) -> QWidget:
        bar = QWidget(); bar.setObjectName("topBar")
        bar.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay = QHBoxLayout(bar); lay.setContentsMargins(28, 0, 28, 0)
        col = QVBoxLayout(); col.setSpacing(2)
        self._page_title = QLabel("Students"); self._page_title.setObjectName("pageTitle")
        self._page_sub   = QLabel("Manage and browse all enrolled student records")
        self._page_sub.setObjectName("pageSubtitle")
        col.addWidget(self._page_title); col.addWidget(self._page_sub)
        lay.addLayout(col); lay.addStretch()
        return bar

    def _build_stats(self) -> QWidget:
        strip = QWidget(); strip.setObjectName("statsStrip")
        strip.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        lay = QHBoxLayout(strip); lay.setContentsMargins(28, 10, 28, 10); lay.setSpacing(16)

        for key, icon_fn, label, warn in (
            ("students",   draw_icon_students, "TOTAL STUDENTS", False),
            ("programs",   draw_icon_programs, "PROGRAMS",       False),
            ("colleges",   draw_icon_colleges, "COLLEGES",       False),
            ("unassigned", draw_icon_warning,  "NO COURSE",      True),
        ):
            card = StatCard(icon_fn=icon_fn, label=label, warn=warn, is_dark=True)
            self._stats[key] = card; lay.addWidget(card)

        lay.addStretch()
        return strip

    def _switch(self, key: str):
        for k, btn in self._nav.items():
            btn.set_active(k == key)
        self._stack.setCurrentWidget(self._views[key])
        title, sub = _PAGE_META[key]
        self._page_title.setText(title); self._page_sub.setText(sub)
        self._views[key].refresh()

    def refresh_stats(self):
        s = db.get_stats()
        self._stats["students"].set_value(s["students"])
        self._stats["programs"].set_value(s["programs"])
        self._stats["colleges"].set_value(s["colleges"])
        self._stats["unassigned"].set_value(s["unassigned"])

    def _toggle_theme(self):
        self._dark = not self._dark; self._apply_theme()
        key = next((k for k, v in self._views.items()
                    if self._stack.currentWidget() is v), "student")
        self._views[key].refresh()

    def _apply_theme(self):
        QApplication.instance().setStyleSheet(th.qss(self._dark))

        self._bg.set_dark(self._dark)
        self._sidebar.set_dark(self._dark)

        for v in self._views.values():
            v.set_dark(self._dark)

        for card in self._stats.values():
            card.set_dark(self._dark)
            card.update()

        for btn in self._nav.values():
            btn.set_dark(self._dark)

        if self._dark:
            self._theme_icon._icon_fn = draw_icon_sun
            self._theme_lbl.setText("Light Mode")
            self._theme_lbl.setStyleSheet("color: #64748B; font-size: 13px; background: transparent;")
            self._theme_icon.set_color(QColor(100, 116, 139))
        else:
            self._theme_icon._icon_fn = draw_icon_moon
            self._theme_lbl.setText("Dark Mode")
            self._theme_lbl.setStyleSheet("color: #475569; font-size: 13px; background: transparent;")
            self._theme_icon.set_color(QColor(71, 85, 105))
        self._theme_icon.update()

        if hasattr(self, "_bg"):
            self._bg.update()

        self.refresh_stats()

#finally done

def run():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    db.init_db()
    app.setStyleSheet(th.qss(True))
    win = MainWindow()
    win.refresh_stats()
    win.show()
    sys.exit(app.exec())
