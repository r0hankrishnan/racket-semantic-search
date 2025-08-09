const mockData = [
      {
        name: "Wilson Pro Staff 97",
        brand: "Wilson",
        price: "$249",
        rating: "4.7",
        image: "https://img.tennis-warehouse.com/watermark/rs.php?path=BARO98-1.jpg&nw=455"
      },
      {
        name: "Babolat Pure Drive",
        brand: "Babolat",
        price: "$219",
        rating: "4.6",
        image: "https://img.tennis-warehouse.com/watermark/rs.php?path=BARO-1.jpg&nw=455"
      },
      {
        name: "Head Radical MP",
        brand: "Head",
        price: "$199",
        rating: "4.5",
        image: "https://img.tennis-warehouse.com/watermark/rs.php?path=BABOOA-1.jpg&nw=455"
      },
      {
        name: "Yonex EZONE 98",
        brand: "Yonex",
        price: "$239",
        rating: "4.8",
        image: "https://img.tennis-warehouse.com/watermark/rs.php?path=BABOAP-1.jpg&nw=455"
      }
    ];

function mockSearch() {
    const results = document.getElementById('results');
    results.innerHTML = '';
    mockData.forEach(r => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
        <img src="${r.image}" alt="${r.name}">
        <h3>${r.name}</h3>
        <p>${r.brand} – Rating: ${r.rating} ⭐</p>
        <p class="price">${r.price}</p>
    `;
    results.appendChild(card);
    });
}