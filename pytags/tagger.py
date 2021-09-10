import pytags.cmdline
import pytags.mgr


def main():
    mgr = pytags.mgr.Mgr()
    pytags.cmdline.parse(mgr)


if __name__ == "__main__":
    main()
