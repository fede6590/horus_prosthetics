# Horus Prosthetics - Limb angle calculator

### Option 1: access the app with my shareable streamlit URL - FAILING (libgl1-mesa-glx libglib2.0-0 error)

Simply access the app using https://horusprosthetics-challenge.streamlit.app/

### Option 2: manual deployment in Streamlit Cloud (very easy but account needed) - FAILING

Log in to https://share.streamlit.io/deploy.
Clone the repository, use the URL to deploy the app, and the app.py script as entry point to deploy the app. In "advanced settings", select "Python 3.11"

That's it, ¡good luck!

### Option 3: local deployment using Docker client (less easy and needs Docker)

Make sure Docker is running, and use the Bash terminal to run the following commands:

```
docker build -t horus-app .
```

```
docker run -p 8501:8501 horus-app .
```

Now, access the app at http://localhost:8501 in your browser (you can also try http://0.0.0.0:8501).
