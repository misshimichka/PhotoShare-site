import base64

f = open("static/img/anya1.jpg", mode="rb").read()
b64_encode = base64.b64encode(f)
b64_decode = base64.b64decode(b64_encode)
f1 = open("image.img", mode="wb")
f1.write(b64_decode)
f1.close()