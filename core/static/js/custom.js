// Toggle du sidebar
document.addEventListener("DOMContentLoaded", () => {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('#sidebarToggle');

    toggleButton.addEventListener('click', () => {
        sidebar.classList.toggle('d-none'); // Cache ou montre le sidebar
    });
});

document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    const tableRows = document.querySelectorAll(".table tbody tr");

    searchInput.addEventListener("input", function () {
        const filter = searchInput.value.toLowerCase();

        tableRows.forEach(row => {
            const cells = Array.from(row.getElementsByTagName("td"));
            const rowText = cells.map(cell => cell.textContent.toLowerCase()).join(" ");
            row.style.display = rowText.includes(filter) ? "" : "none";
        });
    });
});
