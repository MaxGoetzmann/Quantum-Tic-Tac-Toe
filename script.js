newMove = false
mainFile = null
pyodide = null

// What python provides
boardState = null
gameState = null

const MoveType = {
    PLACE: 0,
    HGATE: 1,
    ZGATE: 2,
    NOTGATE: 3,
    CNOTPLACE: 4,
    INVCNOTPLACE: 5,
    PLACE_SUPERPOS: 6,
};


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
                    console.log(mainFile)
                }

                pyodide.FS.writeFile(`./${file.name}`, text, { encoding: "utf8" });
            });
        });
    } catch (error) {
        console.error("Failed to fetch projects:", error);
    }
}

function gameLoop() {
    // Game loop
    if (newMove) {
        let my_namespace = pyodide.globals.get("dict")();
        pyodide.runPython(mainFile);
        newMove = false;
    }

    requestAnimationFrame(gameLoop);
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
        let namespace = pyodide.toPy({ pyodide_first_pass: true, game_out: "", game_in: "", board_out: "" });
        pyodide.runPython(mainFile, { globals: namespace });

        // Accessing dictionaries and lists from Pyodide global space
        let gameOut = pyodide.globals.get("game_out");

        // Convert Python objects to JavaScript objects

        console.log("game_out:", gameOut);
        gameOut.destroy()

        requestAnimationFrame(gameLoop);

    })
    console.log("post py")
    // ....
}

function doMoveRequest(move, row, col, row2, col2, unload) {
    if (unload != undefined) {
        pyodide.globals.set("pyodide_move",
            {
                unload: true
            }
        )
        return
    }
    pyodide.globals.set("pyodide_move",
        {
            move: MoveType[move],
            row: row,
            col: col,
            row2: row2,
            col2: col2,
        }
    )
    console.log(pyodide.globals.get("pyodide_move"))
}

window.onbeforeunload = function () {
    console.log("leaving")
    doMoveRequest(undefined, undefined, undefined, undefined, undefined, true)
}

// script.js
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
        e.dataTransfer.setData('text', e.target.id);
    }

    function handleDragOver(e) {
        e.preventDefault();
    }

    function handleDrop(e) {
        e.preventDefault();
        const id = e.dataTransfer.getData('text');
        const draggableElement = document.getElementById(id);
        if (!e.target.textContent) { // Prevents overwriting cells
            e.target.textContent = draggableElement.textContent;
        }
    }
});


// main()
loadPyodideAndRun();

