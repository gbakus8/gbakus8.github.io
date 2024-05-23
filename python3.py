#!/usr/local/bin/python3

import os
import http.server
import socketserver

PORT = 8000

# Chemin du répertoire contenant les images
img_dir = 'img'

# Template HTML pour la galerie principale
gallery_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery</title>
    <style>
        .thumbnail {
            max-width: 200px;
            display: inline-block;
            margin: 5px;
            cursor: pointer;
        }

        #myModal {
            display: none;
            position: fixed;
            z-index: 1;
            padding-top: 100px;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgb(0,0,0);
            background-color: rgba(0,0,0,0.9);
        }

        .modal-content {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 700px;
        }

        #caption {
            margin: auto;
            display: block;
            width: 80%;
            max-width: 700px;
            text-align: center;
            color: #ccc;
            padding: 10px 0;
            height: 150px;
        }

        .close {
            position: absolute;
            top: 15px;
            right: 35px;
            color: #f1f1f1;
            font-size: 40px;
            font-weight: bold;
            transition: 0.3s;
        }

        .close:hover,
        .close:focus {
            color: #bbb;
            text-decoration: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Gallery</h1>
    <div id="thumbnails">
        <!-- Thumbnails will be inserted here -->
    </div>

    <!-- The Modal -->
    <div id="myModal" class="modal">
        <span class="close">&times;</span>
        <img class="modal-content" id="modalImg">
        <div id="caption"></div>
    </div>

    <script>
        // JavaScript to handle thumbnail clicks
        var thumbnails = document.querySelectorAll('.thumbnail');
        thumbnails.forEach(function(thumbnail) {
            thumbnail.addEventListener('click', function() {
                var modal = document.getElementById("myModal");
                var modalImg = document.getElementById("modalImg");
                var captionText = document.getElementById("caption");

                modal.style.display = "block";
                modalImg.src = this.src;
                captionText.innerHTML = this.alt;
            });
        });

        // Close the modal
        var closeBtn = document.getElementsByClassName("close")[0];
        closeBtn.onclick = function() {
            var modal = document.getElementById("myModal");
            modal.style.display = "none";
        }
    </script>
</body>
</html>
"""

# Handler pour servir les fichiers et gérer les routes
class GalleryHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='.', **kwargs)

    def list_image_files(self):
        image_files = []
        for filename in os.listdir(img_dir):
            if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
                image_files.append(filename)
        return image_files

    def list_image_thumbnails(self):
        thumbnails = ''
        image_files = self.list_image_files()
        for filename in image_files:
            thumbnails += f'<img class="thumbnail" src="/img/{filename}" alt="{filename}">'
        return thumbnails

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(gallery_template.encode('utf-8'))
            self.wfile.write(self.list_image_thumbnails().encode('utf-8'))
        else:
            super().do_GET()

# Lance le serveur
with socketserver.TCPServer(("", PORT), GalleryHandler) as httpd:
    print("Serveur démarré sur le port", PORT)
    httpd.serve_forever()
