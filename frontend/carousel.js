// Carousel
const rootStyles = getComputedStyle(document.documentElement);
const itemWidth = parseInt(rootStyles.getPropertyValue('--day-width'));

function scrollCarousel(direction) {
    const carousel = document.getElementById('carousel');
    
    // Scroll the carousel by one item width in the given direction
    carousel.scrollBy({
      left: direction * itemWidth, // Adjusts the scroll position
      behavior: 'smooth' // Smooth scroll
    });
}

function autoScrollToToday() {

    // Delay Execution by 1 second
    setTimeout(() => {
            const carousel = document.getElementById('carousel');
            const today = new Date().getDate();
            carousel.scrollTo({
                left: itemWidth * (today - 1),
                behavior: 'smooth'
            });    
        },
        5000    // Timeout milliseconds
    );

}