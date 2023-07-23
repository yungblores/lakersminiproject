// Define the function that should be run on scroll and on page load
function checkScrollAndPath() {
  var logo = document.querySelector(".logo img");
  var header = document.querySelector("header");
  
  if (window.location.pathname.endsWith('index.html')) {
    document.querySelector('header').classList.add('fixed-header');
  }
  
  if (window.pageYOffset > 0) {
    logo.style.width = "150px";
    header.style.backgroundColor = "rgba(85, 37, 131, 0.8)";
  } else {
    logo.style.width = "200px";
    header.style.backgroundColor = "rgba(85, 37, 131, 0.0)";
  }
}

// Attach the function to the scroll event
window.addEventListener("scroll", checkScrollAndPath);

// Run the function when the page loads
window.addEventListener("load", checkScrollAndPath);







// Roster table sorting

document.addEventListener("DOMContentLoaded", () => {
  const tableHeaders = document.querySelectorAll("#rosterTable th");
  let sortAscending = true;
  let columnIndex = 0;

  const sortTable = () => {
    const table = document.getElementById("rosterTable");
    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll(":scope > tr"));

    rows.sort((a, b) => {
      const aData = a.querySelector(":scope > td:nth-child(" + (columnIndex + 1) + ")").textContent.trim();
      const bData = b.querySelector(":scope > td:nth-child(" + (columnIndex + 1) + ")").textContent.trim();

      if (columnIndex === 1) { // Sort based on last name for "Name" column
        const aLastName = aData.split(" ").pop();
        const bLastName = bData.split(" ").pop();
        return sortAscending ? aLastName.localeCompare(bLastName) : bLastName.localeCompare(aLastName);
      } else {
        return sortAscending ? aData.localeCompare(bData, undefined, { numeric: true }) : bData.localeCompare(aData, undefined, { numeric: true });
      }
    });

    // Clear the table body
    while (tbody.firstChild) {
      tbody.removeChild(tbody.firstChild);
    }

    // Append sorted rows back to the table body
    rows.forEach((row) => {
      tbody.appendChild(row);
    });

    // Remove all existing arrows
    tableHeaders.forEach((header) => {
      header.textContent = header.textContent.replace(" ↓", "").replace(" ↑", "");
    });

    // Add arrow to sorted column header
    tableHeaders[columnIndex].textContent += sortAscending ? " ↓" : " ↑";

    // Toggle the sort order for the next click
    sortAscending = !sortAscending;
  };

  tableHeaders.forEach((header, index) => {
    header.addEventListener("click", () => {
      if (columnIndex === index) {
        sortTable();
      } else {
        columnIndex = index;
        sortTable();
      }
    });
  });
});












  // Player Description below
  
  var playerCards = document.getElementsByClassName("player-image");
  var activePlayerCard = null;
  var activeCard = null;
  
  for (let i = 0; i < playerCards.length; i++) {
    let playerCard = playerCards[i];
    let playerDescription = playerCard.getElementsByClassName("card")[0];
    let exitBtns = playerDescription.getElementsByClassName("exit-button");
  
    playerCard.addEventListener('mouseover', function () {
      if (activePlayerCard === null) {
        playerDescription.style.display = 'block';
      }
    });
  
    playerCard.addEventListener('mouseout', function () {
      if (activePlayerCard === null) {
        playerDescription.style.display = 'none';
      }
    });
  
    playerCard.addEventListener('click', function (event) {
      if (event.target.tagName === 'IMG') {
        if (activePlayerCard !== null && activePlayerCard !== playerCard) {
          activeCard.style.display = 'none';
          activeCard.classList.remove('is-flipped');
        }
        playerDescription.style.display = 'block';
        activePlayerCard = playerCard;
        activeCard = playerDescription;
      }
    });
  
    playerDescription.addEventListener('click', function (event) {
      if (event.target.tagName !== 'BUTTON') { // Prevents flipping when the exit button is clicked
        playerDescription.classList.toggle('is-flipped');
      }
    });
  
    // Add event listeners to each exit button
    for (let j = 0; j < exitBtns.length; j++) {
      exitBtns[j].addEventListener('click', function () {
        playerDescription.style.display = 'none';
        playerDescription.classList.remove('is-flipped');
        activePlayerCard = null;
        activeCard = null;
      });
    }
  }
  
  
  
  function adjustFontSize() {
    let elements = document.getElementsByClassName("lakergreatname");
  
    for (let i = 0; i < elements.length; i++) {
      let element = elements[i];
      
      // Initial font size (you can adjust this as needed)
      let fontSize = 16; 
  
      // Create a temporary span to measure the text width
      let span = document.createElement("span");
      span.style.fontSize = fontSize + "px";
      span.style.visibility = "hidden"; 
      span.style.whiteSpace = "nowrap";
      span.textContent = element.textContent;
  
      document.body.appendChild(span);
  
      // Reduce the font size until the text fits the element width
      while (span.offsetWidth > element.offsetWidth && fontSize > 0) {
        fontSize -= 0.5;
        span.style.fontSize = fontSize + "px";
      }
  
      document.body.removeChild(span);
  
      // Set the adjusted font size to the element
      element.style.fontSize = fontSize + "px";
    }
  }
  
  // Call the function when the page has loaded
  window.onload = adjustFontSize;
  
  // Call the function when the window is resized
  window.onresize = adjustFontSize;
  


  document.getElementById('searchBar').addEventListener('input', function(e) {
    const searchString = e.target.value.toLowerCase();
  
    const allPlayers = document.querySelectorAll('.lakergreat');
    allPlayers.forEach(function(player) {
      const playerName = player.querySelector('.lakergreatname').textContent.toLowerCase();
  
      // Hide players that do not match search string
      if (playerName.indexOf(searchString) === -1) {
        player.style.display = 'none';
      } else {
        player.style.display = 'flex';
      }
    });
  
    // Get the remaining visible players
    const visiblePlayers = [...allPlayers].filter(player => player.style.display === 'flex');
  
    // If there is only one player left, center it
    if (visiblePlayers.length === 1) {
      visiblePlayers[0].style.gridColumn = "3 / span 1";
    } else {
      allPlayers.forEach(function(player) {
        player.style.gridColumn = "";
      });
    }
  });

// Open player's wikipedia page in a new tab
  document.addEventListener("DOMContentLoaded", function(){
    let playerElements = document.getElementsByClassName("lakergreat");
  
    for(let i = 0; i < playerElements.length; i++){
      playerElements[i].addEventListener("click", function(){
        window.open(this.getAttribute('data-url'), "_blank");
      });
    }
  });
  



  // Carousel handling of google chrome
  window.onload = function() {
    const iframes = document.querySelectorAll('iframe');
    
    iframes.forEach((iframe) => {
        iframe.addEventListener('load', function() {
            setTimeout(() => {
                iframe.style.visibility = 'hidden';
                iframe.offsetHeight; // Force reflow
                iframe.style.visibility = '';
            }, 0);
        });
    });
};



  


  
  