export const getCaptchaToken = (): string | null => {
    const win = window as unknown as {
        __captchaToken?: string;
        turnstileToken?: string;
    };

    return win.__captchaToken || win.turnstileToken || null;
};
