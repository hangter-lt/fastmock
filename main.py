import handle
import service


if __name__ == "__main__":
    for filename in handle.findAllFile("./api"):
        with open(filename, 'r', encoding='UTF-8') as f:
            a = handle.parsefile(f.readlines())
            service.content[a.uri] = a

    service.app.run()

