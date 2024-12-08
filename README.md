
# PYXL - Autosearch

[https://img.shields.io/badge/Python-3.10-blue](https://img.shields.io/badge/Python-3.10-blue)

[https://img.shields.io/badge/Flask-3.0.0-green](https://img.shields.io/badge/Flask-3.0.0-green)

[https://img.shields.io/badge/License-MIT-yellow](https://img.shields.io/badge/License-MIT-yellow)

PYXL is very powerful tool to use in the office for automate extraction or read tasks from Excel files.

The objective of this API is help to automate the search, extract and read Excel files in a simple and efficient way. You don’t need the Microsoft Office Excel installed to use this. The accepted extensions are *.xlsx* and *.xslm*.

---

# Use cases

It was designed to solve one of the challenges that I faced working with backoffice functions, I learned common administrative processes and I saw many possibilities of automate work to save time. The problem to solved this time: “Read and update Excel files with specified references”, it is kind of incisive automation process. The source of data updated to was databases or another files.

You can use it as a service from the api or use the friendly web interface to input the necessary data and for the actions that it must perform. 

## Use & Limitations:

- When it receive input, it will perform only an extraction/read per time.
- It was designed to search, by a passed, filename in a specified path and then perform the action, in case of match, or it brings error.
- It perform a linear search into the directories, if you have many files to process in directory full of directories and files it can take a more time to finish.
- It is stateless and don’t have a database connected on it.
- No login is required to use.
- It just read the value from the cells, if it is formula it will bring just result.

---

A summary of the web interface application

[presentation openpyxl web interface.mp4](presentation_openpyxl_web_interface.mp4)

---

# Installation

### Requiremets:

- Python 3.10.0 or higher
- *pip* installed, as Python packages manager
- Optional: Git (to clone the repository)

### Download the PYXL:

You have 2 ways to do it: Clone the repository or Download the *.zip* file.

1. **CLONE REPOSITORY:**
    
    ** For this path you should have the git installed.
    
    ```jsx
    git clone https://github.com/seu-usuario/nome-do-repositorio.git
    ```
    

1. **DOWNLOAD:**
    
    You  can [click here](https://github.com) to go download directly from the GitHub’s repository.
    

### Install the dependencies:

After download the project, go to it’s directory and open a terminal window. 

```bash
cd pyxl-autosearch
```

Creation of a virtual environment (venv) is recommended before install the dependencies of the project. You can create, active and install by use the following code:

```bash
python -m venv venv # Create the virtual environment

# Activate environment
venv\Scripts\activate
# source venv/bin/activate # For Linux

pip install -r requirements.txt # Install the required dependencies
```

---

# How to configure for the first use?

**How to configure for the first use?**

- First, you need to create a environment file (*.env*), in the root of the project, it will have the path to search and to save the files as default. Your file should be like:

```
SEARCH_PATH=your/absolute/path/to/search
DEFAULT_SAVEPATH=your/absolute/path/to/save 
```

- There are some settings that you can set at *configs/settings.py*:
    
    ```python
    class Setup:
        def __init__(self):
            self.path = os.getenv("SEARCH_PATH") # It'll be loaded from .env file
            self.base_str_find = [] # String must be included in filename(OPTIONAL)
            self.ignored_str = [] # String must be ignored in filename(OPTIONAL)
            self.default_sheetname = "test" # Default sheetname to open in the excel file
            self.default_savepath = os.getenv("DEFAULT_SAVEPATH") # It'll be loaded from .env file
            self.extensions = [".xlsx", ".xlsm"] # Don't change this
    ```
    

---

# How to use

After set the configurations you are ready to run the Api.

1. To start the api, assuming you are in the root of the project, run the command:
    
    ```bash
    python run.py # -d as parameter, for debug purpose
    ```
    
2. The API will run at [localhost](http://localhost):5000 as default and you can change in the [*run.py*](http://run.py) if it is necessary.

Now you can choose how to interact with the application by 2 ways, endpoints and using a frontend interface:

### **ENDPOINTS (technical way)**:

1. To read data: *localhost:5000/pyxl/read*
    1. You must send a POST request with a list, in the body, of *json* objects. Valid cases:
        
        ```json
        [
            {
                "filename": "filename_test",
                "coordinate": "C9",
                "sheetname": "sheetname_optional"
            },
            {
                "filename": "test",
                "coordinate": "C1"
            }
        ]
        ```
        
2. To write data: *localhost:5000/pyxl/write*
    1. You must send a PATCH request with a list, in the body, of *json* objects. This require one more parameter (*value*) and accept one more optional parameter (*savepath*) :
        
        ```json
        [
            {
                "filename": "filename_test",
                "coordinate": "B7",
                "value": "new_value",
                "sheetname":"sheetname_optional",
                "savepath": "C:\\path\\to\\save\\optional"
            },
            {
                "filename": "filename_test",
                "coordinate": "B8",
                "value": "new_value",
                "savepath": "C:\\path\\to\\save\\optional"
            },
            {
                "filename": "filename_test",
                "coordinate": "B9",
                "value": "new_value",
                "sheetname":"sheetname_optional"
            },
            {
                "filename": "filename_test",
                "coordinate": "B9",
                "value": "new_value"
            }
        ]
        ```
        
    

### **FRONTEND INTERFACE (Easy way):**

You can set a list of objects via web interface and you can choose to write or read values at *localhost:5000/api.*

- This part was developed to make the non-developers to use easily, here there are some screens of the interfaces where can input the data to process:
    - *localhost:5000/api*
        
        ![Captura de ecrã 2024-12-05 164848.png](Captura_de_ecr_2024-12-05_164848.png)
        
    
    - *localhost:5000/api/read*
        
        ![Captura de ecrã 2024-12-03 164542.png](Captura_de_ecr_2024-12-03_164542.png)
        
    - *localhost:5000/api/write*
        
        ![Captura de ecrã 2024-12-05 164824.png](Captura_de_ecr_2024-12-05_164824.png)
        

---

# Documentation

If you want to know more information about, please check the available documentation via Swagger at [*localhost:5000/swagger*](http://localhost:5000/swagger). You will find more detailed specifications about the request and response there.

---

# Tests

The unity tests are under development and will be available soon.

---

# Contributions

This project is **open source** and welcomes contributions from the community.

I will be grateful to everyone who has provided ideas, fixes, feedback, and improvements.

### Want to contribute?

1. Fork this repository on GitHub
2. Clone this repository to your local machine
3. Create a new branch for your changes

### **Making Changes.**

1. Add your changes
2. Run tests (if applicable)
3. Commit your changes with a clear and descriptive commit message

### **Submitting a Pull Request.**

1. Push your changes to your fork on GitHub
2. Open a Pull Request and include a clear and descriptive title and explanation of your changes
3. I will review and merge your changes

---

# Tools and Resources Used

This project was made possible thanks to the following technologies and libraries:

- **Python**
- **Flask**
- **Swagger/OpenAPI**
- **OpenpyXL**
- **JavaScript**
- **Ajax**
- **Bootstrap**

---

# 📋 Credits

This project was carefully developed by:

- Luciano-project, Software Developer Committed to delivering efficient and accessible solutions to the community.

---

# License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute it under the terms of the license.