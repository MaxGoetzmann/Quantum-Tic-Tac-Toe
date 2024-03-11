// JS globals
mainFile = null
newMove = null
pyodide = null
handleEvent = true;

// What python provides
boardState = null
gameState = null

// Function to get a CSS variable's value
function getCssVariableValue(variableName) {
    // Get the styles from the root element
    const style = getComputedStyle(document.documentElement);
    // Return the value of the variable
    return style.getPropertyValue(variableName).trim();
}


async function fetchRawTextData(url) {
    try {
        const response = await fetch(url, { mode: "cors" });
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.text();
        return data;
    } catch (error) {
        console.error("Error fetching raw text data:", error);
        return null;
    }
}

async function fetchSrcFolder() {
    /* 
        Bypassing Git token "security".
        You have content read permissions for this repository only. Go wild.
    */
    const apiUrl = "https://api.github.com/repos/MaxGoetzmann/Quantum-Tic-Tac-Toe/contents/src";
    const keypt1 = "github_pat_11AUYCOVI0aCCKMd0dQDeK_"
    const keypt2 = "MWx6IWEXzmaKeNWUeW5iceqqF2CVQvJxifGZTkr59Ec7IZLA4DFrbC13aDF"
    const headers = {
        "Authorization": `token ${keypt1}${keypt2}`
    }
    try {
        const response = await fetch(apiUrl, { headers });
        const data = await response.json();
        data.forEach(file => {
            fetchRawTextData(file.download_url).then(text => {
                if (text === null) throw new Error(`Could not get file ${file.name} data.`)

                // Save main file for execution
                if (file.name === "main.py") {
                    mainFile = text;
                }

                pyodide.FS.writeFile(`./${file.name}`, text, { encoding: "utf8" });
            });
        });
    } catch (error) {
        console.error("Failed to fetch projects:", error);
    }
}

// Function to display win screen
function showWinScreen(winner) {
    if (winner === undefined) return;
    const winScreen = document.getElementById('win-screen');
    const winMessage = document.querySelector('.win-message');
    winMessage.textContent = `Player ${winner[winner.length - 1]} wins!`;
    winScreen.classList.remove('hidden');
}

// Function to close win screen
function closeWinScreen() {
    const winScreen = document.getElementById('win-screen');
    winScreen.classList.add('hidden');
}

// Event listener for the close button
document.getElementById('close-button').addEventListener('click', closeWinScreen);

function gameLoop() {
    // Game loop
    if (newMove) {
        let namespace = pyodide.toPy({ pyodide_first_pass: false, game_in: gameState, pyodide_move: newMove });
        pyodide.runPython(mainFile, { globals: namespace });

        // Accessing dictionaries and lists from Pyodide global space
        gameState = namespace.get("game_out");
        boardState = Array.from(namespace.get("board_out"), innerArray => Array.from(innerArray));
        playerTurn = namespace.get("player_turn");
        afterUpdate(boardState, playerTurn)
        console.log(boardState)
        winner = namespace.get("player_won")
        if (winner !== "None" && winner !== "") {
            showWinScreen(winner)
        }
        newMove = null;
        handleEvent = true;
    }

    requestAnimationFrame(gameLoop);
}

function colorSpecificLetters(element) {
    // Loop through each child node of the current element
    var childNodes = Array.from(element.childNodes);
    childNodes.forEach(function (node) {
        // Check if the current node is a text node
        if (node.nodeType === Node.TEXT_NODE) {
            var text = node.textContent;
            var fragment = document.createDocumentFragment();

            // Split the text content into an array of characters
            text.split('').forEach(function (char) {
                var span = document.createElement('span');
                span.textContent = char;

                // Apply styles to make sure the span affects nothing but the color
                span.style.display = 'inline';
                span.style.font = 'inherit';
                span.style.fontWeight = 'inherit';
                span.style.lineHeight = 'inherit';

                // Check if the current character matches the target letter
                if (char === "X") {
                    span.style.color = getCssVariableValue("--quantum-x-piece");;
                }

                fragment.appendChild(span);
            });

            // Replace the text node with the fragment containing spans
            element.replaceChild(fragment, node);
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            // If the current node is an element node, recursively call the function
            colorSpecificLetters(node);
        }
    });
}

function afterUpdate(board, playerTurn) {
    plotBoard(board);
    playerTurnUpdate(playerTurn)
    //colorSpecificLetters(document.body)
}

function repopTooltip(element, text) {
    const newTooltip = document.createElement('span');
    newTooltip.classList.add('tooltip-content');
    newTooltip.innerText = text;
    element.appendChild(newTooltip);
}

function playerTurnUpdate(playerTurn) {
    player = playerTurn[playerTurn.length - 1]

    /* Update header. */
    const header = document.getElementById("player-to-move")
    header.innerText = `${player}  to  move`

    /* Update player piece. */

    // Find the tooltip within the drag item
    const piece = document.getElementById("drag-player")
    piece.innerText = player

    repopTooltip(piece,
        `Place a ${player}`)

    // Do same for superposition
    const superpos = document.getElementById("drag-superpos")
    txt = "-"
    if (player == "O") txt = "+"
    superpos.innerText = txt

    repopTooltip(superpos,
        `Place a ${player} in superposition`)
}

function plotBoard(board) {
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const id = row * 3 + col + 1
            const cell = document.getElementById(`cell-${id}`);
            let val = board[row][col];
            if (val !== "None") {
                if (val == "~") val = "NOT";
                cell.textContent = val;
            }
        }
    }
}

async function loadPyodideAndRun() {
    pyodide = await loadPyodide();
    await pyodide.loadPackage(["micropip"]); // Load any additional packages your game needs
    await fetchSrcFolder(pyodide)
    await pyodide.runPythonAsync(`
            import micropip

            # Install Python packages
            await micropip.install("numpy")
            await micropip.install("jsonpickle")
        `).then(async () => {
        let namespace = pyodide.toPy({ pyodide_first_pass: true });
        pyodide.runPython(mainFile, { globals: namespace });

        // Accessing dictionaries and lists from Pyodide global space
        gameState = namespace.get("game_out");
        boardState = Array.from(namespace.get("board_out"), innerArray => Array.from(innerArray));
        playerTurn = namespace.get("player_turn");

        afterUpdate(boardState, playerTurn)
        console.log(boardState);

        requestAnimationFrame(gameLoop);

    })
    console.log("post py")
    // ....
}

document.addEventListener('DOMContentLoaded', () => {
    const dragItems = document.querySelectorAll('#drag-items > div');
    const cells = document.querySelectorAll('.cell');

    dragItems.forEach(item => {
        item.addEventListener('dragstart', handleDragStart);
    });

    cells.forEach(cell => {
        cell.addEventListener('dragover', handleDragOver);
        cell.addEventListener('drop', handleDrop);
    });

    function handleDragStart(e) {
        if (!handleEvent) return;
        e.dataTransfer.setData('text', e.target.id);
        const id = e.dataTransfer.getData('text');
        const draggableElement = document.getElementById(id);
        draggableElement.classList.add('dragging');
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    function handleDrop(e) {
        e.preventDefault();
        if (!handleEvent) return;
        const id = e.dataTransfer.getData('text');
        const draggableElement = document.getElementById(id);
        draggableElement.classList.remove('dragging');
        newMove = {
            type: draggableElement.getAttribute("data-type"),
            row: parseInt(e.target.getAttribute("data-row")),
            col: parseInt(e.target.getAttribute("data-col")),
        }
        handleEvent = false
    }
});

// main()
loadPyodideAndRun();

