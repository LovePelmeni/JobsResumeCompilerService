# JOBS SERVICE DOCKER SWARM DEPLOY GUIDE 

---
!! Make sure that you are already familiar with Docker-Swarm and Docker-Compose.

---

# Requirements 
~ `Docker` `1.3.8` *and higher*

~ `Docker-Compose 3.8` *and higher*

~ `Two Virtual Machines: One Main and One for Cluster Worker Node.`
If you haven't some yet. Go check this setUp Guide: [Setting Up Virtual Host Machines Using Docker.]("http://")

# Usage 

1. Initialize Cluster and Connect You Manager Node Docker-Swarm Cluster with command: `docker swarm init`

---
2. Clone this repo.
```editorconfig
    $ git clone https://github.com/LovePelmeni/JobsResumeCompiler.git
```

2.Go to the swarm directory in the project and run:
```editorconfig
    $ docker stack deploy --compose-file ./docker-compose.yaml jobs_resume_service
```

---

### External Links

*You Can Find Me in Social Media*

~ `GitHUB` http://github.com/LovePelmeni

~ `LinkedIn` Email: klimkiruk@gmail.com

