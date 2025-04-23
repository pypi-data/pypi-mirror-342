from phystool.tags import Tags
import locale

def run_A() -> None:
    st = ["A", "E", "É", "C", "D", "B", "F"]
    print(sorted(st))
    print(locale.getlocale())
    locale.setlocale(locale.LC_COLLATE, "fr_CH.UTF-8")
    # print(locale.getlocale())
    # print(sorted(st))
    print(sorted(st, key=locale.strxfrm))


if __name__ == "__main__":
    run_A()
