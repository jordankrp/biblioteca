document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    fetchBooks();
});

// Handle login form submission
document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    const loginData = new URLSearchParams();
    loginData.append('username', username);
    loginData.append('password', password);

    fetch('http://localhost:8000/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: loginData.toString()
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.detail || "Login failed"); });
        }
        return response.json();
    })
    .then(data => {
        if (data.access_token) {
            // Save the token in local storage (for future authenticated requests)
            localStorage.setItem('token', data.access_token);
            alert('Login successful!');
            // Close the modal
            hideModal('loginModal');
        } else {
            alert('Login failed: ' + (data.detail || 'Unknown error'));
        }
    })
    .catch(error => console.error('Error logging in:', error));
});

// Handle signup form submission
document.getElementById('signupForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;

    const signupData = { email, password };

    fetch('http://localhost:8000/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(signupData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.id) {
            alert('Signup successful! You can now log in.');
            // Close the modal
            hideModal('signupModal');
        } else {
            alert('Signup failed: ' + (data.detail || 'Unknown error'));
        }
    })
    .catch(error => console.error('Error signing up:', error));
});

function fetchBooks() {
    fetch('http://localhost:8000/books')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            
            const booksList = document.getElementById('books-list');
            booksList.innerHTML = '';

            data.forEach(bookData => {
                const { Book: book, average_rating, number_of_ratings } = bookData;
                const listItem = document.createElement('li');
                listItem.textContent = `${book.title} by ${book.author} - Average Rating: ${average_rating} (${number_of_ratings} ratings)`;
                booksList.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error fetching books:', error));
}

function checkAuth() {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    const loginButton = document.getElementById('loginButton');
    const signupButton = document.getElementById('signupButton');
    const currentUser = document.getElementById('currentUser');
    const logoutButton = document.getElementById('logoutButton');

    if (token) {
        loginButton.style.display = 'none';
        signupButton.style.display = 'none';
        currentUser.textContent = `Logged in as: ${username}`;
        currentUser.style.display = 'inline';
        logoutButton.style.display = 'inline';
    } else {
        loginButton.style.display = 'inline';
        signupButton.style.display = 'inline';
        currentUser.style.display = 'none';
        logoutButton.style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    alert('Logged out successfully.');
    checkAuth();
}

function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function showSignup() {
    document.getElementById('signupModal').style.display = 'block';
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}