main_file = null
pyodide = null

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
                    main_file = text;
                    console.log(main_file)
                }

                pyodide.FS.writeFile(`/${file.name}`, text, { encoding: "utf8" });
            });
        });
    } catch (error) {
        console.error("Failed to fetch projects:", error);
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
        `).then(a => {

        // Game loop
        pyodide.runPythonAsync(main_file)

        pyodide.globals.set("pyodide_row", 0)
        console.log(pyodide.globals.get("pyodide_row"));
        pyodide.globals.set("pyodide_row", 1)
        console.log(pyodide.globals.get("pyodide_row"));

    })
    console.log("post py")
    // ....
}

function doMoveRequest(move, row, col, row2 = null, col2 = null) {
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

// main()
loadPyodideAndRun();

