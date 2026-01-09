import { motion } from 'motion/react';
import { ReactNode } from 'react';
import { pageVariants } from '../constants/MotionConstants';

interface PageTransitionProps {
    children: ReactNode;
    className?: string;
}

export function PageTransition({ children, className = "" }: PageTransitionProps) {
    return (
        <motion.div
            initial="initial"
            animate="animate"
            exit="exit"
            variants={pageVariants}
            className={`w-full ${className}`}
        >
            {children}
        </motion.div>
    );
}
