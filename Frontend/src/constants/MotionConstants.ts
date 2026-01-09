import { Variants } from 'motion/react';

export const pageVariants: Variants = {
    initial: {
        opacity: 0,
        y: 20,
        filter: 'blur(10px)'
    },
    animate: {
        opacity: 1,
        y: 0,
        filter: 'blur(0px)',
        transition: {
            duration: 0.4,
            ease: [0.25, 0.46, 0.45, 0.94], // Smooth easing
            staggerChildren: 0.1
        }
    },
    exit: {
        opacity: 0,
        y: -20,
        filter: 'blur(10px)',
        transition: {
            duration: 0.3,
            ease: "easeIn"
        }
    }
};

export const buttonVariants: Variants = {
    hover: {
        y: -2,
        scale: 1.02,
        boxShadow: "0px 10px 20px rgba(0,0,0,0.1)",
        transition: { duration: 0.2 }
    },
    tap: {
        scale: 0.97,
        y: 0,
        transition: { duration: 0.1 }
    },
    loading: {
        opacity: 0.8,
        scale: 0.98,
        transition: { duration: 0.2 }
    }
};

export const cardVariants: Variants = {
    hidden: {
        opacity: 0,
        y: 20
    },
    visible: {
        opacity: 1,
        y: 0,
        transition: {
            duration: 0.5,
            ease: "easeOut"
        }
    },
    hover: {
        y: -5,
        boxShadow: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
        transition: { duration: 0.2 }
    }
};

export const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
        opacity: 1,
        transition: {
            staggerChildren: 0.1
        }
    }
};
