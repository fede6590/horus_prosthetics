# Horus Prosthetics - Limb angle calculator

### Only options available (for now): local deployment using Docker client (less easy and needs Docker)

Make sure Docker is running, and use the Bash terminal to run the following commands:

```
docker build -t horus-app .
```

```
docker run -p 8501:8501 horus-app .
```

Now, access the app at http://localhost:8501 in your browser (you can also try http://0.0.0.0:8501).
