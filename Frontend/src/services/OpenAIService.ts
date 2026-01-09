export interface AIChatMessage {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    timestamp: Date;
}

export interface AIResponseChunk {
    text: string;
    isComplete: boolean;
}

export const OpenAIService = {
    // Send a message to the AI via backend
    sendMessage: async (
        message: string,
        context: { name?: string; grade?: string; subject?: string; weakTopics?: string[] }
    ): Promise<string> => {
        try {
            const response = await fetch('/student/api/ask-ai', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: message,
                    studentName: context.name,
                    grade: context.grade || '7',
                    subject: context.subject || 'Math',
                    weakTopics: context.weakTopics || []
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch AI response');
            }

            const data = await response.json();
            return data.response;
        } catch (error) {
            console.error("AI Error", error);
            throw error;
        }
    },

    // Mock file analysis remains for now as backend doesn't support it yet
    analyzeFile: async (file: File): Promise<string> => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve("I've analyzed your file. It looks like a worksheet on Quadratic Equations. I see you made a mistake in Question 3 regarding the negative sign. Would you like me to explain?");
            }, 2000);
        });
    }
};

// Helper to generate realistic responses based on input
function generateMockResponse(message: string, context: any): string {
    const msg = message.toLowerCase();
    const userName = context?.name?.split(' ')[0] || 'Student';

    if (msg.includes('mistake') || msg.includes('wrong')) {
        return `Hi ${userName}, looking at your recent quiz, I see you're struggling with the sign conventions in the quadratic formula. Remember, when 'b' is negative, '-b' becomes positive. Let's try solving x² - 4x - 5 = 0 together. What should '-b' be here?`;
    }

    if (msg.includes('practice') || msg.includes('quiz')) {
        return `Great initiative, ${userName}! Since you're working on ${context?.weakTopic || 'Algebra'}, let's try a practice problem. \n\nSolve for x: 2x² + 5x - 3 = 0. \n\nTake your time, and let me know if you need a hint!`;
    }

    if (msg.includes('study') || msg.includes('next')) {
        return `Based on your progress, I recommend focusing on "Word Problems with Quadratics". You're great at the calculation part, but setting up the equation seems to be the tricky bit. Shall we breakdown a real-world example?`;
    }

    return `That's a great question, ${userName}. To understand this better, let's break it down into smaller steps. First, recall the fundamental concept of ${context?.subject || 'the topic'}. \n\nCan you tell me what you think the first step should be?`;
}
