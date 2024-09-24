const { ipcRenderer } = require('electron');


let storyTellerWindow

function goHome() {
    ipcRenderer.send('open-page', 'HomeScreen.html');
}

// document.getElementById('generateBtn').addEventListener('click', () => {
//     ipcRenderer.send('generate-story');
//     window.location = 'storyTeller.html'; // Change the location to the new HTML file
// });

const axios = require('axios');

// Assuming mainWindow is your window displaying storyTeller.html


mainWindow.webContents.openDevTools();

document.addEventListener('DOMContentLoaded', () => {
    const generateButtons = document.querySelectorAll('.generate-button');
    generateButtons.forEach(button => {
        button.addEventListener('click', () => {
            ipcRenderer.send('generate-story-request');
        });
    });
});

ipcRenderer.on('story-update', (event, data) => {
    displayStory(data.story);
    // displayImages(data.images);
});

function generateStory() {
    //window.location.href = './loading.html'; // Redirect to the loading screen immediately after button click

    fetch('http://127.0.0.1:5000/generate_story_and_images', { method: 'GET' })
      .then(response => response.json())
      .then(data => {
        // Store data in localStorage or pass through a query parameter
        localStorage.setItem('images', JSON.stringify(data.images)); // Assuming the images are paths
        localStorage.setItem('storyText', JSON.stringify(data.story));
        window.location.href = './storyTeller.html'; // Redirect to storyTeller.html after fetching
      })
      .catch(error => {
        console.error('Error:', error);
        alert('Failed to generate story. Please try again.');
      });
  }

function displayStory(story) {
    const storyElement = document.getElementById('story');
    storyElement.textContent = story;
}

function displayImages(images) {
    const imageContainer = document.getElementById('image-container');
    imageContainer.innerHTML = ''; // Clear previous images
    images.forEach(imageUrl => {
        const img = new Element('img');
        img.src = imageUrl;
        imageContainer.appendChild(img);
    });
}