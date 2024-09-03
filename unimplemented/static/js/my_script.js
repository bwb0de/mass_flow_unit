function rolar_ate_o_elemento(element, duration) {
    const targetPosition = element.offsetTop;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    const startTime = performance.now();

    function scrollAnimation(currentTime) {
        const timeElapsed = currentTime - startTime;
        const newPosition = easeInOutQuart(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, newPosition);

        if (timeElapsed < duration) {
        window.requestAnimationFrame(scrollAnimation);
        }
    }

    function easeInOutQuart(t, b, c, d) {
        t /= d/2;
        if (t < 1) return c/2*t*t*t*t + b;
        t -= 2;
        return -c/2 * (t*t*t*t - 2) + b;
    }

    window.requestAnimationFrame(scrollAnimation);
}


function removerNumeros(str) {
    return str.replace(/\d+/g, '');
  }

