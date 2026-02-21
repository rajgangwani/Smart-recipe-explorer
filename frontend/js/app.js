const API = import.meta.env.VITE_API_URL;


// ===============================
// TOAST
// ===============================

function showToast(message, isError = false) {
    const toast = document.getElementById("toast");
    toast.textContent = message;
    toast.style.background = isError ? "#ef4444" : "#10b981";
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 3000);
}


// ===============================
// INITIAL LOAD
// ===============================

document.addEventListener("DOMContentLoaded", () => {
    loadRecipes();

    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.addEventListener("keydown", function (e) {
            if (e.key === "Enter") {
                searchRecipes();
            }
        });
    }
});


// ===============================
// ADD RECIPE
// ===============================

async function addRecipe() {
    try {
        const response = await fetch(`${API}/recipes`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                name: document.getElementById("name").value,
                ingredients: document.getElementById("ingredients").value,
                instructions: document.getElementById("instructions").value,
                category: document.getElementById("category").value,
                cooking_time: parseInt(document.getElementById("time").value)
            })
        });

        if (!response.ok) throw new Error();

        showToast("Recipe Added Successfully!");
        loadRecipes();

    } catch (error) {
        showToast("Error adding recipe", true);
    }
}


// ===============================
// BUILD QUERY STRING
// ===============================

function buildQuery() {
    const search = document.getElementById("searchInput")?.value.trim();
    const category = document.getElementById("categoryFilter")?.value;
    const max_time = document.getElementById("timeInput")?.value;
    const sort_by = document.getElementById("sortFilter")?.value;

    const params = new URLSearchParams();

    if (search) params.append("search", search);
    if (category) params.append("category", category);
    if (max_time) params.append("max_time", max_time);
    if (sort_by) params.append("sort_by", sort_by);

    return params.toString();
}


// ===============================
// LOAD RECIPES (WITH FILTERS)
// ===============================

async function loadRecipes() {
    try {
        const query = buildQuery();
        const url = query ? `${API}/recipes?${query}` : `${API}/recipes`;

        const response = await fetch(url);

        if (!response.ok) throw new Error();

        const data = await response.json();

        renderRecipes(data);
        updateResultCount(data.length);

    } catch (error) {
        showToast("Failed to load recipes", true);
    }
}


// ===============================
// SEARCH BUTTON CLICK
// ===============================

function searchRecipes() {
    loadRecipes();

    document.getElementById("recipeGrid")
        .scrollIntoView({ behavior: "smooth" });
}


// ===============================
// CLEAR SEARCH + FILTERS
// ===============================

function clearSearch() {
    document.getElementById("searchInput").value = "";
    if (document.getElementById("categoryFilter"))
        document.getElementById("categoryFilter").value = "";
    if (document.getElementById("timeInput"))
        document.getElementById("timeInput").value = "";
    if (document.getElementById("sortFilter"))
        document.getElementById("sortFilter").value = "";

    loadRecipes();
}


// ===============================
// UPDATE RESULT COUNT
// ===============================

function updateResultCount(count) {
    const resultCount = document.getElementById("resultCount");
    if (resultCount) {
        resultCount.textContent =
            `${count} recipe${count !== 1 ? "s" : ""} found`;
    }
}


// ===============================
// RENDER RECIPES
// ===============================

function renderRecipes(data) {
    const grid = document.getElementById("recipeGrid");
    const emptyState = document.getElementById("emptyState");

    grid.innerHTML = "";

    if (!data || data.length === 0) {
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");

    data.forEach(recipe => {
        const card = document.createElement("div");
        card.className = "recipe-card";

        card.innerHTML = `
            <h3>${recipe.name}</h3>
            <p><strong>Category:</strong> ${recipe.category}</p>
            <p><strong>Time:</strong> ${recipe.cooking_time} mins</p>
            <p><strong>Ingredients:</strong> ${recipe.ingredients}</p>
            <div style="margin-top:10px; display:flex; gap:10px;">
                <button class="secondary-btn"
                    onclick="deleteRecipe(${recipe.id})">
                    Delete
                </button>
            </div>
        `;

        grid.appendChild(card);
    });
}


// ===============================
// DELETE RECIPE
// ===============================

async function deleteRecipe(id) {
    try {
        const response = await fetch(`${API}/recipes/${id}`, {
            method: "DELETE"
        });

        if (!response.ok) throw new Error();

        showToast("Recipe Deleted");
        loadRecipes();

    } catch (error) {
        showToast("Failed to delete recipe", true);
    }
}


// ===============================
// AI GENERATOR
// ===============================

async function generateAI() {
    const input = document.getElementById("aiIngredients");
    const messages = document.getElementById("aiMessages");

    const userText = input.value.trim();
    if (!userText) return;

    // Add user bubble
    const userMsg = document.createElement("div");
    userMsg.className = "ai-message user-msg";
    userMsg.innerText = userText;
    messages.appendChild(userMsg);

    input.value = "";

    // Add loading bubble
    const loadingMsg = document.createElement("div");
    loadingMsg.className = "ai-message bot-msg";
    loadingMsg.innerText = "Typing...";
    messages.appendChild(loadingMsg);

    messages.scrollTop = messages.scrollHeight;

    try {
        const response = await fetch(`${API}/ai/suggest`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ingredients: userText
            })
        });

        if (!response.ok) throw new Error("AI error");

        const data = await response.json();

        loadingMsg.remove();

        const botMsg = document.createElement("div");
        botMsg.className = "ai-message bot-msg";
        botMsg.innerHTML = data.suggestion.replace(/\n/g, "<br>");

        messages.appendChild(botMsg);
        messages.scrollTop = messages.scrollHeight;

    } catch (error) {
        loadingMsg.innerText = "AI service unavailable.";
    }
}
