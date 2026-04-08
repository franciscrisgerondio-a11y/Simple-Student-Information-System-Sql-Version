import re
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QFrame, QMessageBox, QWidget,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
import db


_ID_RE = re.compile(r"^\d{4}-\d{4}$")


def _hline() -> QFrame:
    f = QFrame()
    f.setObjectName("divider")
    f.setFrameShape(QFrame.Shape.HLine)
    return f


class _FormRow(QHBoxLayout):
    def __init__(self, label: str, widget: QWidget):
        super().__init__()
        self.setSpacing(12)
        lbl = QLabel(label)
        lbl.setObjectName("formLabel")
        lbl.setFixedWidth(120)
        lbl.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignRight)
        self.addWidget(lbl)
        self.addWidget(widget)


class _BaseDialog(QDialog):
    def __init__(self, parent, title: str, subtitle: str = ""):
        super().__init__(parent)
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setWindowTitle(title)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        hdr = QWidget()
        hdr.setObjectName("dialogHeader")
        hdr.setFixedHeight(56)
        hlay = QHBoxLayout(hdr)
        hlay.setContentsMargins(20, 0, 20, 0)
        hlay.setSpacing(0)

        text_col = QVBoxLayout()
        text_col.setSpacing(1)
        t = QLabel(title)
        t.setObjectName("dialogTitle")
        s = QLabel(subtitle)
        s.setObjectName("dialogSubtitle")
        text_col.addWidget(t)
        if subtitle:
            text_col.addWidget(s)
        hlay.addLayout(text_col)
        hlay.addStretch()
        root.addWidget(hdr)

        body = QWidget()
        body.setObjectName("dialogBody")
        self._form = QVBoxLayout(body)
        self._form.setContentsMargins(24, 20, 24, 16)
        self._form.setSpacing(14)
        root.addWidget(body, 1)

        root.addWidget(_hline())

        foot = QWidget()
        foot.setObjectName("dialogBody")
        flay = QHBoxLayout(foot)
        flay.setContentsMargins(20, 12, 20, 12)
        flay.addStretch()

        self._btn_cancel = QPushButton("Cancel")
        self._btn_cancel.setObjectName("btnCancel")
        self._btn_cancel.clicked.connect(self.reject)

        self._btn_save = QPushButton("Save")
        self._btn_save.setObjectName("btnSave")
        self._btn_save.setDefault(True)
        self._btn_save.clicked.connect(self._on_save)

        flay.addWidget(self._btn_cancel)
        flay.addSpacing(8)
        flay.addWidget(self._btn_save)
        root.addWidget(foot)

    def _on_save(self):
        raise NotImplementedError

    def _err(self, msg: str):
        QMessageBox.warning(self, "Validation Error", msg)

    def _critical(self, msg: str):
        QMessageBox.critical(self, "Error", msg)


class CollegeDialog(_BaseDialog):
    def __init__(self, parent, edit_code: str = None, edit_name: str = None):
        is_edit = edit_code is not None
        super().__init__(
            parent,
            title   = "Edit College" if is_edit else "Add College",
            subtitle= f"Editing  {edit_code}" if is_edit else "Create a new college record",
        )
        self._edit_code = edit_code
        self.setFixedWidth(480)

        self._inp_code = QLineEdit()
        self._inp_code.setPlaceholderText("e.g.  CCS")
        self._form.addLayout(_FormRow("College Code", self._inp_code))

        self._inp_name = QLineEdit()
        self._inp_name.setPlaceholderText("e.g.  College of Computer Studies")
        self._form.addLayout(_FormRow("College Name", self._inp_name))

        if is_edit:
            self._inp_code.setText(edit_code)
            self._inp_code.setEnabled(False)
            self._inp_name.setText(edit_name or "")
            self._inp_name.setFocus()
        else:
            self._inp_code.setFocus()

    def _on_save(self):
        code = self._inp_code.text().strip().upper()
        name = self._inp_name.text().strip()

        if not code:
            self._err("College code is required.")
            self._inp_code.setFocus(); return
        if not name:
            self._err("College name is required.")
            self._inp_name.setFocus(); return
        if not self._edit_code and db.college_exists(code):
            self._err(f"College code '{code}' already exists.")
            self._inp_code.setFocus(); return

        try:
            if self._edit_code:
                db.update_college(code, name)
            else:
                db.add_college(code, name)
            self.accept()
        except Exception as ex:
            self._critical(str(ex))


class ProgramDialog(_BaseDialog):
    def __init__(self, parent, edit_code: str = None,
                 edit_name: str = None, edit_college: str = None):
        is_edit = edit_code is not None
        super().__init__(
            parent,
            title   = "Edit Program" if is_edit else "Add Program",
            subtitle= f"Editing  {edit_code}" if is_edit else "Create a new program record",
        )
        self._edit_code = edit_code
        self.setFixedWidth(520)

        self._inp_code = QLineEdit()
        self._inp_code.setPlaceholderText("e.g.  BSCS")
        self._form.addLayout(_FormRow("Program Code", self._inp_code))

        self._inp_name = QLineEdit()
        self._inp_name.setPlaceholderText("e.g.  Bachelor of Science in Computer Science")
        self._form.addLayout(_FormRow("Program Name", self._inp_name))

        self._cmb_college = QComboBox()
        self._cmb_college.addItem("— Select a college —", userData=None)
        for c in db.get_all_colleges():
            self._cmb_college.addItem(f"{c['code']}  —  {c['name']}", userData=c["code"])
        self._form.addLayout(_FormRow("College", self._cmb_college))

        if is_edit:
            self._inp_code.setText(edit_code)
            self._inp_code.setEnabled(False)
            self._inp_name.setText(edit_name or "")
            idx = self._cmb_college.findData(edit_college)
            if idx >= 0:
                self._cmb_college.setCurrentIndex(idx)
            self._inp_name.setFocus()
        else:
            self._inp_code.setFocus()

    def _on_save(self):
        code    = self._inp_code.text().strip().upper()
        name    = self._inp_name.text().strip()
        college = self._cmb_college.currentData()

        if not code:
            self._err("Program code is required."); return
        if not name:
            self._err("Program name is required."); return
        if not college:
            self._err("Please select a college."); return
        if not self._edit_code and db.program_exists(code):
            self._err(f"Program code '{code}' already exists."); return

        try:
            if self._edit_code:
                db.update_program(code, name, college)
            else:
                db.add_program(code, name, college)
            self.accept()
        except Exception as ex:
            self._critical(str(ex))


class StudentDialog(_BaseDialog):
    def __init__(self, parent,
                 edit_id=None, edit_first=None, edit_last=None,
                 edit_course=None, edit_year=None, edit_gender=None):
        is_edit = edit_id is not None
        super().__init__(
            parent,
            title   = "Edit Student" if is_edit else "Add Student",
            subtitle= f"Editing  {edit_id}" if is_edit else "Create a new student record",
        )
        self._edit_id = edit_id
        self.setFixedWidth(540)

        self._inp_id = QLineEdit()
        self._inp_id.setPlaceholderText("YYYY-NNNN  e.g.  2024-1001")
        self._form.addLayout(_FormRow("Student ID", self._inp_id))

        self._inp_first = QLineEdit()
        self._inp_first.setPlaceholderText("First name")
        self._form.addLayout(_FormRow("First Name", self._inp_first))

        self._inp_last = QLineEdit()
        self._inp_last.setPlaceholderText("Last name")
        self._form.addLayout(_FormRow("Last Name", self._inp_last))

        self._form.addSpacing(4)
        self._form.addWidget(_hline())
        self._form.addSpacing(4)

        self._cmb_college = QComboBox()
        self._cmb_college.addItem("— All Colleges —", userData=None)
        self._all_colleges = db.get_all_colleges()
        for c in self._all_colleges:
            self._cmb_college.addItem(f"{c['code']}  —  {c['name']}", userData=c["code"])
        self._form.addLayout(_FormRow("College Filter", self._cmb_college))

        self._cmb_program = QComboBox()
        self._form.addLayout(_FormRow("Course", self._cmb_program))

        self._cmb_year = QComboBox()
        for y in ("1st Year", "2nd Year", "3rd Year", "4th Year"):
            self._cmb_year.addItem(y)
        self._form.addLayout(_FormRow("Year Level", self._cmb_year))

        self._cmb_gender = QComboBox()
        for g in ("Male", "Female", "Other"):
            self._cmb_gender.addItem(g)
        self._form.addLayout(_FormRow("Gender", self._cmb_gender))

        self._cmb_college.currentIndexChanged.connect(self._reload_programs)
        self._reload_programs()

        if is_edit:
            self._inp_id.setText(edit_id)
            self._inp_id.setEnabled(False)
            self._inp_first.setText(edit_first or "")
            self._inp_last.setText(edit_last or "")

            if edit_course and edit_course != "NULL":
                all_p = db.get_all_programs()
                prog  = next((p for p in all_p if p["code"] == edit_course), None)
                if prog and prog["college"]:
                    idx = self._cmb_college.findData(prog["college"])
                    if idx >= 0:
                        self._cmb_college.setCurrentIndex(idx)

            pidx = self._cmb_program.findData(edit_course)
            if pidx >= 0:
                self._cmb_program.setCurrentIndex(pidx)

            if edit_year is not None:
                self._cmb_year.setCurrentIndex(int(edit_year) - 1)

            gidx = self._cmb_gender.findText(edit_gender or "Male")
            if gidx >= 0:
                self._cmb_gender.setCurrentIndex(gidx)

            self._inp_first.setFocus()
        else:
            self._inp_id.setFocus()

    def _reload_programs(self):
        self._cmb_program.blockSignals(True)
        self._cmb_program.clear()
        self._cmb_program.addItem("NULL  —  No course assigned", userData=None)

        college_code = self._cmb_college.currentData()
        all_p = db.get_all_programs()
        for p in all_p:
            if college_code is None or p["college"] == college_code:
                self._cmb_program.addItem(
                    f"{p['code']}  —  {p['name']}", userData=p["code"]
                )
        self._cmb_program.blockSignals(False)

    def _on_save(self):
        id_    = self._inp_id.text().strip()
        first  = self._inp_first.text().strip()
        last   = self._inp_last.text().strip()
        course = self._cmb_program.currentData()
        year   = self._cmb_year.currentIndex() + 1
        gender = self._cmb_gender.currentText()

        if not _ID_RE.match(id_):
            self._err(
                "Student ID must follow the format YYYY-NNNN\n"
                "(4 digits, a dash, then 4 digits).\n\n"
                "Example:  2024-1001"
            )
            self._inp_id.setFocus(); return
        if not first:
            self._err("First name is required."); self._inp_first.setFocus(); return
        if not last:
            self._err("Last name is required."); self._inp_last.setFocus(); return
        if not self._edit_id and db.student_exists(id_):
            self._err(f"Student ID '{id_}' already exists."); self._inp_id.setFocus(); return

        try:
            if self._edit_id:
                db.update_student(id_, first, last, course, year, gender)
            else:
                db.add_student(id_, first, last, course, year, gender)
            self.accept()
        except Exception as ex:
            self._critical(str(ex))
