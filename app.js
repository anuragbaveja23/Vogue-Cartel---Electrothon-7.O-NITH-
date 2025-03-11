async function fetchPrice(store, priceElementId, linkElementId) {
    try {
        const response = await fetch(`/get-price?store=${store}`);
        const data = await response.json();

        document.getElementById(priceElementId).innerText = `₹${data.price}`;
        document.getElementById(linkElementId).href = data.link;
    } catch (error) {
        console.error(`Error fetching ${store} price:`, error);
        document.getElementById(priceElementId).innerText = "Unavailable";
    }
}

// Fetch and update prices
fetchPrice("amazon", "price-firstproduct", "https://www.amazon.in/Jordan-Mens-Sneaker-White-Black-sail/dp/B0CH1WTFHZ/");
fetchPrice("flipkart", "price-firstproduct", "https://www.flipkart.com/nike-full-force-low-sneakers-men/p/itm90e4293b6188a");
document.addEventListener("DOMContentLoaded", function () {
    fetchPrice("amazon", "price-firstproduct", "https://www.amazon.in/Jordan-Mens-Sneaker-White-Black-sail/dp/B0CH1WTFHZ/");
    fetchPrice("flipkart", "price-firstproduct", "https://www.flipkart.com/nike-full-force-low-sneakers-men/p/itm90e4293b6188a");
});

