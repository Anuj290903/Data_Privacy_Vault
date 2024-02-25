document.addEventListener('DOMContentLoaded', function() {
        fetch('http://127.0.0.1:8000/detokenize/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value,
        },
        body: JSON.stringify({
            "id": '1232',
            "data": {
                "Name": 'f5Wf5Ulm',
                "Password": 'f5Wf5Ulm',
            }
        }),
        credentials: 'same-origin',
    })
    .then(response => {
        if (!response.ok) {
            response.json();
            throw new Error('Failed to fetch. Status: ' + response.status + ' ' + response.text());
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.error('Fetch error:', error.message);
    });
});
