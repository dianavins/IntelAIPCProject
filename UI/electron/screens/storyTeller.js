document.addEventListener('DOMContentLoaded', function() {
    const images = JSON.parse(localStorage.getItem('images')); // Assume images are paths like 'img1.png'
    const storyText = JSON.parse(localStorage.getItem('storyText')); // Assume text is an array of sentences
    let currentIndex = 0;

    function updateContent() {
        document.getElementById('story-image').src = images[currentIndex];
        document.getElementById('story-text').textContent = storyText[currentIndex];
    }

    window.navigate = function(direction) {
        if (direction === 'next' && currentIndex < images.length - 1) {
            currentIndex++;
            updateContent();
        } else if (direction === 'prev' && currentIndex > 0) {
            currentIndex--;
            updateContent();
        }
    }

    updateContent(); // Initial update
});
