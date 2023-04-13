from reset import lambda_handler as reset

def test():
    event = {
    }
    ret = reset(event, 0)
    print(f"return: {ret}")

def main():
    test()

if __name__ == "__main__":
    main()