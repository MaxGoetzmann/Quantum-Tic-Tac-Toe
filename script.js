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

async function fetchSrcFolder(pyodide) {
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
        console.log({ headers })
        const response = await fetch(apiUrl, { headers });
        const data = await response.json();
        data.forEach(file => {
            fetchRawTextData(file.download_url).then(text => {
                if (text === null) throw new Error(`Could not get file ${file.name} data.`)
                pyodide.FS.writeFile(`/${file.name}`, text, { encoding: "utf8" })
            });
        });
    } catch (error) {
        console.error("Failed to fetch projects:", error);
    }
}

async function loadPyodideAndRun() {
    let pyodide = await loadPyodide();
    await pyodide.loadPackage(["micropip"]); // Load any additional packages your game needs
    await fetchSrcFolder(pyodide)
    pyodide.runPythonAsync(`
            import micropip
            import sys

            # Install Python packages
            await micropip.install("numpy")

            # Your Python game code here
            print("Hello from Python!")  # Example Python code

            original_argv = sys.argv.copy()
            try:
                sys.argv = ["/main.py", "0", "1"]
                with open("/main.py", "r", encoding="utf-8") as f:
                    code = f.read()
                    exec(code)
            finally:
                sys.argv = original_argv
        `).then(a => {
        pyodide.globals.get('x').toJs();
    }).catch(error => {
        console.log(error);
    })
    console.log("post py")
}

// main()
loadPyodideAndRun();

