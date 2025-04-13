
window.onload = function() {
    const image = document.getElementById("background-preview");
    const pointsDataElement = document.getElementById("points-data");
    const points = JSON.parse(pointsDataElement.innerText);

    // Draw existing points
    points.forEach(point => {
        addMarker(point.x, point.y);
    });

    // Event listener for the image to add new points
    image.addEventListener('click', function (event) {
        const rect = image.getBoundingClientRect();
    
        const clickX = event.clientX - rect.left;
        const clickY = event.clientY - rect.top;
    
        const relativeX = Math.round((clickX / rect.width) * 1000);
        const relativeY = Math.round((clickY / rect.height) * 1000);
        addMarker(relativeX, relativeY);
        savePoint(relativeX, relativeY);
    });

    // Function to add a marker to the canvas
    function addMarker(x, y) {
        const container = document.getElementById("preview-container");
    
        const marker = document.createElement("div");
        marker.classList.add("point-marker");
    
        const percentX = (x / 1000) * 100;
        const percentY = (y / 1000) * 100;
    
        marker.style.left = percentX + "%";
        marker.style.top = percentY + "%";
    
        container.appendChild(marker);
    }

    // Function to save point to the server or database
    function savePoint(pointX, pointY) {
        const csrfToken = document.querySelector('[name=csrf-token]').content;
        
        const dataToSend = {
            x: pointX,
            y: pointY
        };
    
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(dataToSend)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Saved successfully!', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
};
