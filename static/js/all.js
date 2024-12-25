
// Image paths ka array
const images = [
    'static/img/h1.jpg',
    'static/img/h2.jpg',
    'static/img/h3.jpg',
    'static/img/h4.jpg',
    'static/img/h5.jpg',
    'static/img/h6.jpg',
    'static/img/h7.jpg',
    'static/img/h9.jpg',
    'static/img/h10.jpg',
    'static/img/h11.jpg',
    'static/img/h12.jpg',
    'static/img/h13.jpg',
    'static/img/h14.jpg',
    'static/img/h15.jpg',
    'static/img/h16.jpg',
    'static/img/h17.jpg',
    'static/img/h18.jpg',
    'static/img/h19.jpg',
    'static/img/h20.jpg',
    'static/img/h21.jpg',
    'static/img/h22.jpg',
    'static/img/h23.jpg',
    'static/img/h24.jpg',
    'static/img/h25.jpg',
    'static/img/h26.jpg',
    'static/img/h27.jpg',
];

// Fallback placeholder image URL
const placeholderImage = 'https://picsum.photos/1920/1080'; // Use an online placeholder URL

// Random background set karne ka function with fallback
function setRandomBackground() {
    const randomImage = images[Math.floor(Math.random() * images.length)];
    const heroSection = document.getElementById("heroSection");

    // Create a new Image object to test loading
    const img = new Image();
    img.src = randomImage;

    // When the image loads successfully
    img.onload = () => {
        heroSection.style.backgroundImage = `url(${randomImage})`;
    };

    // If the image fails to load, use the placeholder
    img.onerror = () => {
        heroSection.style.backgroundImage = `url(${placeholderImage})`;
    };
}

// Call the function on page load
window.onload = setRandomBackground;



// stars
document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const colors = ["#ff7e5f", "#feb47b", "#86a8e7", "#91eae4"];
    let index = 0;

    setInterval(() => {
        body.style.background = `linear-gradient(120deg, ${colors[index]}, ${colors[(index + 1) % colors.length]})`;
        index = (index + 1) % colors.length;
    }, 5000);

    const starField = document.createElement('div');
    starField.classList.add('star-field');
    body.appendChild(starField);

    function createStar() {
        const star = document.createElement('div');
        star.classList.add('star');
        const size = Math.random() * 3 + 1;
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.top = `${Math.random() * 100}%`;
        star.style.left = `${Math.random() * 100}%`;
        star.style.animationDuration = `${Math.random() * 3 + 2}s`;
        starField.appendChild(star);
    }

    for (let i = 0; i < 100; i++) {
        createStar();
    }
});



// Tooltip
document.addEventListener('DOMContentLoaded', function () {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
})





// users js
// Toggle visibility of the floating search box
function toggleSearchBox(event) {
    event.preventDefault
    const form = document.getElementById("floatingSearchBox");

    // Toggle the visibility of the floating search box
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block"; // Show search box
    } else {
        form.style.display = "none"; // Hide search box
    }
    event.stopPropagation();
}

document.getElementById('searchButton').addEventListener('click', toggleSearchBox);


// Function to show the appropriate input field based on selected filter
function showAppropriateInput() {
    // Hide all input fields initially
    document.getElementById('name_field').style.display = 'none';
    document.getElementById('status_field').style.display = 'none';
    document.getElementById('date_field').style.display = 'none';
    document.getElementById('location_field').style.display = 'none';

    // Get the selected filter value
    var filter = document.getElementById('filter_by').value;

    // Show the corresponding input field
    if (filter === 'service_name' || filter === 'customer_name') {
        document.getElementById('name_field').style.display = 'block';
    } else if (filter === 'status') {
        document.getElementById('status_field').style.display = 'block';
    } else if (filter === 'date') {
        document.getElementById('date_field').style.display = 'block';
    } else if (filter === 'location') {
        document.getElementById('location_field').style.display = 'block';
    }
}

// Prepare the search query based on selected filter and input
function prepareSearchQuery(event) {
    event.preventDefault(); // Prevent default form submission

    // Get the selected filter
    var filter = document.getElementById('filter_by').value;

    // Map filter to corresponding input field's value
    var searchValue = '';
    if (filter === 'service_name' || filter === 'customer_name') {
        searchValue = document.getElementById('name_input').value.trim();
    } else if (filter === 'status') {
        searchValue = document.getElementById('status_input').value.trim();
    } else if (filter === 'date') {
        searchValue = document.getElementById('date_input').value.trim();
    } else if (filter === 'location') {
        searchValue = document.getElementById('location_input').value.trim();
    }

    // Validate input
    if (searchValue === '') {
        alert("Please enter a valid search query.");
        return false; // Stop form submission
    }

    // Set the hidden input field value
    document.getElementById('final_search_query').value = searchValue;

    // Allow form submission
    event.target.submit();
}

// Enable the submit button when user inputs something in the field
function enableSubmitOnInput() {
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('input', function () {
            var submitButton = document.getElementById('submitBtn');
            if (this.value.trim() !== "") {
                submitButton.style.display = 'inline-block'; // Show the submit button
            } else {
                submitButton.style.display = 'none'; // Hide the submit button if input is empty
            }
        });
    });
}

// Run enableSubmitOnInput after the DOM is loaded
document.addEventListener('DOMContentLoaded', enableSubmitOnInput);



// Detect if a click is outside the floating search container
document.addEventListener('click', function (event) {
    const floatingSearch = document.getElementById('floatingSearchBox');
    const searchButton = document.getElementById('searchButton');

    // Only close the floating search if the click is outside the box and and also on the icon
    if (!floatingSearch.contains(event.target) && event.target !== searchButton) {
        floatingSearch.style.display = 'none'; // Close the floating search box
    }
});

// Optionally, add a listener to open the search container
document.getElementById('searchButton').addEventListener('click', function (event) {
    const floatingSearch = document.getElementById('floatingSearchBox');
    floatingSearch.style.display = 'block'; // Open the floating search
    event.stopPropagation(); // Prevent the event from triggering the document click listener
});

// date select 
function toggleDateInput(id) {
    const dateOption = document.getElementById("dateOption" + id).value;
    const customDate = document.getElementById("customDate" + id);
    if (dateOption === "default") {
        customDate.disabled = true;
        customDate.value = ""; // Clear custom input
    } else {
        customDate.disabled = false;
    }
}
