const form = document.getElementById('dreamForm');
const dreamList = document.getElementById('dreamList');

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  await fetch('/submit-dream', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });

  form.reset();
  loadDreams();
});

async function loadDreams() {
  const res = await fetch('/dreams');
  const dreams = await res.json();
  dreamList.innerHTML = dreams.map(d => `
    <div class="dream">
      <h3>${d.name} - ${d.date}</h3>
      <p>${d.description}</p>
    </div>
  `).join('');
}

// Load dreams on page load
loadDreams();
