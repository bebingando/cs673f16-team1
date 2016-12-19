# Final_Project

---

### Development & Deployment utilities required

###### WINDOWS
* [git bash](http://www.geekgumbo.com/2010/04/09/installing-git-on-windows/)
* [docker on Windows](https://docs.docker.com/engine/installation/windows/)
* [docker Toolbox](https://github.com/docker/toolbox/releases/tag/v1.12.3) (comes with Docker Quickstart, Kitematic, Oracle VM VirtualBox)

**Ensure Virtualization** (Enable Intel Virtualization Technology (also known as Intel VT) or AMD-V depending on the brand of the processor.)
-Otherwise, Docker will not be able to create a Virtual Machine for the project to run from.
1) Reboot computer and enter BIOS to change it. The exact button to enter the menu varies from manufacturer to manufacturer. 
2) Once in the BIOS, open the Processor submenu 
3) Open the Processor submenu The processor settings menu may be hidden in the Chipset, Advanced CPU Configuration or Northbridge.
4) Enable Intel Virtualization Technology (also known as Intel VT) or AMD-V depending on the brand of the processor. The virtualization extensions may be labeled Virtualization Extensions, Vanderpool or various other names depending on the OEM and system BIOS.
5) Save and Exit


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

### Building Docker container composition (linux)
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

### Building Docker container composition (Windows)
#### **Run Docker and Creat Image** [Version 1.12.1]
If running the latest version follow these instructions, if not, skip to 4.2

1) Click Docker icon
2) Powershell window will be opened, navigate to the directory you placed to project in. 
3) Open the subfolder 'docker'
4) Copy resources into folder using command: 
   > cp -r ../group1/ resources/group1
5) Build the image and container using the command:
   > docker build -t cs673/team_alpha_project:latest ./ 
6) Run the server:
   > docker-compose up
7) Open browser and navigate to 127.0.0.1:8000

#### **Run Docker and Creat Image** (Older Docker version)

1) Click Docker icon
2) Powershell window will be opened, navigate to the directory you placed to project in. 
3) Open the subfolder 'docker'
4) Create project image and container with the command:
  > ./build_image
5) Run Kitematic to display running container. On Web preview box, click arrow above preview. Note IP address for running project.


---

### Accessing the application

##### navigate to http://localhost:8000 in a browser
.
#### Login Credentials, API interfaces

1) Superuser: **test**, Password: **testpw**
2) Navigate to Issue Tracker
3) You can access Admin page through Admin option on page. 
4) Through Powershell, pip install httpie. You can interact with API    endpoints/make REST calls i.e. GET, POST, PATCH.
   [Cheatsheet](http://ricostacruz.com/cheatsheets/httpie.html)

#### You must get a token to interact with API:
 - http POST localhost:8000/api-token-auth/ username='test' password='testpw'
 - you will get a token in the form: token:----------------------------------
 - use token with REST calls. i.e.:
http GET localhost:8000/issue_tracker/api/users/ 'Authorization: Token 686025567253f9265af2a28e1c022932836e0813'
#### Chat client is under Communications tab to the left

#### Command Calls:
Create a new comment for an issue:
`/issue-comment issue=123 comment='comment'`
-Modify existing issue fields:
`/set-issue-status issue=123 status='valid status'`
`/set-issue-priority issue=123 priority='valid priority'`
`/set-issue-type issue=123 type='valid type'`
-Creat a new issue:
`/new-issue title='My sweet title'`
or
`/new-issue name='My sweet title'`

