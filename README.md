# Setup

### Create a virtual environment

```bash
python3 -m venv venv # for unix
python -m venv venv # for windows
```

### Activate the virtual environment

```bash
source venv/bin/activate # for unix
venv\Scripts\activate # for windows
```

### Install the dependencies

```bash
pip install -r requirements.txt
```

### Set environment variables

- Create a `.env` file in the root directory of the project
- Copy the contents of `.env.example` into the `.env` file
- Replace the values of the environment variables with your own

```dotenv
PORT=5000
MAC_ADDRESS="00:00:00:00:00:00"
```

### Run the application

```bash
python __main__.py
```