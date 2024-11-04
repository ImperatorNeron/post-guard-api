# PostGuardAPI - Task from Starnavi

## Overview

PostGuardAPI is a RESTful API designed for managing user-generated content, including posts and comments. It incorporates artificial intelligence for automatic comment blocking and intelligent auto-replies to user inquiries. The API also provides analytical insights into comments, including metrics on created and blocked comments, authentication by jwt etc.

## Requirements
- [Docker](https://www.docker.com/get-started/)
- [Docker Compose](https://docs.docker.com/compose/install/)


## How to Use

1. Clone the repository:
```bash
git clone https://github.com/ImperatorNeron/post-guard-api.git
cd your_repository
```
2. Install all required packages in **Requirements** section.
3. Set up environment variables. Create a .env file in the root directory and specify the required configurations. You can use .env.template

### Implemented Commands

#### Application
- ```scons up``` - up application
- ```scons logs``` - follow the logs in app container
- ```scons down``` - down application and all 

#### Application with database for tests
- ```scons up-test``` - up application for tests
- ```scons logs-test``` - follow the logs in test app container
- ```scons down-test``` - down test application and all 
- ```scons run-tests``` - run all tests 

#### Database migrations
- ```scons auto-migrations``` - autocreate file of tables
- ```scons migrate-up``` - apply migrations to head
- ```scons migrate-down``` - down migrations t base

## License

This project is licensed under the MIT License - see the [LICENSE](https://en.wikipedia.org/wiki/MIT_License) file for details.