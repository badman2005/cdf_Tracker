var map = L.map('map').setView([-13.1339, 27.8493], 6);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

fetch('/api/projects')
    .then(response => response.json())
    .then(data => {
        const list = document.getElementById('project-list');
        list.innerHTML = ""; 

        data.forEach(p => {
            const marker = L.marker([p.lat, p.lng]).addTo(map);
            // Added image to map popup
            marker.bindPopup(`
                <img src="${p.image_url}" style="width:100%; border-radius:5px; margin-bottom:5px;">
                <br><b>${p.title}</b><br>${p.constituency}
            `);

            const card = document.createElement('div');
            card.className = "p-4 bg-white border rounded-xl mb-3 shadow-sm hover:border-green-600 cursor-pointer transition-all";
            
            // This displays the inspection photo at the top of the card
            card.innerHTML = `
                <img src="${p.image_url}" class="w-full h-32 object-cover rounded-lg mb-2" alt="Site Inspection">
                <span class="text-[10px] font-bold text-green-700 uppercase">${p.category}</span>
                <h4 class="font-bold text-sm text-gray-800">${p.title}</h4>
                <p class="text-xs text-gray-500">${p.constituency}</p>
            `;
            
            card.onclick = () => {
                map.flyTo([p.lat, p.lng], 14);
                marker.openPopup();
            };
            
            list.appendChild(card);
        });
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById('project-list').innerHTML = "<p class='p-4 text-red-500'>Error loading transparency data.</p>";
    });