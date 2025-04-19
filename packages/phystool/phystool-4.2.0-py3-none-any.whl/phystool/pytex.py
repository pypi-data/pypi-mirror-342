import re
from logging import getLogger
from pathlib import Path
from typing import Generator
from math import pi, sqrt, exp, log2, log  # noqa: usablein pdb file
from math import sin, asin, cos, acos, tan, atan, degrees, radians  # noqa: usable in pdb file

logger = getLogger(__name__)


def sind(angle: float) -> float:
    return sin(radians(angle))


def asind(value: float) -> float:
    return degrees(asin(value))


def cosd(angle: float) -> float:
    return cos(radians(angle))


def acosd(value: float) -> float:
    return degrees(acos(value))


def tand(value: float) -> float:
    return tan(radians(value))


def atand(value: float) -> float:
    return degrees(atan(value))


def cot(value: float) -> float:
    return 1.0/tan(value)


def cotd(value: float) -> float:
    return 1.0/tan(radians(value))


def ln(value: float) -> float:
    return log(value)


class PyTex:
    PYCODE_PATTERN = r"\\begin{pycode}(\[.*\])?(.*)\\end{pycode}"
    CONSTANTS = {
        'G': (6.6743e-11, r"\newton\meter\squared\per\kilogram\squared"),
        'g': (9.81, r"\meter\per\second\squared"),
        'au': (1.495979e11, r"\meter"),   # astronomical unit
        'Ms': (1.98847e30, r"\kilogram"),  # solar mass
        'c': (299792458, r"\meter\per\second"),  # speed of light
        'h': (6.6260701e-34, r"\joule\second"),  # Plank constant
        'hbar': (1.054571817e-34, r"\joule\second"),  # Plank constant
        'me': (9.1093837015e-31, r"\kilogram"),       # electron mass
        'mn': (1.67492749804e-27, r"\kilogram"),  # neutron mass
        'mp': (1.67262192369e-27, r"\kilogram"),  # proton mass
        'me_amu': (5.4858e-4, r"\amu"),       # electron mass
        'mp_amu': (1.007276, r"\amu"),        # proton mass
        'mn_amu': (1.008665, r"\amu"),        # neutron mass
        'malpha': (4.001506, r"\amu"),    # sans électrons
        'm1H': (1.007825, r"\amu"),       # avec électrons
        'm2H': (2.014102, r"\amu"),       # avec électrons
        'm3H': (3.016049, r"\amu"),       # avec électrons
        'm3He': (3.016029, r"\amu"),      # avec électrons
        'm4He': (4.002603, r"\amu"),      # avec électrons
        'm8Be': (8.005305, r"\amu"),      # avec électrons
        'm42Ca': (41.958617, r"\amu"),    # avec électrons
        'm43Ca': (42.958766, r"\amu"),    # avec électrons
        'm88Sr': (87.905746, r"\amu"),    # avec électrons
        'm92Kr': (91.9250, r"\amu"),      # avec électrons
        'm136Xe': (135.90722, r"\amu"),   # avec électrons
        'm141Ba': (140.9141, r"\amu"),    # avec électrons
        'm206Pb': (205.974465, r"\amu"),  # avec électrons
        'm210Po': (209.982874, r"\amu"),  # avec électrons
        'm234Th': (234.043599, r"\amu"),  # avec électrons
        'm234Pa': (234.043305, r"\amu"),  # avec électrons
        'm235U': (235.043925, r"\amu"),   # avec électrons
        'm238U': (238.050786, r"\amu"),   # avec électrons
        'Na': (6.02214076e23, ""),
        'amu': (1.66053906660e-27, r"\kilogram"),  # amu != 1/Na even after the 2019 unit redefinition
        'kWh': (3600000, r"\joule"),  # kilowatt hour
        'amuc2': (931.49410242, r"\mega\electronvolt\per\amu"),  # conversion factor kg -> MeV
        'qe': (1.602176634e-19, r"\coulomb"),  # electron charge
        'a0': (5.29177210903e-11, r"\meter"),  # Bohr radius
        'k': (8.987551e9, r"\newton\meter\squared\per\coulomb\squared"),
        'R': (8.31446261815324, r"\joule\per\kelvin\per\mole"),
        'kB': (1.380649e-23, r"\joule\per\kelvin"),
        'mu0': (pi*4e-7, r"\tesla\meter\per\ampere"),
        'ceau': (4185, r"\joule\per\kilogram\per\kelvin"),
        'cglace': (2060, r"\joule\per\kilogram\per\kelvin"),
        'Lveau': (2300000, r"\joule\per\kilogram"),
        'Lfeau': (330000, r"\joule\per\kilogram"),
        'atm': (101325, r"\pascal"),
        'MTerre': (5.9722e24, r"\kilogram"),
        'RTerre': (6371000, r"\meter"),
    }
    CONVERSION = {
        'amu2MeV': lambda x: (x*PyTex.CONSTANTS['amuc2'][0], r"\mega\electronvolt"),
        'amu2eV': lambda x: (x*PyTex.CONSTANTS['amuc2'][0]*1e6, r"\electronvolt"),
        'amu2J': lambda x: (x*PyTex.CONSTANTS['amuc2'][0]*PyTex.CONSTANTS['qe'][0], r"\joule"),
        'amu2kg': lambda x: (x/PyTex.CONSTANTS['Na'][0]/1000, r"\kilogram"),
        'amu2g': lambda x: (x/PyTex.CONSTANTS['Na'][0], r"\gram"),
        'eV2J': lambda x: (x*PyTex.CONSTANTS['qe'][0], r"\joule"),
        'MeV2J': lambda x: (1e6*x*PyTex.CONSTANTS['qe'][0], r"\joule"),
        'kmh2ms': lambda x: (x/3.6, r"\meter\per\second"),
        'ms2kmh': lambda x: (x*3.6, r"\kilo\meter\per\hour"),
        'C2K': lambda x: (x+273, r"\kelvin"),
        'K2C': lambda x: (x-273, r"\celsius"),
        'atm2Pa': lambda x: (x*PyTex.CONSTANTS['atm'][0], r"\pascal"),
        'Pa2atm': lambda x: (x/PyTex.CONSTANTS['atm'][0], r"\atm"),
        'mmHg2Pa': lambda x: (x*133.22, r"\pascal"),
        'Pa2mmHg': lambda x: (x/133.22, r"\mmHg"),
        'torr2Pa': lambda x: (x*PyTex.CONSTANTS['atm'][0]/760, r"\pascal"),
        'Pa2torr': lambda x: (x/PyTex.CONSTANTS['atm'][0]*760, r"\torr"),
        'seconde2annee': lambda x: (x/31556952, r"\an"),
        'cal2J': lambda x: (x*PyTex.CONSTANTS['ceau'][0]/1000, r"\joule"),
        'J2cal': lambda x: (x/PyTex.CONSTANTS['ceau'][0]*1000, r"\cal"),
        'J2kWh': lambda x: (x/PyTex.CONSTANTS['kWh'][0], r"\kWh"),
        'kWh2J': lambda x: (x*PyTex.CONSTANTS['kWh'][0], r"\joule"),
        'au2m': lambda x: (x*PyTex.CONSTANTS['au'][0], r"\meter"),
        'm2au': lambda x: (x/PyTex.CONSTANTS['au'][0], r"\astronomicalunit"),
    }

    class OutputVariableParsingError(Exception):
        ERRNO_MESSAGE = (10, 'Variable parsing error')

        def __init__(self, arg: tuple[str, str, str]):
            variable = "|".join(arg)
            super().__init__(variable)
            self.msg = f"Error when parsing variable '#{variable}'"

    class OutputOptionsParsingError(Exception):
        ERRNO_MESSAGE = (20, 'Option parsing error')

        def __init__(self, arg: tuple[str, str, str]):
            variable = "|".join(arg)
            super().__init__(variable)
            self.msg = f"Error when parsing option '#{variable}'"

    class UnitConversionError(Exception):
        ERRNO_MESSAGE = (30, 'Unit conversion error')

        def __init__(self, key: str, unit: str):
            super().__init__(f"{key=}, {unit=}")
            self.msg = f"Error when converting '{key}' into '{unit}'"

    def __init__(self, tex_file: Path):
        self.tex_file = tex_file
        self._successful_run = False
        self._messages: list[str] = []

    def _parse_file(self) -> bool:
        try:
            with self.tex_file.open() as tf:
                if match := re.search(
                    self.PYCODE_PATTERN,
                    tf.read(),
                    re.DOTALL
                ):
                    self.constants = match.group(1)
                    match_list = match.group(2).split('\n')[1:-1]
                    ntab = match_list[0].count('\t')
                    # FIXME: doesn't properly catch identation error (in pycode
                    # start newline with random text, no %)
                    self.match = [
                        m[ntab:] for m in match_list
                        # empty lines and LaTex comments
                        if (m.strip() and m[ntab] != '%')
                    ]
                    return True
                else:
                    logger.debug(f"No 'pycode' in {self.tex_file.stem}")
        except FileNotFoundError:
            logger.error(f"{self.tex_file} not found")
            self.tex_file.with_suffix(".pty").unlink(missing_ok=True)
        except IndexError as xcpt:
            logger.error(f"Identation error in {self.tex_file}", xcpt)
            logger.error(
                "\n".join(
                    [
                        f"{i}: \"{m}\"" for i, m in enumerate(match_list)
                        if (m.strip() and len(m) <= ntab)
                    ]
                )
            )

        return False

    def _get_constants(self) -> tuple[str, list[tuple[str, str, str]]]:
        init_block = ""
        out_block = []
        if self.constants:
            for cst_str in self.constants[1:-1].split(","):
                cst_str = cst_str.strip()
                notout = cst_str.startswith("*")
                if notout:
                    cst_str = cst_str[1:]
                try:
                    cst_variable, cst_opt = cst_str.split("|")
                except ValueError:
                    cst_variable = cst_str
                    cst_opt = ""

                try:
                    cst_value, cst_unit = self.CONSTANTS[cst_variable]
                except KeyError:
                    logger.warning(f"Undefined constant '{cst_variable}' in {self.tex_file.stem}")
                    logger.info("Available constants are: " + " ".join(self.CONSTANTS.keys()))
                    continue

                if "_" in cst_variable:
                    cst_name, cst_version = cst_variable.split('_')
                else:
                    cst_name = cst_variable

                init_block += f"{cst_name} = {cst_value}\n"
                if not notout:
                    out_block.append((cst_name, cst_unit, cst_opt))

        return init_block, out_block

    def _parse_init_command(self, command: str) -> str:
        if "|" in command:
            if "=" not in command:
                raise self.UnitConversionError(command, "")

            key, command = command.split("=")
            commands = command.split("|")
            value = commands.pop(0).strip()
            command = ""
            for c in reversed(commands):
                command += f"self.CONVERSION['{c}']("
            command = f"{key} = {command}{value}" + ")[0]"*len(commands)

        return command + "\n"

    def _parse_options(self, options: str) -> None:
        self._siopts = ""
        self._fstring = ""
        for option in options.split(','):
            if ':' in option:
                self._fstring = option
            elif option == 'prefix':
                self._siopts += "prefix-mode=combine-exponent,"
                self._siopts += "exponent-mode=engineering,"
            elif option:
                self._siopts += option + ","

    def _parse_out_block(self, current_command: tuple[str, str, str]) -> str:
        try:
            key_value_str, self._units, options = current_command
        except ValueError:
            raise self.OutputOptionsParsingError(current_command)

        if not key_value_str:
            raise self.OutputOptionsParsingError(current_command)

        self._parse_options(options)
        key_value = key_value_str.split('=')
        self.key = key_value[0].strip()
        if len(key_value) == 1:
            return self.key

        if len(key_value) == 2:
            if value := key_value[1].strip():
                return value

        raise self.OutputVariableParsingError(current_command)

    def _generate_tex_string(self, value: float) -> tuple[str, str]:
        if self._units and not self._units.startswith("\\"):
            try:
                value, self._units = self.CONVERSION[self._units](value)
            except KeyError:
                raise self.UnitConversionError(self.key, self._units)

        if self._fstring:
            value = eval("f'{{{}{}}}'".format(value, self._fstring))
            if value[0:2] == '1e':
                value = value[1:]

        if self._units:
            if self.key == "mu0":
                self._siopts += ",input-digits = 0123456789\\pi"
                value = "4\\pi e-7"
            if self._siopts:
                siunitx = f"\\qty[{self._siopts}]{{{value}}}{{{self._units}}}"
            else:
                siunitx = f"\\qty{{{value}}}{{{self._units}}}"
        else:
            if self._siopts:
                siunitx = f"\\num[{self._siopts}]{{{value}}}"
            else:
                siunitx = f"\\num{{{value}}}"

        logger.debug(f"{self.key}={value} % {self._units}")
        return self.key, siunitx

    def _execute_commands(
        self,
        init_block: str,
        out_block: list[tuple[str, str, str]],
        extra_block: list[str]
    ) -> Generator[tuple[str, str], None, None]:
        """Should not define any variable to avoid conflict with pycode"""
        try:
            exec(init_block)
        except SyntaxError as xcpt:
            logger.error(f"SyntaxError: %s in {self.tex_file.stem}", xcpt)
            return
        except Exception as xcpt:
            logger.error(f"Exception: %s in {self.tex_file.stem}", xcpt)
            return

        self._successful_run = True
        for block_command in out_block:
            try:
                yield self._generate_tex_string(
                    eval(self._parse_out_block(block_command))
                )
            except (
                self.OutputOptionsParsingError,
                self.OutputVariableParsingError,
                self.UnitConversionError
            ) as xcpt:
                # needs to come before except ValueError to be correctly caught
                self._successful_run = False
                logger.error(xcpt.msg)
            except ValueError as xcpt:
                self._successful_run = False
                logger.error(f"ValueError: %s in {self.tex_file.stem}", xcpt)
            except NameError as xcpt:
                self._successful_run = False
                logger.error(f"NameError: %s in {self.tex_file.stem}", xcpt)

        for extra_command in extra_block:
            eval(extra_command)

    def _get_python_result(self) -> Generator[tuple[str, str], None, None]:
        init_block, out_block = self._get_constants()
        extra_block = []
        for current_command in self.match:
            if current_command[0] != '#':
                init_block += self._parse_init_command(current_command)
            elif '|' in current_command:
                out_block.append(current_command[1:].split('|'))
            else:
                extra_block.append(current_command[1:])

        return self._execute_commands(init_block, out_block, extra_block)

    def _get_pytex(self) -> str:
        return (
            "\\ExplSyntaxOn\n"
            "\\prop_gset_from_keyval:Nn \\g_pdb_pytotex_prop {{\n"
            "{}\n"
            "}}\n"
            "\\ExplSyntaxOff"
        ).format(
            ",\n".join(
                f"\t{{{key}}} = {{{siunitx}}}"
                for key, siunitx in self._get_python_result()
            )
        )

    def run(self) -> bool:
        pty_file = self.tex_file.with_suffix(".pty")
        if (
            self._parse_file()
            and (
                not pty_file.exists()
                or pty_file.stat().st_mtime < self.tex_file.stat().st_mtime
            )
        ):
            with pty_file.open('w') as out:
                out.write(self._get_pytex())
        return self._successful_run

    def get_messages(self) -> str:
        if not self._messages:
            return ""

        tmp = f"%% PYTEX: {self.tex_file.stem}\n"
        for message in self._messages:
            tmp += f"%% {message}\n"
        return tmp
