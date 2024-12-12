
# PYXL - Autosearch


![Python](https://img.shields.io/badge/Python-3.10-blue) ![Flask](https://img.shields.io/badge/Flask-3.0.0-green) ![MIT](https://img.shields.io/badge/License-MIT-yellow)


PYXL - Autosearch (or just PYXL) is very powerful tool that can be used for automate the extraction or update tasks from Excel files. In the core of this project, Python was used then to create the algorithms and the API to handle the users request.

The objective of this API is automate the search, extract and read for Excel files in a simple and efficient way. You don’t need the Microsoft Office Excel installed to use this and the accepted extensions are *.xlsx* and *.xslm*.

---

Here is a PYXL Interface demo. To see the entire and explained video, [click here](https://www.youtube.com/watch?v=jmosDh_VpNQ).
<br>** *You will be redirected to YouTube.*

<div align="center">
    
https://github.com/user-attachments/assets/84c41062-0e07-4e15-82f7-1e29dc9d9d32

</div>

---

# Use cases

It was designed to solve one of the challenges that I faced working with backoffice functions, I learned common administrative processes and I saw many possibilities of automate work to save time. The problem to solved this time: “Read and update Excel files with specified references”, it is kind of incisive automation process. The source of data, updated to, is databases and another files.

You can use it as a service from the api or use the friendly web interface to input the necessary data and for the actions that it must perform. 

![PYXL - Flow](https://github.com/user-attachments/assets/7a1288c4-8634-4974-aa68-42d92a27d673)

## Use & Limitations:

- When it receive input, it will perform only an extraction/read per time.
- It was designed to search, by a passed, filename in a specified path and then perform the action, in case of match, or it brings error.
- It perform a linear search into the directories, if you have many files to process in directory full of directories and files it can take a more time to finish.
- It is stateless and don’t have a database connected on it.
- No login is required to use.
- It just read the value from the cells, if it is formula it will bring just result.
- The extensions files allowed to work with is: *xlsx* and *xlsm*.

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
    
    You can [click here](https://github.com/Luciano-project/pyxl-autosearch/archive/refs/heads/master.zip) to go download directly from the GitHub’s repository.
    

### Install the dependencies:

After download the project, go to it’s directory and open a terminal window. 

```bash
cd pyxl-autosearch
```
---
### Make it easy!!
If you use Windows or Linux, the many following processes, can be automated by run the script *configure.py*.
***Just make sure that you are at the root of the project before continue.*
* Windows:
    ```shell
    python configure.py
    ```
* Linux:
    **Before run the python file, make sure that you have installed:
    ```bash
        apt install python3.10-venv
    ```
    and then:
    ```bash
    python3 configure.py
    ```

It will prepare all the environment, the script do:

  The first time:
    *  Create virtual enviroment named "*venv*"
    *  Active environment and install the dependences
    *  Create the directory for the sample
    *  Create a sample named *test.xlsx* at, the relative path:"*pyxl-autosearch/example/default_search/test.xlsx*"

Now all the configuration you need, until the section *"How to use?"*, for the first use is done.

---


Creation of a virtual environment *(venv)* is recommended before install the dependencies of the project. Once you create it, active and install by use the following code:

```bash
python -m venv venv # Create the virtual environment

# Activate environment
venv\Scripts\activate
# source venv/bin/activate # For Linux

pip install -r requirements.txt # Install the required dependencies
```

---


# How to configure for the first use?

- First, you need to create a environment file (*.env*) in the root of the project, it will have the path to search and to save the files as default. Your file should be like:

```
SEARCH_PATH=your/absolute/path/to/search
DEFAULT_SAVEPATH=your/absolute/path/to/save
DEBUG=True # You should change this for production
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

### **ENDPOINTS (for developers)**:

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
    1. You must send a *PATCH* request with a list, in the body, of *json* objects. This require one more parameter (*value*) and accept one more optional parameter (*savepath*) :
        
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
        
---


### **FRONTEND INTERFACE (Easy way):**

You can set a list of objects via web interface and you can choose to write or read values at *localhost:5000/api.*
* It was made using HTML, Bootstrap, JavaScript, Ajax,

- This part was developed to make the non-developers to use easily, here there are some screens of the interfaces where the user can input the data:
    - *localhost:5000/api*
        
        ![endpoint_api](https://github.com/user-attachments/assets/ab663029-242b-4ff1-85c1-05bbe71f832d)
    
    - *localhost:5000/api/read*

        ![endpoint_api_read](https://github.com/user-attachments/assets/b60b384e-3c6d-4762-8def-730c38245c21)
        
    - *localhost:5000/api/write*

        ![endpoint_api_write](https://github.com/user-attachments/assets/6b259fc9-92ad-4a32-b21b-d5fb5fedafda)

---


# Documentation

If you want to know more information about, please check the available documentation via Swagger at [*localhost:5000/swagger*](http://localhost:5000/swagger). You will find more detailed specifications about the request and response there.


![docs_swagger_read](https://github.com/user-attachments/assets/55ed7950-c3be-44b6-ae60-18d3a7012db9)


![docs_swagger_write](https://github.com/user-attachments/assets/b25f3f6a-491d-41bc-8851-c5d8d7e07c31)


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

The following technologies and libraries were used to build the application:

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

- Luciano Sousa, Software Developer, Committed to delivering efficient and accessible solutions to the community.


---


# License

This project is licensed under the **MIT License**.

Feel free to use, modify, and distribute it under the terms of the license.
