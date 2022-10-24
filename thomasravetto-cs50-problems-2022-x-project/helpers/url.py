def check_url():

    pl_input = input("Url: ")

    if len(pl_input) > 34:
        if pl_input[-35] == "=":
            print(pl_input[-34:])
            return 0
        print("invalid")
        return 1

    elif len(pl_input) == 34:
        if "=" not in pl_input:
            print(pl_input)
            return 0
        print("invalid")
        return 1

    elif len(pl_input) < 34:
        print("invalid")
        return 1

if __name__ == '__main__':
    check_url()