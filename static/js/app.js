const form = document.getElementById("comicForm");

if (form) {
    form.addEventListener("submit", () => {
        const button = form.querySelector("button[type='submit']");
        if (button) {
            button.disabled = true;
            button.textContent = "✨ Creating your comic...";
        }
    });
}
