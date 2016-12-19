# Final_Project

---

### Development & Deployment utilities required

###### WINDOWS
* [git bash](http://www.geekgumbo.com/2010/04/09/installing-git-on-windows/)
* [docker on Windows](https://docs.docker.com/engine/installation/windows/)

###### MAC OS X
* [docker for Mac](https://docs.docker.com/docker-for-mac/)

###### LINUX
* [docker on Ubuntu](https://docs.docker.com/engine/installation/linux/ubuntulinux/)

---

### Getting the source code

##### make a development directory
~> mkdir dev

##### navigate into development directory
~> cd dev

##### initialize as git directory
~/dev> git init

##### clone git repository
~/dev> git clone https://github.com/bebingando/cs673f16-team1

##### navigate into cs673f16-team1 directory
~/dev> cd cs673f16-team1

##### checkout develop branch
~/dev/cs673f16-team1> git checkout -b develop

---

### Building Docker container composition
.
#### Please note: if you have preexisting images you want to save, you WILL want to modify the following script, or remove team_alpha_project* images by hand

.

##### remove all images
~/dev/cs673f16-team1/docker> ./remove_all_images

##### building docker composition and running the application
~/dev/cs673f16-team1/docker> ./build_image

##### the aforementioned build_image script will make migration files, run the database migration and populate the database.
.
##### helpful commands for listing and cleaning up images and containers
listing all images: **docker images**
removing an image: **docker rmi IMAGE_NAME:IMAGE_TAG**
listing all containers: **docker ps -a**
removing a container: **docker rm CONTAINER_TAG**

---

### Accessing the application

##### navigate to http://localhost:8000 in a browser



