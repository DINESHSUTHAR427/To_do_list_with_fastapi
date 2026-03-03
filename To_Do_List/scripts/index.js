

let token = "";

// ================= REGISTER =================

async function register() {
    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email: document.getElementById("reg_email").value,
                password: document.getElementById("reg_password").value
            })
            
        });
    
        const data = await response.json();
    
        if (response.ok) {
            alert("User created successfully! Now login.");
        } else {
            alert(JSON.stringify(data, null, 2));
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// ================= LOGIN =================

async function login() {
    try {
        const formData = new URLSearchParams();
        formData.append("username",
            document.getElementById("login_email").value);
        formData.append("password",
            document.getElementById("login_password").value);

        const response = await fetch("/login", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            token = data.access_token;
            document.getElementById("taskSection").classList.remove("hidden");
            document.getElementById("login_email").value = "";
            document.getElementById("login_password").value = "";
            loadTasks();
            alert("Login successful");
        } else {
            alert(data.detail || "Login failed");
        }
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// ================= LOAD TASKS =================

async function loadTasks() {
    try {
        const response = await fetch("/tasks", {
            headers: {
                "Authorization": "Bearer " + token
            }
        });
    
        const tasks = await response.json();
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";
    
        tasks.forEach(task => {
            const div = document.createElement("div");
            div.className = "task";
            div.innerHTML = `
                <span>${task.title}</span>
                <button onclick="deleteTask(${task.id})">Delete</button>
            `;
            taskList.appendChild(div);
        });
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// ================= CREATE TASK =================

async function createTask() {
    try {
        await fetch("/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify({
                title: document.getElementById("title").value,
                description: document.getElementById("description").value
            })
        });
    
        loadTasks();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// ================= DELETE TASK =================

async function deleteTask(taskId) {
    try {
        await fetch(`/tasks/${taskId}`, {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + token
            }
        });
    
        loadTasks();
    } catch (error) {
        alert("Error: " + error.message);
    }
}

// ================= LOGOUT =================

function logout() {
    token = "";
    document.getElementById("taskSection").classList.add("hidden");
    document.getElementById("taskList").innerHTML = "";
    alert("Logged out");
}