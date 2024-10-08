document.addEventListener('DOMContentLoaded', function() {
    const token = localStorage.getItem('token');
    if (token) {
        console.log("Token found");
        updateUIAfterLogin();
    } else {
        console.log("Token NOT found");
        fetchBooks();  // Fetch and display books even if not logged in
    }
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
            localStorage.setItem('username', username);
            alert('Login successful!');
            hideModal('loginModal');
            updateUIAfterLogin();
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

// Handle create book form submission
document.getElementById('createBookForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const token = localStorage.getItem('token'); // Get the token from local storage

    if (!token) {
        alert('You must be logged in to create a book.');
        return;
    }

    const title = document.getElementById('bookTitle').value;
    const author = document.getElementById('bookAuthor').value;
    const year = document.getElementById('bookYear').value;
    const summary = document.getElementById('bookSummary').value;

    const response = await fetch('http://localhost:8000/books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}` // Include the token in the Authorization header
        },
        body: JSON.stringify({ title, author, year, summary }),
    });

    if (response.ok) {
        const newBook = await response.json();
        displayBook(newBook);
        document.getElementById('createBookModal').style.display = 'none'; // Hide the modal after creation
    } else {
        alert('Failed to create book');
    }
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
    const createBookButton = document.getElementById('createBookButton');

    if (token) {
        loginButton.style.display = 'none';
        signupButton.style.display = 'none';
        currentUser.textContent = `Logged in as: ${username}`;
        currentUser.style.display = 'inline';
        logoutButton.style.display = 'inline';
        createBookButton.style.display = 'inline';
    } else {
        loginButton.style.display = 'inline';
        signupButton.style.display = 'inline';
        currentUser.style.display = 'none';
        logoutButton.style.display = 'none';
        createBookButton.style.display = 'none';
    }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    alert('Logged out successfully.');
    location.reload();  // Refresh the page to reset the UI
}

function showLogin() {
    document.getElementById('loginModal').style.display = 'block';
}

function showSignup() {
    document.getElementById('signupModal').style.display = 'block';
}

function showCreateBookForm() {
    document.getElementById('createBookModal').style.display = 'block';
}

function hideModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

function updateUIAfterLogin() {
    console.log('Updating UI after login');
    const username = localStorage.getItem('username');
    console.log("Username %s", username);
    if (username) {
        // Show the username and logout button
        document.getElementById('currentUser').textContent = `Welcome, ${username}`;
        document.getElementById('currentUser').style.display = 'inline';
        document.getElementById('logoutButton').style.display = 'inline';
        document.getElementById('loginButton').style.display = 'none';
        document.getElementById('signupButton').style.display = 'none';
        document.getElementById('createBookButton').style.display = 'inline';
    }
    fetchBooks();  // Fetch and display books
}

function displayBook(book) {
    const bookItem = document.createElement('li');
    bookItem.textContent = `${book.title} by ${book.author}, ${book.year}`;
    if (book.summary) {
        const summaryElement = document.createElement('p');
        summaryElement.textContent = `Summary: ${book.summary}`;
        bookItem.appendChild(summaryElement);
    }
    document.getElementById('books-list').appendChild(bookItem);
}