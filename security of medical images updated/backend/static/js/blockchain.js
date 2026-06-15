document.addEventListener('DOMContentLoaded', () => {
    const storeBtn = document.getElementById('store-image-btn');
    const viewBtn = document.getElementById('view-stored-images-btn');
    const backBtn = document.getElementById('back-btn');
    const watermarkingBtn = document.getElementById('go-to-watermarking-btn');

    const storeSection = document.getElementById('store-image-section');
    const transSection = document.getElementById('transaction-section');
    const storedSection = document.getElementById('stored-images-section');

    const imageElem = document.getElementById('stored-image');
    const hashElem = document.getElementById('transaction-hash');
    const container = document.getElementById('stored-images-container');

    storeBtn.addEventListener('click', () => {
        fetch('/blockchain/store', { method: 'POST' })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                storeSection.style.display = 'none';
                transSection.style.display = 'block';
                imageElem.src = data.stored_image_url;
                hashElem.textContent = data.transaction_hash;
            } else {
                alert("Failed to store image!");
            }
        });
    });

    viewBtn.addEventListener('click', () => {
        fetch('/blockchain/stored_images')
        .then(res => res.json())
        .then(images => {
            transSection.style.display = 'none';
            storedSection.style.display = 'block';
            container.innerHTML = '';
            images.forEach(url => {
                const img = document.createElement('img');
                img.src = url;
                img.style.margin = '10px';
                container.appendChild(img);
            });
        });
    });

    backBtn.addEventListener('click', () => {
        storedSection.style.display = 'none';
        storeSection.style.display = 'block';
    });

    watermarkingBtn.addEventListener('click', () => {
        window.location.href = '/watermarking';
    });
});

