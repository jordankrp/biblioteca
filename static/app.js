// async function createResource() {
//     const resourceData = document.getElementById('inputResource').value;

//     const response = await fetch('http://localhost:8000/resources/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify({ data: resourceData }),
//     });

//     const newResource = await response.json();
//     displayResource(newResource);
// }

// function displayResource(resource) {
//     const listItem = document.createElement('li');
//     listItem.textContent = resource.data;
//     document.getElementById('resourceList').appendChild(listItem);
// }

async function login() {
    const userData = document.getElementById('inputResource').value;

    const response = await fetch('http://localhost:8000/users/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ data: userData }),
            });
    
    const loginResponse = await response.json();
    displayResource(loginResponse);
}

// Load existing resources when the page loads
window.onload = async function() {
    const response = await fetch('http://localhost:8000/books/');
    const resources = await response.json();
    resources.forEach(displayResource);
};