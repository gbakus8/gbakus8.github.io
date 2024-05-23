const galleryContainer = document.querySelector('.gallery');

// Function to fetch images from the "img" directory
function fetchImages() {
    // Assume images are stored in the "img" directory
    const directory = 'img/';
    // Fetch images
    // Code to fetch images and create thumbnails dynamically
}

// Function to open photo in larger view
function openPhoto(photoSrc) {
    // Code to display photo in larger view
}

// Function to navigate to previous or next photo
function navigatePhoto(direction) {
    // Code to navigate to previous or next photo
}

// Event listener for clicking on thumbnail
galleryContainer.addEventListener('click', function(event) {
    if (event.target.classList.contains('thumbnail')) {
        const photoSrc = event.target.dataset.src;
        openPhoto(photoSrc);
    }
});

// Event listener for navigation buttons
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('prev-photo')) {
        navigatePhoto('prev');
    } else if (event.target.classList.contains('next-photo')) {
        navigatePhoto('next');
    } else if (event.target.classList.contains('back-to-gallery')) {
        // Code to go back to the gallery
    }
});

// Initialize gallery
fetchImages();
