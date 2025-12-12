document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth Scroll for Prediction Button
    const predictNavBtn = document.querySelector('.cta-link');
    if (predictNavBtn) {
        predictNavBtn.addEventListener('click', function(e) {
            e.preventDefault();
            document.getElementById('prediction').scrollIntoView({ behavior: 'smooth' });
        });
    }

    // Tab Functionality
    const tabs = document.querySelectorAll('.tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.style.display = 'none');
            
            tab.classList.add('active');
            const targetId = tab.id.replace('Btn', '');
            document.getElementById(targetId).style.display = 'block';
        });
    });

    // Image Preview & Drag/Drop
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('imageInput');
    const imageContainer = document.getElementById('imageContainer');

    if (dropArea) {
        dropArea.addEventListener('click', () => fileInput.click());

        dropArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropArea.classList.add('drag-active');
        });

        dropArea.addEventListener('dragleave', () => {
            dropArea.classList.remove('drag-active');
        });

        dropArea.addEventListener('drop', (e) => {
            e.preventDefault();
            dropArea.classList.remove('drag-active');
            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                handleFiles(fileInput.files);
            }
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function() {
            handleFiles(this.files);
        });
    }

    function handleFiles(files) {
        if (files && files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                imageContainer.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
                // Reset prediction results on new image load
                const pResult = document.getElementById('predictionResult');
                if (pResult) pResult.innerHTML = '';
                document.getElementById('positive-card').style.display = 'none';
                document.getElementById('negative-card').style.display = 'none';
            }
            reader.readAsDataURL(files[0]);
        }
    }

    // Prediction Logic
    const predictBtn = document.getElementById('predictBtn');
    if (predictBtn) {
        predictBtn.addEventListener('click', predictImage);
    }

    function predictImage() {
        const formData = new FormData();
        // Check if fileInput has files
        if (!fileInput.files || !fileInput.files[0]) {
            alert("Please upload an image first.");
            return;
        }
        
        const imageFile = fileInput.files[0];
        const resultDiv = document.getElementById('predictionResult');
        
        const originalBtnText = predictBtn.innerHTML;
        predictBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Analyzing...';
        predictBtn.disabled = true;
        
        formData.append('image', imageFile);

        fetch('prediction', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
            }
        })
        .then(response => response.json())
        .then(data => {
            // Reset UI
            predictBtn.innerHTML = originalBtnText;
            predictBtn.disabled = false;
            
            const isNormal = data.prediction === "Normal Eye";
            const colorClass = isNormal ? "color: var(--success-color)" : "color: var(--accent-color)";
            
            resultDiv.innerHTML = `Prediction: <span style="${colorClass}">${data.prediction}</span>`;
            
            const posCard = document.getElementById('positive-card');
            const negCard = document.getElementById('negative-card');

            // If normal, show maintain healthy tips (negative-card for disease)
            // If disease, show action required (positive-card for disease)
            if (isNormal) {
                posCard.style.display = 'none';
                negCard.style.display = 'block';
            } else {
                posCard.style.display = 'block';
                negCard.style.display = 'none';
            }
            
            // Scroll to results
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        })
        .catch(error => {
            console.error('Error:', error);
            predictBtn.innerHTML = originalBtnText;
            predictBtn.disabled = false;
            alert("An error occurred during prediction.");
        });
    }

});
