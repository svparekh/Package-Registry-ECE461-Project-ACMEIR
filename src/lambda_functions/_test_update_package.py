from update_package import lambda_handler as update
from _fake_upload_package import lambda_handler as upload
from delete_package_by_name import lambda_handler as delete_by_name

def settup():
    event = {
        'path': "/package/byName/test"
    }
    ret = delete_by_name(event, 0)
    print(f"setup del_by_name: {ret}")
    
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
        print(f"setup upload: {ret}")
    except Exception as exception:
        print(f"setup upload: {exception}")

def test1():
    event = {
        "metadata": {
            "Name": "test",
            "Version": "1.0.0",
            "ID": "999"
        },
        "data": {
            "Content": "This is now new content",
            "URL": "This is different too",
            "JSProgram": "string"
        }
    }
    ret = update(event, 0)
    print(f"return: {ret}")

def test2():
    event = {
        "metadata": {
            "Name": "test",
            "Version": "2.0.0",
            "ID": "999"
        },
        "data": {
            "Content": "This shouldn't be in database",
            "URL": "This shouldn't be in database",
            "JSProgram": "string"
        }
    }
    try:
        ret = update(event, 0)
        print(f"return: {ret}")
    except Exception as exception:
        print(exception)

def test3():
    event = {
        "metadata": {
            "Name": "test3",
            "Version": "1.0.0",
            "ID": "25"
        },
        "data": {
            "Content": "This shouldn't be in database",
            "URL": "This shouldn't be in database",
            "JSProgram": "string"
        }
    }
    try:
        ret = update(event, 0)
        print(f"return: {ret}")
    except Exception as exception:
        print(exception)

def test4():
    event = {
        "metadata": {
            "Name": "test",
            "Version": "1.0.0",
            "ID": "995"
        },
        "data": {
            "Content": "This shouldn't be in database",
            "URL": "This shouldn't be in database",
            "JSProgram": "string"
        }
    }
    try:
        ret = update(event, 0)
        print(f"return: {ret}")
    except Exception as exception:
        print(exception)

def main():
    settup()
    test1()
    test2()
    test3()
    test4()

if __name__ == "__main__":
    main()