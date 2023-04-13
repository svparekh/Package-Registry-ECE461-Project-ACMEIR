from get_package_by_name import lambda_handler as get_package_by_name
from _fake_upload_package import lambda_handler as upload

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
    except Exception as exception:
        print("caught ", exception)

    event = {
        "metadata": {
            "Name": "test",
            "Version": "2.0.0",
            "ID": "998"
        },
        "data": {
            "Content": "Hello different version",
            "URL": "something",
            "JSProgram": "string"
        }
    }

    try:
        ret = upload(event, 0)
        print(f"return: {ret}")
    except Exception as exception:
        print("caught ", exception)

def test1():
    event = {
        'path': "/package/byName/test"
    }
    ret = get_package_by_name(event, 0)
    print(f"return: {ret}")


def test2():
    try:
        event = {
            'path': "/package/byName/thisPackageDoesNotExist"
        }
        ret = get_package_by_name(event, 0)
        print(f"return: {ret}")
    except Exception as exception:
        print("caught ",exception)


def main():
    settup()
    test1()
    test2()

if __name__ == "__main__":
    main()