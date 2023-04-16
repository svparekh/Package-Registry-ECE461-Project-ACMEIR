from upload_package import lambda_handler as upload_package

def test1():
    event = {
        "metadata": {
            "Name": "test",
            "Version": "1.0.0",
            "ID": "999"
        },
        "data": {
            "Content": "Hello world",
            "URL": "something",
            "JSProgram": "string"
        }
    }

    try:
        ret = upload_package(event, 0)
        print(f"return: {ret}")
    except Exception as exception:
        print(exception)
        pass


def test2():
    test1()
    test1()

def test3():
    event = {
        "metadata": {
            "Name": "test3",
            "Version": "1.0.0",
            "ID": "999"
        },
        "data": {
            "Content": "Hello world",
            "URL": "something",
            "JSProgram": "string"
        }
    }

    try:
        ret = upload_package(event, 0)
        print(f"return: {ret}")
    except:
        print("caught exception")

def test4():
    event = {
        "metadata": {
            "Name": "test",
            "Version": "2.0.0",
            "ID": "999"
        },
        "data": {
            "Content": "Hello world",
            "URL": "something",
            "JSProgram": "string"
        }
    }

    try:
        ret = upload_package(event, 0)
        print(f"return: {ret}")
    except:
        print("caught exception")

def main():
    # test1()
    test2()
    test3()
    test4()



if __name__ == "__main__":
    main()