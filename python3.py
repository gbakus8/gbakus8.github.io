import os
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request = self.request.recv(1024).decode()
        if request.startswith("GET"):
            if request.split(" ")[1] == "/":
                self.send_index_page()
            elif request.split(" ")[1].endswith("jpg"):
                self.send_image_file(request.split(" ")[1].split("/")[1])
            elif request.split(" ")[1] == "/styles.css":
                self.send_css_file()
            elif request.split(" ")[1] == "/index.js":
                self.send_js_file()
            else:
                self.send_404_error()
        elif request.startswith("POST"):
            pass
        else:
            self.send_400_error()

    def send_400_error(self):
        self.request.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")

    def send_404_error(self):
        self.request.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

    def send_index_page(self):
        html_file = open("index.html", "rb").read()
        self.request.sendall(b"HTTP/1.1 200 OK\r\n")
        self.request.sendall(b"Content-Type: text/html\r\n")
        self.request.sendall(b"\r\n")
        self.request.sendall(html_file)

    def send_image_file(self, filename):
        image_file = open(f"img/{filename}", "rb").read()
        self.request.sendall(b"HTTP/1.1 200 OK\r\n")
        self.request.sendall(b"Content-Type: image/jpeg\r\n")
        self.request.sendall(b"\r\n")
        self.request.sendall(image_file)

    def send_css_file(self):
        css_file = open("styles.css", "rb").read()
        self.request.sendall(b"HTTP/1.1 200 OK\r\n")
        self.request.sendall(b"Content-Type: text/css\r\n")
        self.request.sendall(b"\r\n")
        self.request.sendall(css_file)

    def send_js_file(self):
        js_file = open("index.js", "rb").read()
        self.request.sendall(b"HTTP/1.1 200 OK\r\n")
        self.request.sendall(b"Content-Type: text/javascript\r\n")
        self.request.sendall(b"\r\n")
        self.request.sendall(js_file)

if __name__ == "__main__":
    with socketserver.TCPServer(("", 8080), MyTCPHandler) as server:
        server.serve_forever()
```

**styles.css**

```css
body {
  font-family: Arial, sans-serif;
  text-align: center;
}

#banner {
  width: 100%;
  height: 100px;
  background-image: url("catsdogsloversclubbanner.png");
  background-size: cover;
}

#gallery {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: repeat(4, 1fr);
}

#gallery img {
  max-width: 200px;
  max-height: 200px;
}

#photo {
  width: 100%;
  max-width: 1800px;
  max-height: 1800px;
}

.button {
  padding: 10px 20px;
  background-color: #333;
  color: #fff;
  text-decoration: none;
  border: none;
}
```

**index.html**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Cats & Dogs Lovers Club</title>
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <div id="banner"></div>
    <h1>Cats & Dogs Lovers Club</h1>
    <div id="gallery">
      {% for image in os.listdir("img") %}
      <a href="{{ image }}">
        <img src="{{ image }}" />
      </a>
      {% endfor %}
    </div>
    <script src="index.js"></script>
  </body>
</html>
```

**index.js**

```javascript
const galleryImages = document.querySelectorAll("#gallery img");
const photo = document.getElementById("photo");
const buttons = document.querySelectorAll(".button");

let currentIndex = 0;

function showImage(index) {
  photo.src = galleryImages[index].src;
  currentIndex = index;
  updateButtons();
}

function nextImage() {
  currentIndex += 1;
  if (currentIndex >= galleryImages.length) {
    currentIndex = 0;
  }
  showImage(currentIndex);
}

function previousImage() {
  currentIndex -= 1;
  if (currentIndex < 0) {
    currentIndex = galleryImages.length - 1;
  }
  showImage(currentIndex);
}

function updateButtons() {
  buttons[0].disabled = currentIndex === 0;
  buttons[1].disabled = currentIndex === galleryImages.length - 1;
}

galleryImages.forEach((image, index) => {
  image.addEventListener("click", () => {
    showImage(index);
  });
});

buttons[0].addEventListener("click", previousImage);
buttons[1].addEventListener("click", nextImage);