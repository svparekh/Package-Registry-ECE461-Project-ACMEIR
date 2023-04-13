from delete_package import lambda_handler as delete
from upload_package import lambda_handler as upload

def settup():
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
        ret = upload(event, 0)
        print(f"return: {ret}")
    except:
        print("caught exception")

def test1():
    event = {
        'path': "/package/999"
    }
    ret = delete(event, 0)
    print(f"return: {ret}")
    # try:
    #     ret = lambda_handler(event, 0)
    #     print(f"return: {ret}")
    # except:
    #     print("caught exception")


def test2():
    try:
        test1()
    except:
        print("caught exception")


def main():
    settup()
    test1()
    test2()

if __name__ == "__main__":
    main()