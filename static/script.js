const form = document.getElementById('dreamForm');
const dreamList = document.getElementById('dreamList');

// Submit dream
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  if (form.dataset.id) {
    // Update existing dream
    await fetch(`/update-dream/${form.dataset.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    delete form.dataset.id;
  } else {
    // Add new dream
    await fetch('/submit-dream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
  }

  form.reset();
  loadDreams();
});

// Load all dreams
async function loadDreams() {
  const res = await fetch('/dreams');
  const dreams = await res.json();
  dreamList.innerHTML = dreams.map(d => `
    <div class="dream" data-id="${d.id}">
      <h3>${d.name} - ${d.date}</h3>
      <p>${d.description}</p>
      <button onclick="editDream(${d.id})">Edit</button>
      <button onclick="deleteDream(${d.id})">Delete</button>
    </div>
  `).join('');
}

// Delete a dream
async function deleteDream(id) {
  await fetch(`/delete-dream/${id}`, { method: 'DELETE' });
  loadDreams();
}

// Edit a dream
function editDream(id) {
  const dreamDiv = document.querySelector(`.dream[data-id='${id}']`);
  const name = dreamDiv.querySelector('h3').innerText.split(' - ')[0];
  const date = dreamDiv.querySelector('h3').innerText.split(' - ')[1];
  const description = dreamDiv.querySelector('p').innerText;

  form.elements['name'].value = name;
  form.elements['description'].value = description;
  form.elements['date'].value = date;

  form.dataset.id = id; // mark form for update
}

// Load dreams on page load
loadDreams();
const starsContainer = document.getElementById('stars');
const numStars = 100; // number of stars

for (let i = 0; i < numStars; i++) {
    const star = document.createElement('div');
    const size = Math.random() * 2 + 1; // 1px to 3px
    const duration = Math.random() * 3 + 2; // 2s to 5s animation
    const delay = Math.random() * 5; // random start delay

    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    star.style.background = '#fff';
    star.style.position = 'absolute';
    star.style.top = `${Math.random() * window.innerHeight}px`;
    star.style.left = `${Math.random() * window.innerWidth}px`;
    star.style.borderRadius = '50%';
    star.style.opacity = Math.random();
    star.style.animation = `glow ${duration}s infinite alternate`;
    star.style.animationDelay = `${delay}s`;

    starsContainer.appendChild(star);
}


// Twinkle animation
const style = document.createElement('style');
style.innerHTML = `
@keyframes twinkle {
    from { opacity: 0.2; }
    to { opacity: 1; }
}`;
document.head.appendChild(style);
