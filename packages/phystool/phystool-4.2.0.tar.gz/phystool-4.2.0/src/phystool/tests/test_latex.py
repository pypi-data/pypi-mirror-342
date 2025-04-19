from unittest import TestCase

from pathlib import Path
from tempfile import NamedTemporaryFile

from phystool.config import config
from phystool.latex import (
    PdfLatex,
    LatexLogParser,
)


class TexContent:
    def __init__(
        self,
        header: str = r"\documentclass{article}"
    ):
        self._header = header
        self._body = ""

    def header(self, txt: str) -> None:
        self._header += "\n" + txt

    def body(self, txt: str) -> None:
        self._body += "\n" + txt

    def get(self) -> str:
        return f"{self._header}\n\\begin{{document}}{self._body}\n\\end{{document}}"  # noqa


class TestLatexLogParser(TestCase):
    def _compile(
        self,
        texcontent: TexContent,
        fails: bool,
        clean: bool = True,
        twice: bool = False
    ) -> tuple[LatexLogParser, Path]:
        with NamedTemporaryFile(
            "w",
            suffix=".tex",
            delete_on_close=False
        ) as fp:
            fp.write(texcontent.get())
            fp.close()

            fname = Path(fp.name)
            pdflatex = PdfLatex(fname)
            if fails:
                with self.assertRaises(PdfLatex.CompilationError):
                    pdflatex.compile()
            else:
                pdflatex.compile()
                if twice:
                    pdflatex.compile()

            parser = LatexLogParser(fname)
            parser.process()
            if clean:
                pdflatex.clean([".aux", ".log", ".out", ".pdf"])
            return parser, fname

    def test_W_package_geometry(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage[margin=20cm]{geometry}")
        parser, fname = self._compile(texcontent, False)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 3)
        self.assertEqual(msg[0], r"[W:package='geometry'] `width' results in NEGATIVE (-523.81523pt).")  # noqa
        self.assertEqual(msg[1], r"                       `lmargin' or `rmargin' should be shortened in length.")  # noqa
        self.assertEqual(msg[2], f"    -> {fname}")

    def test_W_missing_ref(self):
        texcontent = TexContent()
        texcontent.body(r"\ref{toto}")
        parser, fname = self._compile(texcontent, False)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[W:LaTeX] Reference `toto' on page 1 undefined on input line 3.")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")
        msg = parser.warning()[1].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[W:LaTeX] There were undefined references.")
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_W_labels_may_have_changed(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{equation}")
        texcontent.body(r"foo \label{foo}")
        texcontent.body(r"\end{equation}")
        parser, fname = self._compile(texcontent, False)
        self.assertTrue(parser.should_recompile())
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[W:LaTeX] Label(s) may have changed. Rerun to get cross-references right.")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_W_label_multiply_defined(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{equation}")
        texcontent.body(r"foo \label{foo}")
        texcontent.body(r"\end{equation}")
        texcontent.body(r"\begin{equation}")
        texcontent.body(r"bar \label{foo}")
        texcontent.body(r"\end{equation}")
        parser, fname = self._compile(texcontent, False, twice=True)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[W:LaTeX] Label `foo' multiply defined.")
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_W_unused_gobal_options(self):
        texcontent = TexContent(r"\documentclass[coucou]{article}")
        texcontent.body("toto")
        parser, fname = self._compile(texcontent, False)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], "[W:LaTeX] Unused global option(s): [coucou].")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_W_float_specifier_changed(self):
        img = config.DB_DIR / "figures" / "tech_support_cheat_sheet.png"
        texcontent = TexContent()
        texcontent.header(r"\usepackage[pdftex]{graphicx}")
        texcontent.header(r"\usepackage[french]{babel}")
        texcontent.header(r"\usepackage[T1]{fontenc}")
        texcontent.header(r"\usepackage{lipsum}")
        texcontent.header(r"\setlipsum{auto-lang=false}")
        texcontent.body(r"\lipsum[1-3]")
        texcontent.body(r"\begin{figure}[h!]")
        texcontent.body(fr"\includegraphics[scale=0.5]{{{img}}}")
        texcontent.body(r"\end{figure}")
        texcontent.body(r"\lipsum")
        parser, fname = self._compile(texcontent, False)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 3)
        self.assertEqual(msg[0], "[W:LaTeX] `!h' float specifier changed to `!ht'.")  # noqa
        self.assertEqual(msg[1], f"    use {img}")
        self.assertEqual(msg[2], f"    -> {fname}")

    def test_W_no_position_in_float_specifier(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{figure}[]")
        texcontent.body(r"\end{figure}")
        parser, fname = self._compile(texcontent, False)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[W:LaTeX] No positions in optional float specifier. Default added (so using `tbp') on input line 3.")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_W_siunitx_conflict_with_physics(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{siunitx}")
        texcontent.header(r"\usepackage{physics}")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, False)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 7)
        self.assertEqual(msg[0], r"[W:package='siunitx']"+' Detected the "physics" package:')  # noqa
        self.assertEqual(msg[1], r"                      omitting definition of \qty.")  # noqa
        self.assertEqual(msg[2], r"                      If you want to use \qty with the siunitx definition,")  # noqa
        self.assertEqual(msg[3], r"                      add ")
        self.assertEqual(msg[4], r"                      \AtBeginDocument{\RenewCommandCopy\qty\SI}")  # noqa
        self.assertEqual(msg[5], r"                      to your preamble.")
        self.assertEqual(msg[6], f"    -> {fname}")

    def test_E_package_amsmath(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{amsmath}")
        texcontent.body(r"\begin{aligned}")
        texcontent.body(r"toto")
        texcontent.body(r"\end{aligned}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:package='amsmath'] \begin{aligned} allowed only in math mode.")  # noqa
        self.assertEqual(msg[1], r"    l.5 t")
        self.assertEqual(msg[2], r"         oto")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_package_cmd(self):
        texcontent = TexContent()
        texcontent.header(r"\NewDocumentCommand{\toto}{}{}% foo")
        texcontent.header(r"\NewDocumentCommand{\toto}{}{}% bar")
        texcontent.body("toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:package='cmd'] Command '\toto' already defined.")  # noqa
        self.assertEqual(msg[1], r"    l.3 \NewDocumentCommand{\toto}{}{}")
        self.assertEqual(msg[2], r"                                      % bar")  # noqa
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_package_keyval(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{graphicx}")
        texcontent.body(r"\includegraphics[foo=bar]{toto}% tutu")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:package='keyval'] foo undefined.")
        self.assertEqual(msg[1], r"    l.4 \includegraphics[foo=bar]{toto}")
        self.assertEqual(msg[2], r"                                       % tutu")  # noqa
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_only_in_math_mode(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{amsmath}")
        texcontent.body(r"foo \mathrm{toto} bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] \mathrm allowed only in math mode.")  # noqa
        self.assertEqual(msg[1], r"    l.4 foo \mathrm")
        self.assertEqual(msg[2], r"                   {toto} bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_file_not_found(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage[pdftex]{graphicx}")
        texcontent.body(r"\includegraphics{foo}bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] File `foo' not found.")
        self.assertEqual(msg[1], r"    l.4 \includegraphics{foo}")
        self.assertEqual(msg[2], r"                             bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_pdf_inclusion(self):
        texcontent = TexContent()
        img = config.DB_DIR / "01cdfb94-e20e-446c-91df-12eacc7ab474.pdf"
        texcontent.header(r"\usepackage[pdftex]{graphicx}")
        texcontent.body(fr"\includegraphics[page=2]{{{img}}}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], fr"[E:pdfTeX] pdflatex (file {img}): PDF inclusion: required page does not exist <1>")
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_E_file_not_found_latex3(self):
        inputname = 46*"m"
        texcontent = TexContent()
        texcontent.header(r"\ExplSyntaxOn")
        texcontent.header(r"\NewDocumentCommand{\toto}{}{\file_input:n {" + inputname + "}}")  # noqa
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body(r"\toto{} bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], fr"[E:LaTeX] File '{inputname}' not found.")
        self.assertEqual(msg[1], r"    l.6 \toto")
        self.assertEqual(msg[2], r"             {} bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_can_be_used_only_in_preamble(self):
        texcontent = TexContent()
        texcontent.body(r"\usepackage{toto}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Can be used only in preamble.")
        self.assertEqual(msg[1], r"    l.3 \usepackage")
        self.assertEqual(msg[2], r"                   {toto}")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_missing_begin_document(self):
        texcontent = TexContent()
        texcontent.header("toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Missing \begin{document}.")
        self.assertEqual(msg[1], r"    l.2 t")
        self.assertEqual(msg[2], r"         oto")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_invalid_in_math_mode(self):
        texcontent = TexContent()
        texcontent.body(r"$\item$")
        parser, fname = self._compile(texcontent, True, False)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Command \item invalid in math mode.")  # noqa
        self.assertEqual(msg[1], r"    l.3 $\item")
        self.assertEqual(msg[2], r"              $")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_control_sequence_alread_defined(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{expl3}")
        texcontent.header(r"\ExplSyntaxOn")
        texcontent.header(r"\tl_new:N \l_toto_tl % bar")
        texcontent.header(r"\tl_new:N \l_toto_tl % bar")
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body("toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Control sequence \l_toto_tl already defined.")  # noqa
        self.assertEqual(msg[1], r"    l.5 \tl_new:N \l_toto_tl")
        self.assertEqual(msg[2], r"                             % bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_no_line_here_to_end(self):
        texcontent = TexContent()
        texcontent.body(r"\newpage")
        texcontent.body(r"\\")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] There's no line here to end.")
        self.assertEqual(msg[1], r"    l.5 t")
        self.assertEqual(msg[2], r"         oto")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_environment_endefined(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{toto}[bar]")
        texcontent.body(r"foo")
        texcontent.body(r"\end{toto}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Environment toto undefined.")
        self.assertEqual(msg[1], r"    l.3 \begin{toto}")
        self.assertEqual(msg[2], r"                    [bar]")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_missing_item(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{itemize}")
        texcontent.body(r"foo")
        texcontent.body(r"\end{itemize}bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Something's wrong--perhaps a missing \item.")  # noqa
        self.assertEqual(msg[1], r"    l.5 \end{itemize}")
        self.assertEqual(msg[2], r"                     bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_environment_foo_ended_by_bar(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{center}")
        texcontent.body(r"toto")
        texcontent.body(r"\end{itemize}toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] \begin{center} on input line 3 ended by \end{itemize}.")  # noqa
        self.assertEqual(msg[1], r"    l.5 \end{itemize}")
        self.assertEqual(msg[2], r"                     toto")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_unknown_float_option(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{figure}[foo] bar")
        texcontent.body(r"\end{figure}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Unknown float option `f'.")
        self.assertEqual(msg[1], r"    l.3 \begin{figure}[foo]")
        self.assertEqual(msg[2], r"                            bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_misplaced_alignment(self):
        texcontent = TexContent()
        texcontent.body(r"foo & bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Misplaced alignment tab character &.")
        self.assertEqual(msg[1], r"    l.3 foo &")
        self.assertEqual(msg[2], r"              bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_misplaced_noalign(self):
        texcontent = TexContent()
        texcontent.body(r"foo\hline bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Misplaced \noalign.")
        self.assertEqual(msg[1], r"    l.3 foo\hline")
        self.assertEqual(msg[2], r"                  bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_missing_number(self):
        texcontent = TexContent()
        texcontent.body(r"foo\vspace{toto}bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Missing number, treated as zero.")
        self.assertEqual(msg[1], r"    l.3 foo\vspace{toto}")
        self.assertEqual(msg[2], r"                        bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_missing_brace_inserted(self):
        texcontent = TexContent()
        texcontent.body(r"$\frac\\$bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Missing } inserted.")
        self.assertEqual(msg[1], r"    l.3 $\frac\\$")
        self.assertEqual(msg[2], r"                 bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_missing_dollar(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{equation}")
        texcontent.body("toto")
        texcontent.body("")
        texcontent.body(r"\end{equation}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 3)
        self.assertEqual(msg[0], r"[E] Missing $ inserted.")
        self.assertEqual(msg[1], r"    l.5")
        self.assertEqual(msg[2], f"    -> {fname}")

    def test_E_extra_alignment_tab(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{tabular}{c}")
        texcontent.body(r"1 & 2")
        texcontent.body(r"\end{tabular}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Extra alignment tab has been changed to \cr.")  # noqa
        self.assertEqual(msg[1], r"    l.4 1 &")
        self.assertEqual(msg[2], r"            2")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_illegal_character_in_array(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{tabular}[l]")
        texcontent.body(r"toto")
        texcontent.body(r"\end{tabular}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Illegal character in array arg.")
        self.assertEqual(msg[1], r"    l.4 t")
        self.assertEqual(msg[2], r"         oto")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_too_many_braces(self):
        texcontent = TexContent()
        texcontent.body(r"\textbf{toto}}foo")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Too many }'s.")
        self.assertEqual(msg[1], r"    l.3 \textbf{toto}}")
        self.assertEqual(msg[2], r"                      foo")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_extra_brace_or_forgotten_endgroup(self):
        texcontent = TexContent()
        texcontent.body(r"\begin{center}}foo")
        texcontent.body(r"\textbf{toto}")
        texcontent.body(r"\end{center}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Extra }, or forgotten \endgroup.")
        self.assertEqual(msg[1], r"    l.3 \begin{center}}")
        self.assertEqual(msg[2], r"                       foo")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_argument_of_has_an_extra_brace(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{amsmath}")
        texcontent.body(r"$\dot\frac{1}{2}$")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Argument of \frac  has an extra }.")
        self.assertEqual(msg[1], r"    l.4 $\dot\frac")
        self.assertEqual(msg[2], r"                  {1}{2}$")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_undefined_control_sequence(self):
        # If in header:
        # | ! Undefined control sequence.
        # | <recently read> \unkowncommand
        # |
        # | l.2 \unkowncommand
        texcontent = TexContent()
        texcontent.header(r"\unkowncommand toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Undefined control sequence.")
        self.assertEqual(msg[1], r"    l.2 \unkowncommand")
        self.assertEqual(msg[2], r"                       toto")
        self.assertEqual(msg[3], f"    -> {fname}")

        # If in body:
        # | ! Undefined control sequence.
        # | l.3 \unkowncommand
        texcontent = TexContent()
        texcontent.body(r"\unkowncommand toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Undefined control sequence.")
        self.assertEqual(msg[1], r"    l.3 \unkowncommand")
        self.assertEqual(msg[2], r"                       toto")
        self.assertEqual(msg[3], f"    -> {fname}")

        # If in newcommand (irrelevant if in header or body):
        # | ! Undefined control sequence.
        # | \foo code -> \unknownncommand
        # TODO: find a way to extract the reason (-> \unkowncommand)
        texcontent = TexContent()
        texcontent.header(r"\NewDocumentCommand{\foo}{}{")
        texcontent.header(r"\unknowncommand")
        texcontent.header(r"}")
        texcontent.header(r"\foo{}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Undefined control sequence.")
        self.assertEqual(msg[1], r"    l.5 \foo")
        self.assertEqual(msg[2], r"            {}")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_WE_invalid_in_math_mode(self):
        texcontent = TexContent()
        texcontent.body(r"$é$")
        parser, fname = self._compile(texcontent, True)
        msg = parser.warning()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[W:LaTeX] Command \' invalid in math mode on input line 3.")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Please use \mathaccent for accents in math mode.")  # noqa
        self.assertEqual(msg[1], r"    l.3 $é")
        self.assertEqual(msg[2], r"           $")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_file_ended_while_scanning(self):
        texcontent = TexContent()
        texcontent.body(r"\textbf{{toto}bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[E] File ended while scanning use of \textbf .")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_E_double_subscript(self):
        texcontent = TexContent()
        texcontent.body(r"$toto_1_2$")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Double subscript.")
        self.assertEqual(msg[1], r"    l.3 $toto_1_")
        self.assertEqual(msg[2], r"                2$")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_display_math_should_end_with_two_dollars(self):
        texcontent = TexContent()
        texcontent.body(r"$$toto$ foo")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Display math should end with $$.")
        self.assertEqual(msg[1], r"    l.3 $$toto$ ")
        self.assertEqual(msg[2], r"                foo")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_illegal_parameter_number_in_definition(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{tcolorbox}")
        texcontent.header(r"\ExplSyntaxOn")
        texcontent.header(r"\cs_new_protected:Nn \foo: {")
        texcontent.header(r"    #2")
        texcontent.header(r"}")
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body(r"toto")
        # TODO: the parameter number could be caught if one starts to read
        # context before first occurence of "l." as is it displayed in the line
        # just above. Maybe I could try to check when "<to be read again> is
        # displayed.
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[E] Illegal parameter number in definition of \foo:.")  # noqa
        self.assertEqual(msg[1], f"    -> {fname}")

    def test_E_illegal_unit_of_measure(self):
        texcontent = TexContent()
        texcontent.body(r"foo\hspace{3toto}bar")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Illegal unit of measure (pt inserted).")  # noqa
        self.assertEqual(msg[1], r"    l.3 foo\hspace{3toto}")
        self.assertEqual(msg[2], r"                         bar")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_no_shape_XX_is_known(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{tikz}")
        texcontent.body(r"\tikz{\draw (0,0) -- (B)}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:package='pgf'] No shape named `B' is known.")  # noqa
        self.assertEqual(msg[1], r"    l.4 \tikz{\draw (0,0) -- (B)")
        self.assertEqual(msg[2], r"                                }")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_package_pgf_error(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{tikz}")
        texcontent.body(r"\tikz{\node[rectangle, rotate=12 m]{};}")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E] Package PGF Math Error: Unknown operator `m' or `m@' (in '12 m').")  # noqa
        self.assertEqual(msg[1], r"    l.4 \tikz{\node[rectangle, rotate=12 m]{};")  # noqa
        self.assertEqual(msg[2], r"                                              }")  # noqa
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_package_pgf_duplicate_power_part(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{siunitx}")
        texcontent.body(r"\unit{\meter\cubed\cubed} %  noqa")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:package='siunitx'] Duplicate power part: \cubed.")  # noqa
        self.assertEqual(msg[1], r"    l.4 \unit{\meter\cubed\cubed}")
        self.assertEqual(msg[2], r"                                  %  noqa")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_the_key_is_unknown_and_is_being_ignord(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{siunitx}")
        texcontent.body(r"\unit[toto]{\meter\cubed\cubed} %  noqa")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] The key 'siunitx/toto' is unknown and is being ignored.")  # noqa
        self.assertEqual(msg[1], r"    l.4 \unit[toto]{\meter\cubed\cubed}")
        self.assertEqual(msg[2], r"                                        %  noqa")  # noqa
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_E_option_clash(self):
        texcontent = TexContent()
        texcontent.header(r"\usepackage{tcolorbox}")
        texcontent.header(r"\usepackage[pdftex]{graphicx}")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.error()[0].message.split("\n")
        self.assertEqual(len(msg), 4)
        self.assertEqual(msg[0], r"[E:LaTeX] Option clash for package graphicx.")  # noqa
        self.assertEqual(msg[1], r"    l.4 \begin")
        self.assertEqual(msg[2], r"              {document}")
        self.assertEqual(msg[3], f"    -> {fname}")

    def test_S_show(self):
        texcontent = TexContent()
        texcontent.header(r"\ExplSyntaxOn")
        texcontent.header(r"\tl_show:N \l_tmpa_tl")
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.latex3()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], r"[S:LaTeX3] \l_tmpa_tl=.")
        self.assertEqual(msg[1], f"    -> {fname}")

        texcontent = TexContent()
        texcontent.header(r"\ExplSyntaxOn")
        foolong = 30*"foo"
        texcontent.header(fr"\tl_show:n {{{foolong}}}")
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.latex3()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], fr"[S:LaTeX3] {foolong}.")
        self.assertEqual(msg[1], f"    -> {fname}")

        texcontent = TexContent()
        texcontent.header(r"\ExplSyntaxOn")
        texcontent.header(fr"\tl_set:Nn \l_tmpa_tl {{{foolong}}}")
        texcontent.header(r"\tl_show:N \l_tmpa_tl")
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.latex3()[0].message.split("\n")
        self.assertEqual(len(msg), 2)
        self.assertEqual(msg[0], fr"[S:LaTeX3] \l_tmpa_tl={foolong}.")
        self.assertEqual(msg[1], f"    -> {fname}")

        texcontent = TexContent()
        texcontent.header(r"\ExplSyntaxOn")
        texcontent.header(fr"\tl_set:Nn \l_tmpa_tl {{{foolong} ~ {foolong}}}")
        texcontent.header(r"\tl_show:N \l_tmpa_tl")
        texcontent.header(r"\ExplSyntaxOff")
        texcontent.body(r"toto")
        parser, fname = self._compile(texcontent, True)
        msg = parser.latex3()[0].message.split("\n")
        self.assertEqual(len(msg), 3)
        self.assertEqual(msg[0], fr"[S:LaTeX3] \l_tmpa_tl={foolong}")
        self.assertEqual(msg[1], f"{foolong}.")
        self.assertEqual(msg[2], f"    -> {fname}")
