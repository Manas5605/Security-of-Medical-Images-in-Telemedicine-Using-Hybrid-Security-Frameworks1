document.getElementById("encryptButton").addEventListener("click", function () {
    fetch('/encryption/apply_encryption', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("dnaEncoded").value = data.dna_encoded;
        document.getElementById("encryptedImage").src = data.encrypted_image;
        document.getElementById("encryptedHistogram").src = data.encrypted_histogram;
        document.getElementById("encryptionResults").classList.remove('hidden');
        document.getElementById("storeBlockchainButton").classList.remove('hidden');
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById("storeBlockchainButton").addEventListener("click", function () {
    fetch('/blockchain/store', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/blockchain";
        } else {
            alert("Failed to store in blockchain.");
        }
    })
    .catch(error => console.error('Error:', error));
});
