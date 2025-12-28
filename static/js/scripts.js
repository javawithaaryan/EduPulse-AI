document.addEventListener('DOMContentLoaded', () => {
    // Scroll Reveal Intersection Observer
    const revealCallback = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    };

    const revealObserver = new IntersectionObserver(revealCallback, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    const revealElements = document.querySelectorAll('.reveal, .reveal-left');
    revealElements.forEach(el => revealObserver.observe(el));

    // Click Ripple Effect
    document.addEventListener('click', (e) => {
        const target = e.target.closest('.btn-primary, .btn-outline, .btn-ripple');
        if (!target) return;

        const ripple = document.createElement('span');
        ripple.classList.add('ripple');

        const rect = target.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = `${size}px`;
        ripple.style.left = `${x}px`;
        ripple.style.top = `${y}px`;

        target.appendChild(ripple);

        setTimeout(() => {
            ripple.remove();
        }, 600);
    });
});
