document.addEventListener('DOMContentLoaded', function() {
    // Menu animation initialization
    function menuAnimation(){
        const menuOpen = document.getElementById('menu-open');
        const menuClose = document.getElementById('menu-close');
        const navPart2 = document.getElementById('nav-part2');
    
        menuOpen.addEventListener('click', function() {
            navPart2.style.display = 'flex';
            setTimeout(() => {
                navPart2.style.right = '0';
            }, 10); // Small delay to allow the display to be set before transitioning
            menuOpen.style.display = 'none';
            menuClose.style.display = 'block';
        });
    
        menuClose.addEventListener('click', function() {
            navPart2.style.right = '-100%';
            setTimeout(() => {
                navPart2.style.display = 'none';
            }, 300); // Match the transition duration in the CSS
            menuOpen.style.display = 'block';
            menuClose.style.display = 'none';
        });
    }

    // Image preview initialization
    function imagepreview(){
        document.getElementById('file').addEventListener('change', function(event) {
            const imagePreview = document.getElementById('imagePreview');
            imagePreview.innerHTML = ''; // Clear previous preview

            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    imagePreview.appendChild(img);
                }
                reader.readAsDataURL(file);
            }
        });
    }

    // Initialize functions
    menuAnimation();
    imagepreview();
});

