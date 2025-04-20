from oxapy import templating
from oxapy import static_file, get, post, HttpServer, Status, Router
from oxapy import serializer


@get("/")
def index_page(request):
    return templating.render(request, "index.html.j2", {"name": "word"})


@get("/login")
def login_page(request):
    return templating.render(request, "login.html.j2")


@post("/upload-file")
def upload_file(request):
    if file := request.files().get("file"):
        file.save(f"media/{file.name}")
    return Status.OK


class CredSerializer(serializer.Serializer):
    username = serializer.CharField()
    password = serializer.CharField()


@post("/login")
def login_form(request):
    cred = CredSerializer(request)

    try:
        cred.validate()
    except Exception as e:
        return str(e), Status.OK

    username = cred.validate_data["username"]
    password = cred.validate_data["password"]

    if username == "admin" and password == "password":
        return "Login success", Status.OK
    return templating.render(
        request, "components/error_mesage.html.j2", {"error_message": "Login failed"}
    )


def logger(request, next, **kwargs):
    print(f"{request.method} {request.uri}")
    return next(request, **kwargs)


router = Router()
router.middleware(logger)
router.routes([index_page, login_page, login_form, upload_file])
router.route(static_file("./static", "static"))


server = HttpServer(("127.0.0.1", 8080))
server.attach(router)
server.template(templating.Template("./templates/**/*.html.j2"))

if __name__ == "__main__":
    server.run()
